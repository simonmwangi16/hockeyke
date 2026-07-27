from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404

from competitions.models import LeagueSeason
from .models import Standings
from .services import calculate_standings


@admin.register(Standings)
class StandingsAdmin(admin.ModelAdmin):
    change_list_template = "admin/stats/standings_changelist.html"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return Standings.objects.none()

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "league-season/<int:league_season_id>/",
                self.admin_site.admin_view(self.standings_view),
                name="stats_standings_detail",
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        league_seasons = LeagueSeason.objects.select_related(
            "league",
            "season",
        ).order_by(
            "-season__name",
            "league__gender",
            "league__name",
            "league__zone",
        )

        context = {
            **(extra_context or {}),
            "league_seasons": league_seasons,
        }

        return super().changelist_view(request, extra_context=context)

    def standings_view(self, request, league_season_id):
        league_season = get_object_or_404(LeagueSeason, id=league_season_id)
        standings = calculate_standings(league_season)

        context = {
            **self.admin_site.each_context(request),
            "title": f"Standings - {league_season}",
            "league_season": league_season,
            "standings": standings,
        }

        return render(request, "admin/stats/standings_detail.html", context)