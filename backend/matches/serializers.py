from rest_framework import serializers
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    league = serializers.CharField(source="league_season.league.name", read_only=True)
    season = serializers.CharField(source="league_season.season.name", read_only=True)
    home_team_name = serializers.CharField(source="home_team.name", read_only=True)
    away_team_name = serializers.CharField(source="away_team.name", read_only=True)
    home_team_short_name = serializers.CharField(source="home_team.short_name", read_only=True)
    away_team_short_name = serializers.CharField(source="away_team.short_name", read_only=True)

    class Meta:
        model = Match
        fields = [
            "id",
            "league",
            "season",
            "league_season",
            "home_team",
            "away_team",
            "home_team_name",
            "away_team_name",
            "home_team_short_name",
            "away_team_short_name",
            "match_date",
            "match_time",
            "venue",
            "status",
            "home_score",
            "away_score",
        ]