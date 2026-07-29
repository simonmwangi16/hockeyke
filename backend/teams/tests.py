from datetime import date, time
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from competitions.models import League, LeagueSeason, Season
from matches.models import Match
from teams.admin import TeamLeagueSeasonAdminForm
from teams.models import Team, TeamLeagueSeason


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


class TeamLeagueSeasonBackfillTests(TestCase):
    def test_backfill_derives_memberships_from_fixture_teams(self):
        season = Season.objects.create(name="2027")
        league = League.objects.create(name="Super League", gender="MEN")
        league_season = LeagueSeason.objects.create(
            league=league,
            season=season,
        )
        home_team = Team.objects.create(name="Home Team", gender="MEN")
        away_team = Team.objects.create(name="Away Team", gender="MEN")
        Match.objects.create(
            league_season=league_season,
            home_team=home_team,
            away_team=away_team,
        )

        dry_run_output = StringIO()
        call_command(
            "backfill_team_league_seasons",
            season="2027",
            dry_run=True,
            stdout=dry_run_output,
        )
        self.assertEqual(TeamLeagueSeason.objects.count(), 0)
        self.assertIn("Missing memberships: 2", dry_run_output.getvalue())

        call_command(
            "backfill_team_league_seasons",
            season="2027",
            stdout=StringIO(),
        )

        self.assertSetEqual(
            set(
                TeamLeagueSeason.objects.values_list(
                    "league_season_id",
                    "team_id",
                )
            ),
            {
                (league_season.id, home_team.id),
                (league_season.id, away_team.id),
            },
        )


class TeamLeagueSeasonAdminFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        season = Season.objects.create(name="2028")
        men_league = League.objects.create(name="Premier League", gender="MEN")
        cls.league_season = LeagueSeason.objects.create(
            league=men_league,
            season=season,
        )
        cls.men_team = Team.objects.create(
            name="University Hockey Club",
            gender="MEN",
        )
        cls.women_team = Team.objects.create(
            name="University Hockey Club",
            gender="WOMEN",
        )

    def test_team_choices_include_gender(self):
        field = TeamLeagueSeasonAdminForm.base_fields["team"]

        self.assertEqual(
            field.label_from_instance(self.men_team),
            "University Hockey Club — Men",
        )
        self.assertEqual(
            field.label_from_instance(self.women_team),
            "University Hockey Club — Women",
        )

    def test_rejects_team_with_different_gender_from_league(self):
        form = TeamLeagueSeasonAdminForm(
            data={
                "team": self.women_team.id,
                "league_season": self.league_season.id,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Select a Men team", form.errors["team"][0])

    def test_accepts_team_with_matching_gender(self):
        form = TeamLeagueSeasonAdminForm(
            data={
                "team": self.men_team.id,
                "league_season": self.league_season.id,
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
