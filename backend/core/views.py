from urllib.parse import urlencode

from django.db.models import Q
from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from competitions.models import League, LeagueSeason, Season
from matches.models import Match
from teams.models import Team


SEARCH_LIMIT = 6


def league_path(league):
    path = f"/league/{league.gender.lower()}/{slugify(league.name)}"
    if league.zone:
        path = f"{path}/{slugify(league.zone)}"
    return path


def with_query(path, **params):
    return f"{path}?{urlencode(params)}"


@api_view(["GET"])
def global_search(request):
    query = request.GET.get("q", "").strip()

    if len(query) < 2:
        return Response(
            {"detail": "Search query must contain at least 2 characters."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    teams = Team.objects.filter(
        Q(name__icontains=query) | Q(short_name__icontains=query)
    ).order_by("name")[:SEARCH_LIMIT]

    matches = (
        Match.objects.filter(
            Q(match_number__icontains=query)
            | Q(home_team__name__icontains=query)
            | Q(home_team__short_name__icontains=query)
            | Q(away_team__name__icontains=query)
            | Q(away_team__short_name__icontains=query)
            | Q(venue__icontains=query)
            | Q(league_season__league__name__icontains=query)
            | Q(league_season__league__short_name__icontains=query)
            | Q(league_season__league__zone__icontains=query)
            | Q(league_season__season__name__icontains=query)
        )
        .select_related(
            "home_team",
            "away_team",
            "league_season__league",
            "league_season__season",
        )
        .distinct()
        .order_by("-match_date", "-match_time", "-id")[:SEARCH_LIMIT]
    )

    seasons = Season.objects.filter(name__icontains=query).order_by("-name")[
        :SEARCH_LIMIT
    ]

    league_seasons = (
        LeagueSeason.objects.filter(
            Q(league__name__icontains=query)
            | Q(league__short_name__icontains=query)
            | Q(league__zone__icontains=query)
            | Q(league__gender__icontains=query)
            | Q(season__name__icontains=query)
        )
        .select_related("league", "season")
        .order_by("-season__name", "league__name", "league__gender", "league__zone")[
            :SEARCH_LIMIT
        ]
    )

    results = []

    for team in teams:
        results.append(
            {
                "type": "team",
                "id": team.id,
                "title": team.name,
                "subtitle": f"{team.get_gender_display() or 'Team'} · Team",
                "url": f"/teams/{team.id}/{slugify(team.name)}",
            }
        )

    for match in matches:
        score = (
            f"{match.home_score}–{match.away_score}"
            if match.status == "FT"
            else match.get_status_display()
        )
        date_label = match.match_date.strftime("%d %b %Y") if match.match_date else "Date TBC"
        results.append(
            {
                "type": "match",
                "id": match.id,
                "title": f"{match.home_team.name} vs {match.away_team.name}",
                "subtitle": f"{date_label} · {score} · {match.league_season.season.name}",
                "url": (
                    f"/match/{match.id}/"
                    f"{slugify(match.home_team.name)}-vs-{slugify(match.away_team.name)}"
                ),
            }
        )

    for season in seasons:
        results.append(
            {
                "type": "season",
                "id": season.id,
                "title": f"{season.name} season",
                "subtitle": "Browse competition tables",
                "url": with_query("/", season=season.name),
            }
        )

    for league_season in league_seasons:
        league = league_season.league
        labels = [league.get_gender_display()]
        if league.zone:
            labels.append(league.zone)
        labels.append(league_season.season.name)
        results.append(
            {
                "type": "competition",
                "id": league_season.id,
                "title": league.name,
                "subtitle": " · ".join(labels),
                "url": with_query(
                    league_path(league),
                    season=league_season.season.name,
                    tab="table",
                ),
            }
        )

    return Response({"query": query, "results": results})
