from datetime import date

from django.test import TestCase
from django.urls import reverse

from competitions.models import League, LeagueSeason, Season
from matches.models import Match
from teams.models import Team


class GlobalSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.season = Season.objects.create(name="2026")
        cls.league = League.objects.create(
            name="Premier League",
            short_name="PLM",
            gender="MEN",
        )
        cls.league_season = LeagueSeason.objects.create(
            league=cls.league,
            season=cls.season,
        )
        cls.home_team = Team.objects.create(
            name="Warriors",
            short_name="WAR",
            gender="MEN",
        )
        cls.away_team = Team.objects.create(
            name="Strathmore University",
            short_name="STR",
            gender="MEN",
        )
        cls.match = Match.objects.create(
            match_number="M001",
            league_season=cls.league_season,
            home_team=cls.home_team,
            away_team=cls.away_team,
            match_date=date(2026, 3, 14),
            venue="City Park",
            status="FT",
            home_score=2,
            away_score=1,
        )

    def search(self, query):
        return self.client.get(reverse("global-search"), {"q": query})

    def test_rejects_queries_shorter_than_two_characters(self):
        response = self.search("W")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Search query must contain at least 2 characters."},
        )

    def test_searches_teams_and_returns_profile_url(self):
        response = self.search("War")

        self.assertEqual(response.status_code, 200)
        team_result = next(
            result for result in response.json()["results"] if result["type"] == "team"
        )
        self.assertEqual(team_result["title"], "Warriors")
        self.assertEqual(team_result["url"], f"/teams/{self.home_team.id}/warriors")

    def test_searches_matches_by_team_venue_and_match_number(self):
        for query in ("Strathmore", "City Park", "M001"):
            with self.subTest(query=query):
                response = self.search(query)
                match_result = next(
                    result
                    for result in response.json()["results"]
                    if result["type"] == "match"
                )
                self.assertEqual(match_result["id"], self.match.id)
                self.assertIn("2–1", match_result["subtitle"])

    def test_searches_seasons_and_competitions(self):
        response = self.search("2026")
        result_types = {result["type"] for result in response.json()["results"]}

        self.assertIn("season", result_types)
        self.assertIn("competition", result_types)

        response = self.search("PLM")
        competition = next(
            result
            for result in response.json()["results"]
            if result["type"] == "competition"
        )
        self.assertEqual(
            competition["url"],
            "/league/men/premier-league?season=2026&tab=table",
        )
