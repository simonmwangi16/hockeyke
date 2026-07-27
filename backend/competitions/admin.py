from django.contrib import admin
from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.utils.html import format_html

from .models import Season, League, LeagueSeason
from stats.services import calculate_standings


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "is_current")
    list_filter = ("is_current",)
    search_fields = ("name",)


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "gender", "zone")
    list_filter = ("gender", "short_name", "zone")
    search_fields = ("name", "short_name", "zone")


@admin.register(LeagueSeason)
class LeagueSeasonAdmin(admin.ModelAdmin):
    list_display = (
        "league",
        "season",
        "view_standings",
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:league_season_id>/standings/",
                self.admin_site.admin_view(self.standings_view),
                name="competitions_leagueseason_standings",
            ),
        ]
        return custom_urls + urls

    def view_standings(self, obj):
        return format_html(
            '<a class="button" href="{}">View standings</a>',
            f"{obj.id}/standings/"
        )

    view_standings.short_description = "Standings"

    def standings_view(self, request, league_season_id):
        league_season = get_object_or_404(LeagueSeason, id=league_season_id)
        standings = calculate_standings(league_season)

        context = {
            **self.admin_site.each_context(request),
            "title": f"Standings - {league_season}",
            "league_season": league_season,
            "standings": standings,
        }

        return render(request, "admin/competitions/standings.html", context)