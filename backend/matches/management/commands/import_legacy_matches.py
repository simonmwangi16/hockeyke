import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from teams.models import Team
from competitions.models import LeagueSeason
from matches.models import Match


LEGACY_TEAM_MAP = {
    "Butali Warriors": "Warriors",
    "KCAU": "KCA University",
    "Kenyatta University Men": "Kenyatta University",
    "Mombasa Sports Club Men": "Mombasa Sports Club",
    "Sikh Union Nrb": "Sikh Union Nairobi",
    "Strathmore University Men": "Strathmore University",
    "Technical University Men": "Technical University",
    "USIU-A Men": "USIU-A",

    # National Men
    "UON": "University of Nairobi",
    "Daystar University Men": "Daystar University",

    "Daystar University Women": "Daystar University",
    "Kenyatta University Women": "Kenyatta University",
    "Mombasa Sports Club Women": "Mombasa Sports Club",
    "Multimedia University Women": "Multimedia University",
    "Strathmore University Women": "Strathmore University",
    "Technical University Women": "Technical University",
    "USIU-A Women": "USIU-A",
    "UON Women": "UON",
    "University of Nairobi": "UON",
    "Lakers": "Lakers Hockey Club",
}


CSV_ZONE_MAP = {
    "A": "Pool A",
    "B": "Pool B",
    "Pool A": "Pool A",
    "Pool B": "Pool B",
    "Central Zone": "Central Zone",
    "Eastern Zone": "Eastern Zone",
    "Southern Zone": "Southern Zone",
    "Western Zone": "Western Zone",
    "CZ": "Central Zone",
    "EZ": "Eastern Zone",
    "SZ": "Southern Zone",
    "WZ": "Western Zone",
}


class Command(BaseCommand):
    help = "Import legacy fixtures/results"

    def add_arguments(self, parser):
        parser.add_argument("csv_file")
        parser.add_argument("--league-name", required=True)
        parser.add_argument("--gender", required=True)
        parser.add_argument("--league-zone", default="")
        parser.add_argument("--use-csv-zone", action="store_true")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        league_name = options["league_name"]
        gender = options["gender"].upper()
        default_league_zone = options["league_zone"]
        use_csv_zone = options["use_csv_zone"]
        dry_run = options["dry_run"]

        created = 0
        updated = 0
        checked = 0
        skipped_playoffs = 0
        errors = []

        with open(csv_file, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row_number, row in enumerate(reader, start=2):
                league_zone = ""

                try:
                    season_year = int(row["season"])
                    csv_zone = self.clean_text(row.get("zone"))

                    if csv_zone.lower() == "playoff":
                        skipped_playoffs += 1
                        continue

                    league_zone = (
                        self.resolve_league_zone(csv_zone)
                        if use_csv_zone
                        else default_league_zone
                    )

                    league_season = LeagueSeason.objects.get(
                        league__name=league_name,
                        league__gender=gender,
                        league__zone=league_zone,
                        season__name=str(season_year),
                    )

                    home_name = self.clean_team_name(row["home_team_name"])
                    away_name = self.clean_team_name(row["away_team_name"])

                    home_team = self.get_team_or_error(
                        team_name=home_name,
                        csv_value=row["home_team_name"],
                        gender=gender,
                        side="home",
                    )

                    away_team = self.get_team_or_error(
                        team_name=away_name,
                        csv_value=row["away_team_name"],
                        gender=gender,
                        side="away",
                    )

                    match_datetime = self.parse_match_datetime(row["date"])
                    match_date = match_datetime.date()
                    match_time = match_datetime.time()

                    played = str(row["played"]).strip() == "1"

                    match_data = {
                        "league_season": league_season,
                        "home_team": home_team,
                        "away_team": away_team,
                        "match_date": match_date,
                        "match_time": match_time,
                        "match_number": self.clean_int(row.get("game_week")),
                        "venue": self.clean_text(row.get("venue")),
                        "home_score": self.clean_score(row.get("home_score")) if played else 0,
                        "away_score": self.clean_score(row.get("away_score")) if played else 0,
                        "status": "FT" if played else "SCHEDULED",
                    }

                    if dry_run:
                        checked += 1
                        continue

                    obj, was_created = Match.objects.update_or_create(
                        league_season=league_season,
                        home_team=home_team,
                        away_team=away_team,
                        match_date=match_date,
                        match_time=match_time,
                        defaults=match_data,
                    )

                    if was_created:
                        created += 1
                    else:
                        updated += 1

                except Exception as e:
                    errors.append(
                        f"Row {row_number}: {e} | "
                        f"league={league_name}, gender={gender}, "
                        f"csv_zone='{row.get('zone')}', resolved_zone='{league_zone}', "
                        f"season='{row.get('season')}'"
                    )

        self.stdout.write(f"Created: {created}")
        self.stdout.write(f"Updated: {updated}")
        self.stdout.write(f"Checked only: {checked}")
        self.stdout.write(f"Skipped playoffs: {skipped_playoffs}")
        self.stdout.write(f"Errors: {len(errors)}")

        for error in errors[:80]:
            self.stdout.write(self.style.ERROR(error))

    def get_team_or_error(self, team_name, csv_value, gender, side):
        try:
            return Team.objects.get(name=team_name, gender=gender)
        except Team.DoesNotExist:
            raise ValueError(
                f"Missing {side} team: '{team_name}' from CSV value '{csv_value}'"
            )
        except Team.MultipleObjectsReturned:
            raise ValueError(
                f"Duplicate {side} team match: '{team_name}' with gender '{gender}'"
            )

    def parse_match_datetime(self, value):
        value = self.clean_text(value)

        parsed = parse_datetime(value)
        if parsed:
            return parsed

        for fmt in [
            "%d/%m/%Y %H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
        ]:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass

        raise ValueError(f"Invalid date: {value}")

    def resolve_league_zone(self, zone):
        zone = self.clean_text(zone)
        return CSV_ZONE_MAP.get(zone, zone)

    def clean_team_name(self, name):
        name = self.clean_text(name)
        return LEGACY_TEAM_MAP.get(name, name)

    def clean_text(self, value):
        if value is None:
            return ""
        return str(value).strip()

    def clean_int(self, value):
        if value in [None, ""]:
            return 0
        return int(float(value))

    def clean_score(self, value):
        if value in [None, "", "nan", "NULL"]:
            return 0
        return int(float(value))