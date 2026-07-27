from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from competitions.models import LeagueSeason
from .models import Match
from datetime import date
from stats.services import calculate_standings


LEAGUE_MAPPING = {
    "premier-league-men": {"name": "Premier League", "gender": "MEN", "zone": ""},
    "premier-league-women": {"name": "Premier League", "gender": "WOMEN", "zone": ""},
    "super-league-men": {"name": "Super League", "gender": "MEN", "zone": ""},
    "super-league-women": {"name": "Super League", "gender": "WOMEN", "zone": ""},

    "national-league-men-eastern-zone": {
    "name": "National League",
    "gender": "MEN",
    "zone": "Eastern Zone",
    },
    
    "national-league-men-central-zone": {
        "name": "National League",
        "gender": "MEN",
        "zone": "Central Zone",
    },
    "national-league-men-western-zone": {
        "name": "National League",
        "gender": "MEN",
        "zone": "Western Zone",
    },
    "national-league-men-southern-zone": {
        "name": "National League",
        "gender": "MEN",
        "zone": "Southern Zone",
    },
}

def get_month_year(request, base_queryset, mode="fixtures"):
    year = request.GET.get("year")
    month = request.GET.get("month")
    season = request.GET.get("season")

    if month:
        return int(year or season), int(month)

    if mode == "fixtures":
        match = base_queryset.order_by("match_date").first()
    else:
        match = base_queryset.order_by("-match_date").first()

    if match:
        return match.match_date.year, match.match_date.month

    return None, None


