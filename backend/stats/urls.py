from django.urls import path
from .views import league_standings, team_stats, season_stats

urlpatterns = [
    path("standings/", league_standings, name="league-standings"),
    path("teams/", team_stats, name="team-stats"),
    path("season/", season_stats, name="season-stats"),
]