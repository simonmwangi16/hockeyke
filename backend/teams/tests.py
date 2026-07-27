from datetime import date, time

from django.test import TestCase
from django.urls import reverse

from competitions.models import League, LeagueSeason, Season
from matches.models import Match
from teams.models import Team


class TeamMatchesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        season = Season.objects.create(name="2026")
        league = League.objects.create(name="Premier League", gender="MEN")
        league_season = LeagueSeason.objects.create(league=league, season=season)
        cls.team = Team.objects.create(name="Warriors", gender="MEN")
        opponent = Team.objects.create(name="Blazers", gender="MEN")

        cls.oldest_match = Match.objects.create(
            league_season=league_season,
            home_team=cls.team,
            away_team=opponent,
            match_date=date(2026, 1, 10),
            match_time=time(12, 0),
        )
        cls.latest_match = Match.objects.create(
            league_season=league_season,
            home_team=opponent,
            away_team=cls.team,
            match_date=date(2026, 2, 10),
            match_time=time(15, 0),
        )

    def test_matches_are_returned_in_descending_date_order(self):
        response = self.client.get(
            reverse("team-matches", kwargs={"team_id": self.team.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [match["id"] for match in response.json()["matches"]],
            [self.latest_match.id, self.oldest_match.id],
        )