def get_league_season(request):
    season = request.GET.get("season")
    league_slug = request.GET.get("league")
    print("LEAGUE FROM URL:", request.GET.get("league"))

    if not season or not league_slug:
        return None, Response(
            {"detail": "season and league are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    league_info = LEAGUE_MAPPING.get(league_slug)

    if not league_info:
        return None, Response(
            {"detail": "Invalid league."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        league_season = LeagueSeason.objects.select_related("league", "season").get(
            season__name=season,
            league__name=league_info["name"],
            league__gender=league_info["gender"],
            league__zone=league_info["zone"],
        )
    except LeagueSeason.DoesNotExist:
        return None, Response(
            {"detail": "League season not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    return league_season, None


def serialize_match(match):
    return {
        "id": match.id,
        "league_season_id": match.league_season_id,
        "home_team_id": match.home_team_id,
        "away_team_id": match.away_team_id,
        "home_team": match.home_team.name,
        "away_team": match.away_team.name,
        "home_short_name": match.home_team.short_name,
        "away_short_name": match.away_team.short_name,

        # Formatted versions
        "match_date": match.match_date.strftime("%d %B %Y"),
        "match_time": match.match_time.strftime("%H:%M") if match.match_time else None,

        # Raw versions (useful later for sorting/filtering)
        "match_date_raw": match.match_date,
        "match_time_raw": match.match_time,
        
        "venue": match.venue,
        "status": match.status,
        "home_score": match.home_score,
        "away_score": match.away_score,
    }


def serialize_home_match(match):
    data = serialize_match(match)
    league = match.league_season.league
    competition = league.name
    if league.zone:
        competition = f"{competition} · {league.zone}"

    data.update({
        "competition": competition,
        "gender": league.get_gender_display(),
        "season": match.league_season.season.name,
    })
    return data


@api_view(["GET"])
def home_match_feed(request):
    season = request.GET.get("season", "").strip()
    matches = Match.objects.filter(
        match_date__isnull=False,
    ).select_related(
        "league_season__league",
        "league_season__season",
        "home_team",
        "away_team",
    )

    if season:
        matches = matches.filter(league_season__season__name=season)

    upcoming = matches.filter(
        status="SCHEDULED",
        match_date__gte=date.today(),
    ).order_by("match_date", "match_time", "id")[:3]

    recent_results = matches.filter(
        status="FT",
        match_date__lte=date.today(),
    ).order_by("-match_date", "-match_time", "-id")[:3]

    return Response({
        "season": season or None,
        "upcoming": [serialize_home_match(match) for match in upcoming],
        "recent_results": [
            serialize_home_match(match) for match in recent_results
        ],
    })


@api_view(["GET"])
def matches(request):
    league_season, error_response = get_league_season(request)
    if error_response:
        return error_response

    year = request.GET.get("year")
    month = request.GET.get("month")

    base_queryset = Match.objects.filter(
        league_season=league_season,
    ).select_related(
        "league_season",
        "home_team",
        "away_team",
    )

    # If visitor clicked previous/next month, use selected month
    if year and month:
        year = int(year)
        month = int(month)

    # On first page load, find next upcoming fixture month
    else:
        upcoming_match = base_queryset.filter(
            status="SCHEDULED",
            match_date__gte=date.today(),
        ).order_by("match_date", "match_time").first()

        # If no future fixture exists, fallback to latest played month
        if upcoming_match:
            year = upcoming_match.match_date.year
            month = upcoming_match.match_date.month
        else:
            latest_match = base_queryset.filter(
                status="FT",
            ).order_by("-match_date", "-match_time").first()

            if latest_match:
                year = latest_match.match_date.year
                month = latest_match.match_date.month
            else:
                return Response({
                    "year": None,
                    "month": None,
                    "matches": [],
                })

    queryset = base_queryset.filter(
        match_date__year=year,
        match_date__month=month,
    ).order_by("match_date", "match_time")

    return Response({
        "year": year,
        "month": month,
        "matches": [serialize_match(match) for match in queryset],
    })

@api_view(["GET"])
def match_detail(request, match_id):
    match = (
        Match.objects
        .select_related(
            "league_season",
            "league_season__league",
            "league_season__season",
            "home_team",
            "away_team",
        )
        .get(id=match_id)
    )

    return Response(serialize_match(match))


@api_view(["GET"])
def match_form(request, match_id):
    match = (
        Match.objects
        .select_related("home_team", "away_team", "league_season")
        .get(id=match_id)
    )

    def result_for_team(m, team):
        if m.home_score == m.away_score:
            return "D"

        if m.home_team_id == team.id:
            return "W" if m.home_score > m.away_score else "L"

        return "W" if m.away_score > m.home_score else "L"

    def serialize_recent_match(m, team):
        return {
            "id": m.id,
            "match_date": m.match_date,
            "home_team_id": m.home_team_id,
            "home_team": m.home_team.short_name,
            "away_team_id": m.away_team_id,
            "away_team": m.away_team.short_name,
            "home_score": m.home_score,
            "away_score": m.away_score,
            "status": m.status,
            "result": result_for_team(m, team),
        }

    def recent_matches(team):
        matches = (
            Match.objects
            .filter(
                league_season=match.league_season,
                status="FT",
            )
            .filter(Q(home_team=team) | Q(away_team=team))
            .exclude(id=match.id)
            .select_related("home_team", "away_team")
            .order_by("-match_date", "-match_time")[:5]
        )

        return [serialize_recent_match(m, team) for m in matches]

    return Response({
        "home_team": {
            "id": match.home_team_id,
            "name": match.home_team.name,
            "matches": recent_matches(match.home_team),
        },
        "away_team": {
            "id": match.away_team_id,
            "name": match.away_team.name,
            "matches": recent_matches(match.away_team),
        },
    })


@api_view(["GET"])
def match_league_table(request, match_id):
    match = (
        Match.objects
        .select_related("league_season", "home_team", "away_team")
        .get(id=match_id)
    )

    raw_standings = calculate_standings(match.league_season)

    standings = []

    for index, row in enumerate(raw_standings, start=1):
        team = row["team"]

        standings.append({
            "position": row.get("position", index),
            "team_id": team.id,
            "team": team.short_name,
            "played": row.get("played", 0),
            "won": row.get("won", 0),
            "drawn": row.get("drawn", 0),
            "lost": row.get("lost", 0),
            "goals_for": row.get("goals_for", 0),
            "goals_against": row.get("goals_against", 0),
            "goal_difference": row.get("goal_difference", 0),
            "points": row.get("points", 0),
        })

    return Response({
        "home_team_id": match.home_team_id,
        "away_team_id": match.away_team_id,
        "highlight_team_ids": [
            match.home_team_id,
            match.away_team_id,
        ],
        "standings": standings,
    })


@api_view(["GET"])
def match_head_to_head(request, match_id):
    match = Match.objects.select_related("home_team", "away_team", "league_season").get(id=match_id)

    h2h_matches = (
        Match.objects
        .filter(status="FT")
        .filter(
            Q(home_team=match.home_team, away_team=match.away_team) |
            Q(home_team=match.away_team, away_team=match.home_team)
        )
        .exclude(id=match.id)
        .order_by("-match_date")[:10]
        .select_related("home_team", "away_team")
    )

    home_wins = 0
    away_wins = 0
    draws = 0
    home_goals = 0
    away_goals = 0
    home_clean_sheets = 0
    away_clean_sheets = 0

    for m in h2h_matches:
        if m.home_team_id == match.home_team_id:
            home_score = m.home_score
            away_score = m.away_score
        else:
            home_score = m.away_score
            away_score = m.home_score

        home_goals += home_score or 0
        away_goals += away_score or 0

        if away_score == 0:
            home_clean_sheets += 1

        if home_score == 0:
            away_clean_sheets += 1

        if home_score == away_score:
            draws += 1
        elif home_score > away_score:
            home_wins += 1
        else:
            away_wins += 1

    return Response({
        "summary": {
            "home_team": match.home_team.short_name,
            "away_team": match.away_team.short_name,
            "home_wins": home_wins,
            "draws": draws,
            "away_wins": away_wins,
            "home_goals": home_goals,
            "away_goals": away_goals,
            "home_clean_sheets": home_clean_sheets,
            "away_clean_sheets": away_clean_sheets,
        },
        "matches": [serialize_match(m) for m in h2h_matches]
    })


@api_view(["GET"])
def match_team_stats(request, match_id):
    match = Match.objects.select_related("home_team", "away_team", "league_season").get(id=match_id)

    def team_stats(team):
        matches = (
            Match.objects
            .filter(league_season=match.league_season, status="FT")
            .filter(Q(home_team=team) | Q(away_team=team))
        )

        played = matches.count()
        wins = draws = losses = goals_for = goals_against = 0

        for m in matches:
            if m.home_team_id == team.id:
                gf = m.home_score
                ga = m.away_score
            else:
                gf = m.away_score
                ga = m.home_score

            goals_for += gf or 0
            goals_against += ga or 0

            if gf == ga:
                draws += 1
            elif gf > ga:
                wins += 1
            else:
                losses += 1

        return {
            "team_id": team.id,
            "team": team.short_name,
            "played": played,
            "won": wins,
            "drawn": draws,
            "lost": losses,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "goal_difference": goals_for - goals_against,
            "points": wins * 3 + draws,
        }

    return Response({
        "home_team": team_stats(match.home_team),
        "away_team": team_stats(match.away_team),
    })
