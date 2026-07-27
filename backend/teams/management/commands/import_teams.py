import csv
from django.core.management.base import BaseCommand
from teams.models import Team


class Command(BaseCommand):
    help = "Import teams from CSV"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        gender_map = {
            "M": "MEN",
            "F": "WOMEN",
            "W": "WOMEN",
            "MEN": "MEN",
            "WOMEN": "WOMEN",
        }

        created_count = 0
        updated_count = 0

        with open(csv_file, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["tname"].strip()
                short_name = row.get("short_name", "").strip()
                gender_raw = row["gender"].strip().upper()
                gender = gender_map.get(gender_raw)

                if not gender:
                    self.stdout.write(
                        self.style.WARNING(f"Skipped {name}: invalid gender {gender_raw}")
                    )
                    continue

                team, created = Team.objects.update_or_create(
                    name=name,
                    defaults={
                        "short_name": short_name,
                        "gender": gender,
                        "active": True,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete. Created: {created_count}, Updated: {updated_count}"
            )
        )