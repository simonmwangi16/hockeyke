from django.urls import path
from .views import (
     home_match_feed,
     matches,
     match_detail,
     match_form,
     match_league_table,
     match_head_to_head,
     match_team_stats,
)

urlpatterns = [
     path("", matches, name="matches"),
     path("home-feed/", home_match_feed, name="home-match-feed"),
     path("<int:match_id>/", match_detail, name="match-detail"),
     path("<int:match_id>/form/", match_form, name="match-form"),
     path("<int:match_id>/league-table/", match_league_table, name="match-league-table"),
     path("<int:match_id>/head-to-head/", match_head_to_head, name="match-head-to-head"),
     path("<int:match_id>/team-stats/", match_team_stats, name="match-team-stats"),
]
