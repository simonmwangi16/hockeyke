from django.core.management.base import BaseCommand
from django.db import transaction

from matches.models import Match
from teams.models import TeamLeagueSeason


class Command(BaseCommand):
    help = "Backfill league-season team memberships from existing matches"

    def add_arguments(self, parser):
        parser.add_argument(
            "--season",
            help="Limit the backfill to one season name, for example 2026",
        )
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        matches = Match.objects.all()
        season = (options.get("season") or "").strip()

        if season:
            matches = matches.filter(league_season__season__name=season)

        home_pairs = matches.values_list("league_season_id", "home_team_id")
        away_pairs = matches.values_list("league_season_id", "away_team_id")
        fixture_pairs = set(home_pairs).union(away_pairs)

        league_season_ids = {pair[0] for pair in fixture_pairs}
        existing_pairs = set(
            TeamLeagueSeason.objects.filter(
                league_season_id__in=league_season_ids,
            ).values_list("league_season_id", "team_id")
        )
        missing_pairs = sorted(fixture_pairs - existing_pairs)

        self.stdout.write(f"Fixture participation pairs: {len(fixture_pairs)}")
        self.stdout.write(f"Existing memberships: {len(existing_pairs)}")
        self.stdout.write(f"Missing memberships: {len(missing_pairs)}")

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING("Dry run: no records created"))
            return

        created_ids = []
        with transaction.atomic():
            for league_season_id, team_id in missing_pairs:
                membership, created = TeamLeagueSeason.objects.get_or_create(
                    league_season_id=league_season_id,
                    team_id=team_id,
                )
                if created:
                    created_ids.append(membership.id)

        self.stdout.write(
            self.style.SUCCESS(f"Created memberships: {len(created_ids)}")
        )
        if created_ids:
            self.stdout.write(
                "Created membership IDs: "
                + ",".join(str(record_id) for record_id in created_ids)
            )
