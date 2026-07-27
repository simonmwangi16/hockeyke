from django.db import models
from competitions.models import LeagueSeason

#Team Model
class Team(models.Model):
    GENDER_CHOICES = [
        ("MEN", "Men"),
        ("WOMEN", "Women"),
    ]

    name = models.CharField(max_length=80)
    short_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    logo = models.ImageField(upload_to="team_logos/", blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

#Menu Options
class MenTeam(Team):
    class Meta:
        proxy = True
        verbose_name = "Men Team"
        verbose_name_plural = "Men Teams"


class WomenTeam(Team):
    class Meta:
        proxy = True
        verbose_name = "Women Team"
        verbose_name_plural = "Women Teams"

#Team Per Season Model
class TeamLeagueSeason(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="league_memberships")
    league_season = models.ForeignKey(LeagueSeason, on_delete=models.CASCADE, related_name="team_memberships")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "league_season"],
                name="uniq_team_league_season"
            )
        ]
        ordering = ["league_season", "team__name"]

    def __str__(self):
        return f"{self.team} - {self.league_season}"