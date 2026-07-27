from django.contrib import admin
from .models import Team, MenTeam, WomenTeam, TeamLeagueSeason


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
    list_display = ("team", "league_season")
    list_filter = ("league_season",)
    search_fields = (
        "team__name",
        "league_season__league__name",
        "league_season__season__name",
    )