from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from competitions.models import LeagueSeason
from .services import calculate_standings, calculate_team_stats


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


@api_view(["GET"])
def league_standings(request):
    season = request.GET.get("season")
    league_slug = request.GET.get("league")

    if not season or not league_slug:
        return Response(
            {"detail": "season and league are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    league_info = LEAGUE_MAPPING.get(league_slug)

    if not league_info:
        return Response(
            {"detail": "Invalid league."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        league_season = LeagueSeason.objects.select_related(
            "league",
            "season",
        ).get(
            season__name=season,
            league__name=league_info["name"],
            league__gender=league_info["gender"],
            league__zone=league_info["zone"],
        )
    except LeagueSeason.DoesNotExist:
        return Response(
            {"detail": "League season not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    standings = calculate_standings(league_season)

    data = []

    for position, row in enumerate(standings, start=1):
        team = row["team"]

        data.append({
            "position": position,
            "team_id": team.id,
            "team": team.name,
            "short_name": team.short_name,
            "played": row["played"],
            "won": row["won"],
            "drawn": row["drawn"],
            "lost": row["lost"],
            "goals_for": row["goals_for"],
            "goals_against": row["goals_against"],
            "goal_difference": row["goal_difference"],
            "clean_sheets": row.get("clean_sheets", 0),
            "yellow_cards": row.get("yellow_cards", 0),
            "red_cards": row.get("red_cards", 0),
            "points": row["points"],
            "form": row["form"],
        })

    return Response({
        "league": {
            "slug": league_slug,
            "name": league_info["name"],
            "gender": league_info["gender"],
            "zone": league_info["zone"],
        },
        "season": season,
        "standings": data,
    })


#per team season stat
@api_view(["GET"])
def team_stats(request):
    season = request.GET.get("season")
    league_slug = request.GET.get("league")

    if not season or not league_slug:
        return Response(
            {"detail": "season and league are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    league_info = LEAGUE_MAPPING.get(league_slug)

    if not league_info:
        return Response(
            {"detail": "Invalid league."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        league_season = LeagueSeason.objects.select_related(
            "league",
            "season",
        ).get(
            season__name=season,
            league__name=league_info["name"],
            league__gender=league_info["gender"],
            league__zone=league_info["zone"],
        )
    except LeagueSeason.DoesNotExist:
        return Response(
            {"detail": "League season not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    stats = calculate_team_stats(league_season)

    data = []

    for row in stats:
        team = row["team"]

        data.append({
            "team_id": team.id,
            "team": team.name,
            "short_name": team.short_name,
            "goals_scored": row["goals_scored"],
            "goals_conceded": row["goals_conceded"],
            "clean_sheets": row["clean_sheets"],
            "longest_winning_streak": row["longest_winning_streak"],
            "longest_losing_streak": row["longest_losing_streak"],
        })

    return Response({
        "league": {
            "slug": league_slug,
            "name": league_info["name"],
            "gender": league_info["gender"],
            "zone": league_info["zone"],
        },
        "season": season,
        "stats": data,
    })


#season stats
@api_view(["GET"])
def season_stats(request):
    season = request.GET.get("season")
    league_slug = request.GET.get("league")

    if not season or not league_slug:
        return Response(
            {"detail": "season and league are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    league_info = LEAGUE_MAPPING.get(league_slug)

    if not league_info:
        return Response(
            {"detail": "Invalid league."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        league_season = LeagueSeason.objects.select_related(
            "league",
            "season",
        ).get(
            season__name=season,
            league__name=league_info["name"],
            league__gender=league_info["gender"],
            league__zone=league_info["zone"],
        )
    except LeagueSeason.DoesNotExist:
        return Response(
            {"detail": "League season not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    team_stats = calculate_team_stats(league_season)

    def build_ranking(field):
        ranked = sorted(
            team_stats,
            key=lambda row: (-row[field], row["team"].name)
        )

        return [
            {
                "rank": index,
                "team_id": row["team"].id,
                "team": row["team"].name,
                "short_name": row["team"].short_name,
                "value": row[field],
            }
            for index, row in enumerate(ranked, start=1)
        ]

    return Response({
        "league": {
            "slug": league_slug,
            "name": league_info["name"],
            "gender": league_info["gender"],
            "zone": league_info["zone"],
        },
        "season": season,
        "stats": {
            "goals_scored": build_ranking("goals_scored"),
            "goals_conceded": build_ranking("goals_conceded"),
            "clean_sheets": build_ranking("clean_sheets"),
            "longest_winning_streak": build_ranking("longest_winning_streak"),
            "longest_losing_streak": build_ranking("longest_losing_streak"),
        },
    })