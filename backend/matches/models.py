from django.db import models
from competitions.models import LeagueSeason
from teams.models import Team


class Match(models.Model):
    STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("LIVE", "Live"),
        ("FT", "Full Time"),
        ("POSTPONED", "Postponed"),
        ("CANCELLED", "Cancelled"),
    ]

    match_number = models.CharField(max_length=20, null=True)

    league_season = models.ForeignKey(
        LeagueSeason,
        on_delete=models.PROTECT,
        related_name="matches"
    )

    home_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="home_matches"
    )

    away_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="away_matches"
    )

    match_date = models.DateField(blank=True, null=True)
    match_time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="SCHEDULED")

    home_score = models.PositiveSmallIntegerField(default=0)
    away_score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "All Matches"
        verbose_name_plural = "All Matches"
        ordering = ["match_date", "match_time"]

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
    

class MatchEvent(models.Model):
    EVENT_CHOICES = [
        ("GOAL", "Goal"),
        ("GREEN_CARD", "Green Card"),
        ("YELLOW_CARD", "Yellow Card"),
        ("RED_CARD", "Red Card"),
    ]

    GOAL_TYPE_CHOICES = [
        ("FIELD_GOAL", "Field Goal"),
        ("PENALTY_CORNER", "Penalty Corner"),
        ("PENALTY_STROKE", "Penalty Stroke"),
    ]

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="events")
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    player_name = models.CharField(max_length=100, blank=True)

    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    minute = models.PositiveSmallIntegerField()

    goal_type = models.CharField(
        max_length=30,
        choices=GOAL_TYPE_CHOICES,
        blank=True,
    )

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["match", "minute"]

    def __str__(self):
        return f"{self.match} - {self.event_type} - {self.minute}'"
    

class PremierLeagueMenMatch(Match):
    class Meta:
        proxy = True
        verbose_name = "PLM Match"
        verbose_name_plural = "PLM Matches"


class PremierLeagueWomenMatch(Match):
    class Meta:
        proxy = True
        verbose_name = "PLW Match"
        verbose_name_plural = "PLW Matches"


class SuperLeagueMenMatch(Match):
    class Meta:
        proxy = True
        verbose_name = "SLM Match"
        verbose_name_plural = "SLM Matches"


class SuperLeagueWomenMatch(Match):
    class Meta:
        proxy = True
        verbose_name = "SLW Match"
        verbose_name_plural = "SLW Matches"


class NationalLeagueCentralZoneMatch(Match):
    class Meta:
        proxy = True
        verbose_name = "NLM-CZ Match"
        verbose_name_plural = "NLM-CZ Matches"


class NationalLeagueEasternZoneMatch(Match):
    class Meta:
        proxy = True
        verbose_name = "NLM-EZ Match"
        verbose_name_plural = "NLM-EZ Matches"


class NationalLeagueSouthernZoneMatch(Match):
    class Meta:
        proxy = True
        verbose_name = "NLM-SZ Match"
        verbose_name_plural = "NLM-SZ Matches"


class NationalLeagueWesternZoneMatch(Match):
    class Meta:
        proxy = True
        verbose_name = "NLM-WZ Match"
        verbose_name_plural = "NLM-WZ Matches"