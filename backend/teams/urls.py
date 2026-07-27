from django.urls import path
from .views import team_overview, team_matches, team_stats, team_table

urlpatterns = [
    path("<int:team_id>/overview/", team_overview, name="team-overview"),
    path("<int:team_id>/matches/", team_matches, name="team-matches"),
    path("<int:team_id>/stats/", team_stats, name="team-stats"),
    path("<int:team_id>/table/", team_table, name="team-table"),
]