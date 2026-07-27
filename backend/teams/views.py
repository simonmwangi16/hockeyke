from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from teams.models import Team
from matches.models import Match
from stats.services import calculate_standings, calculate_team_stats


def serialize_match(match, team=None):
    return {
        "id": match.id,
        "match_date": match.match_date.strftime("%d %B %Y") if match.match_date else None,
        "match_date_raw": match.match_date,
        "match_time": match.match_time.strftime("%H:%M") if match.match_time else None,
        "venue": match.venue,
        "status": match.status,
        "home_team_id": match.home_team_id,
        "away_team_id": match.away_team_id,
        "home_team": match.home_team.name,
        "away_team": match.away_team.name,
        "home_short_name": match.home_team.short_name,
        "away_short_name": match.away_team.short_name,
        "home_score": match.home_score,
        "away_score": match.away_score,
        "is_home": match.home_team_id == team.id if team else None,
    }


def get_team(team_id):
    try:
        return Team.objects.get(id=team_id), None
    except Team.DoesNotExist:
        return None, Response(
            {"detail": "Team not found."},
            status=status.HTTP_404_NOT_FOUND,
        )


def get_active_league_season(team):
    latest_match = (
        Match.objects
        .filter(
            Q(home_team=team) | Q(away_team=team)
        )
        .select_related(
            "league_season",
            "league_season__league",
            "league_season__season",
        )
        .order_by(
            "-league_season__season__name"
        )
        .first()
    )

    return latest_match.league_season if latest_match else None

def get_team_form(team, league_season):
    matches = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team),
        league_season=league_season,
        status="FT",
    ).order_by("-match_date", "-match_time")[:5]

    form = []

    for match in matches:
        if match.home_team_id == team.id:
            if match.home_score > match.away_score:
                form.append("W")
            elif match.home_score < match.away_score:
                form.append("L")
            else:
                form.append("D")
        else:
            if match.away_score > match.home_score:
                form.append("W")
            elif match.away_score < match.home_score:
                form.append("L")
            else:
                form.append("D")

    return form


@api_view(["GET"])
def team_overview(request, team_id):
    team, error = get_team(team_id)
    if error:
        return error

    league_season = get_active_league_season(team)

    if not league_season:
        return Response({
            "team": {
                "id": team.id,
                "name": team.name,
                "short_name": team.short_name,
                "gender": team.gender,
            },
            "detail": "No matches found for this team.",
        })

    team_matches = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team),
        league_season=league_season,
    ).select_related("home_team", "away_team")

    last_match = team_matches.filter(status="FT").order_by(
        "-match_date", "-match_time"
    ).first()

    next_match = team_matches.filter(status="SCHEDULED").order_by(
        "match_date", "match_time"
    ).first()

    standings = calculate_standings(league_season)

    print([(i + 1, row["team"].name) for i, row in enumerate(standings)])
    print("PROFILE TEAM:", team.name)

    team_position = None
    snapshot_rows = []
    snapshot_start_position = 1

    for index, row in enumerate(standings, start=1):
        if row["team"].id == team.id:
            team_position = index

            team_index = index - 1

            start = team_index - 1
            end = team_index + 2

            if start < 0:
                end += abs(start)
                start = 0

            if end > len(standings):
                start -= end - len(standings)
                end = len(standings)

            start = max(start, 0)

            snapshot_rows = standings[start:end]
            snapshot_start_position = start + 1
            break

    table_snapshot = []

    for offset, row in enumerate(snapshot_rows):
        position = snapshot_start_position + offset

        table_snapshot.append({
            "position": position,
            "team_id": row["team"].id,
            "team": row["team"].name,
            "short_name": row["team"].short_name,
            "played": row["played"],
            "goal_difference": row["goal_difference"],
            "points": row["points"],
            "is_profile_team": row["team"].id == team.id,
        })

    return Response({
        "team": {
            "id": team.id,
            "name": team.name,
            "short_name": team.short_name,
            "gender": team.gender,
        },
        "league_season": {
            "id": league_season.id,
            "league": str(league_season.league),
            "season": league_season.season.name,
        },
        "position": team_position,
        "form": get_team_form(team, league_season),
        "last_match": serialize_match(last_match, team) if last_match else None,
        "next_match": serialize_match(next_match, team) if next_match else None,
        "table_snapshot": table_snapshot,
    })

@api_view(["GET"])
def team_matches(request, team_id):
    team, error = get_team(team_id)
    if error:
        return error

    league_season = get_active_league_season(team)

    if not league_season:
        return Response({"matches": []})

    matches = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team),
        league_season=league_season,
    ).select_related(
        "home_team",
        "away_team",
    ).order_by("match_date", "match_time")

    return Response({
        "team_id": team.id,
        "team": team.name,
        "matches": [serialize_match(match, team) for match in matches],
    })


@api_view(["GET"])
def team_stats(request, team_id):
    team, error = get_team(team_id)
    if error:
        return error

    league_season = get_active_league_season(team)

    if not league_season:
        return Response({"stats": None})

    all_stats = calculate_team_stats(league_season)

    team_row = next(
        (row for row in all_stats if row["team"].id == team.id),
        None,
    )

    if not team_row:
        return Response({"stats": None})

    return Response({
        "team": {
            "id": team.id,
            "name": team.name,
            "short_name": team.short_name,
        },
        "league_season": {
            "id": league_season.id,
            "league": str(league_season.league),
            "season": league_season.season.name,
        },
        "stats": {
            "goals_scored": team_row["goals_scored"],
            "goals_conceded": team_row["goals_conceded"],
            "clean_sheets": team_row["clean_sheets"],
            "longest_winning_streak": team_row["longest_winning_streak"],
            "longest_losing_streak": team_row["longest_losing_streak"],
        },
    })


@api_view(["GET"])
def team_table(request, team_id):
    team, error = get_team(team_id)
    if error:
        return error

    league_season = get_active_league_season(team)

    if not league_season:
        return Response({
            "team": {
                "id": team.id,
                "name": team.name,
                "short_name": team.short_name,
            },
            "league_season": None,
            "standings": [],
        })

    standings = calculate_standings(league_season)

    data = []

    for position, row in enumerate(standings, start=1):
        row_team = row["team"]

        data.append({
            "position": position,
            "team_id": row_team.id,
            "team": row_team.name,
            "short_name": row_team.short_name,
            "played": row["played"],
            "won": row["won"],
            "drawn": row["drawn"],
            "lost": row["lost"],
            "goals_for": row["goals_for"],
            "goals_against": row["goals_against"],
            "goal_difference": row["goal_difference"],
            "points": row["points"],
            "form": row.get("form", []),
            "is_profile_team": row_team.id == team.id,
        })

    return Response({
        "team": {
            "id": team.id,
            "name": team.name,
            "short_name": team.short_name,
        },
        "league_season": {
            "id": league_season.id,
            "league": str(league_season.league),
            "season": league_season.season.name,
        },
        "standings": data,
    })
