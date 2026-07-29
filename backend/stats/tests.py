from django.test import TestCase

from competitions.models import League, LeagueSeason, Season
from matches.models import Match
from stats.services import calculate_standings
from teams.models import Team, TeamLeagueSeason


class StandingsParticipationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        season = Season.objects.create(name="2027")
        league = League.objects.create(
            name="Super League",
            short_name="SLM",
            gender="MEN",
        )
        cls.league_season = LeagueSeason.objects.create(
            league=league,
            season=season,
        )

    def test_membership_only_teams_have_zero_rows_in_alphabetical_order(self):
        zebra = Team.objects.create(name="Zebra Hockey Club", gender="MEN")
        alpha = Team.objects.create(name="Alpha Hockey Club", gender="MEN")
        TeamLeagueSeason.objects.create(
            team=zebra,
            league_season=self.league_season,
        )
        TeamLeagueSeason.objects.create(
            team=alpha,
            league_season=self.league_season,
        )

        standings = calculate_standings(self.league_season)

        self.assertEqual(
            [row["team"].name for row in standings],
            ["Alpha Hockey Club", "Zebra Hockey Club"],
        )
        for row in standings:
            self.assertEqual(row["played"], 0)
            self.assertEqual(row["won"], 0)
            self.assertEqual(row["drawn"], 0)
            self.assertEqual(row["lost"], 0)
            self.assertEqual(row["goals_for"], 0)
            self.assertEqual(row["goals_against"], 0)
            self.assertEqual(row["goal_difference"], 0)
            self.assertEqual(row["points"], 0)

    def test_fixture_teams_remain_visible_without_membership_records(self):
        home_team = Team.objects.create(name="Historical Home", gender="MEN")
        away_team = Team.objects.create(name="Historical Away", gender="MEN")
        Match.objects.create(
            league_season=self.league_season,
            home_team=home_team,
            away_team=away_team,
            status="SCHEDULED",
        )

        standings = calculate_standings(self.league_season)

        self.assertEqual(
            [row["team"].name for row in standings],
            ["Historical Away", "Historical Home"],
        )
