from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from competitions.models import League, LeagueSeason, Season
from matches.models import Match
from teams.models import Team


class HomeMatchFeedTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        season = Season.objects.create(name="2026")
        league = League.objects.create(name="Premier League", gender="MEN")
        league_season = LeagueSeason.objects.create(league=league, season=season)
        home_team = Team.objects.create(name="Warriors", gender="MEN")
        away_team = Team.objects.create(name="Blazers", gender="MEN")

        cls.upcoming = []
        cls.results = []
        for offset in range(1, 5):
            cls.upcoming.append(
                Match.objects.create(
                    league_season=league_season,
                    home_team=home_team,
                    away_team=away_team,
                    match_date=date.today() + timedelta(days=offset),
                    status="SCHEDULED",
                )
            )
            cls.results.append(
                Match.objects.create(
                    league_season=league_season,
                    home_team=away_team,
                    away_team=home_team,
                    match_date=date.today() - timedelta(days=offset),
                    status="FT",
                    home_score=offset,
                    away_score=0,
                )
            )

        old_season = Season.objects.create(name="2025")
        old_league_season = LeagueSeason.objects.create(
            league=league,
            season=old_season,
        )
        Match.objects.create(
            league_season=old_league_season,
            home_team=home_team,
            away_team=away_team,
            match_date=date.today() + timedelta(days=1),
            status="SCHEDULED",
        )

    def test_feed_is_limited_ordered_and_filtered_by_season(self):
        response = self.client.get(
            reverse("home-match-feed"),
            {"season": "2026"},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["season"], "2026")
        self.assertEqual(
            [match["id"] for match in data["upcoming"]],
            [match.id for match in self.upcoming[:3]],
        )
        self.assertEqual(
            [match["id"] for match in data["recent_results"]],
            [match.id for match in self.results[:3]],
        )
        self.assertTrue(
            all(match["status"] == "SCHEDULED" for match in data["upcoming"])
        )
        self.assertTrue(
            all(match["status"] == "FT" for match in data["recent_results"])
        )


class LeagueMatchesTests(TestCase):
    def test_uses_latest_dated_month_when_only_past_scheduled_matches_exist(self):
        season = Season.objects.create(name="2026")
        league = League.objects.create(
            name="Super League",
            short_name="SLM",
            gender="MEN",
        )
        league_season = LeagueSeason.objects.create(
            league=league,
            season=season,
        )
        home_team = Team.objects.create(name="Parkroad Badgers", gender="MEN")
        away_team = Team.objects.create(name="Parkroad Tigers", gender="MEN")
        latest_date = date.today() - timedelta(days=10)

        latest_match = Match.objects.create(
            league_season=league_season,
            home_team=home_team,
            away_team=away_team,
            match_date=latest_date,
            status="SCHEDULED",
        )
        Match.objects.create(
            league_season=league_season,
            home_team=away_team,
            away_team=home_team,
            match_date=date.today() - timedelta(days=45),
            status="SCHEDULED",
        )

        response = self.client.get(
            reverse("matches"),
            {
                "league": "super-league-men",
                "season": "2026",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["year"], latest_date.year)
        self.assertEqual(response.json()["month"], latest_date.month)
        self.assertIn(
            latest_match.id,
            [match["id"] for match in response.json()["matches"]],
        )
