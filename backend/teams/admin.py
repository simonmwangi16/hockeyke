from django.contrib import admin
from django import forms

from .models import Team, MenTeam, WomenTeam, TeamLeagueSeason


class TeamChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        gender = obj.get_gender_display() or "Gender not set"
        return f"{obj.name} — {gender}"


class TeamLeagueSeasonAdminForm(forms.ModelForm):
    team = TeamChoiceField(
        queryset=Team.objects.order_by("name", "gender"),
    )

    class Meta:
        model = TeamLeagueSeason
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        team = cleaned_data.get("team")
        league_season = cleaned_data.get("league_season")

        if (
            team
            and league_season
            and team.gender != league_season.league.gender
        ):
            self.add_error(
                "team",
                (
                    f"Select a {league_season.league.get_gender_display()} team "
                    f"for {league_season}."
                ),
            )

        return cleaned_data


class BaseTeamAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "gender", "active")
    list_filter = ("active",)
    search_fields = ("name", "short_name")


@admin.register(MenTeam)
class MenTeamAdmin(BaseTeamAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(gender="MEN")

    def save_model(self, request, obj, form, change):
        obj.gender = "MEN"
        super().save_model(request, obj, form, change)


@admin.register(WomenTeam)
class WomenTeamAdmin(BaseTeamAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(gender="WOMEN")

    def save_model(self, request, obj, form, change):
        obj.gender = "WOMEN"
        super().save_model(request, obj, form, change)


@admin.register(TeamLeagueSeason)
class TeamLeagueSeasonAdmin(admin.ModelAdmin):
    form = TeamLeagueSeasonAdminForm
    list_display = (
        "team",
        "team_gender",
        "league_season",
        "league_gender",
    )
    list_filter = (
        "team__gender",
        "league_season__league__gender",
        "league_season__season",
        "league_season",
    )
    search_fields = (
        "team__name",
        "team__short_name",
        "league_season__league__name",
        "league_season__season__name",
    )
    list_select_related = (
        "team",
        "league_season__league",
        "league_season__season",
    )

    @admin.display(description="Team gender", ordering="team__gender")
    def team_gender(self, obj):
        return obj.team.get_gender_display()

    @admin.display(
        description="League gender",
        ordering="league_season__league__gender",
    )
    def league_gender(self, obj):
        return obj.league_season.league.get_gender_display()
