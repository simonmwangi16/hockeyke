from django.db import models


class Season(models.Model):
    name = models.CharField(max_length=20, unique=True)  # 2026 or 2026/27
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class League(models.Model):
    GENDER_CHOICES = [
        ("MEN", "Men"),
        ("WOMEN", "Women"),
    ]

    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=20, blank=True)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    zone = models.CharField(
        max_length=30,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "gender", "zone"],
                name="uniq_league"
            )
        ]
        ordering = ["name", "gender", "zone"]

    def __str__(self):
        parts = [self.name, self.gender]
        if self.zone:
            parts.append(self.zone)
        return " - ".join(parts)
    

class LeagueSeason(models.Model):
    league = models.ForeignKey(League, on_delete=models.PROTECT, related_name="league_seasons")
    season = models.ForeignKey(Season, on_delete=models.PROTECT, related_name="league_seasons")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["league", "season"],
                name="uniq_league_season"
            )
        ]
        ordering = ["-season__name", "league__name"]

    def __str__(self):
        return f"{self.league} - {self.season}"