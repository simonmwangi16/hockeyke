from django.contrib import admin
from .models import (
    Match,
    PremierLeagueMenMatch,
    PremierLeagueWomenMatch,
    SuperLeagueMenMatch,
    SuperLeagueWomenMatch,
    NationalLeagueCentralZoneMatch,
    NationalLeagueEasternZoneMatch,
    NationalLeagueSouthernZoneMatch,
    NationalLeagueWesternZoneMatch,
)


class BaseMatchAdmin(admin.ModelAdmin):
    list_display = (
        "match_number",
        "home_team",
        "score",
        "away_team",
        "match_date",
        "match_time",     
        "venue",
        "status",
        
    )

    list_filter = (
        "status",
        "league_season__season",
        "match_date",
    )

    search_fields = (
        "match_number",
        "home_team__name",
        "home_team__short_name",
        "away_team__name",
        "away_team__short_name",
        "venue",
    )

    ordering = (
        "match_date",
        "match_time",
        "match_number",
    )

    list_select_related = (
        "league_season",
        "league_season__league",
        "league_season__season",
        "home_team",
        "away_team",
    )

    
    @admin.display(description="Score")
    def score(self, obj):
        return f"{obj.home_score} - {obj.away_score}"


@admin.register(Match)
class MatchAdmin(BaseMatchAdmin):
    pass


class LeagueFilteredMatchAdmin(BaseMatchAdmin):
    league_short_name = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(
            league_season__league__short_name=self.league_short_name
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "league_season" and self.league_short_name:
            kwargs["queryset"] = db_field.remote_field.model.objects.filter(
                league__short_name=self.league_short_name
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PremierLeagueMenMatch)
class PremierLeagueMenMatchAdmin(LeagueFilteredMatchAdmin):
    league_short_name = "PLM"


@admin.register(PremierLeagueWomenMatch)
class PremierLeagueWomenMatchAdmin(LeagueFilteredMatchAdmin):
    league_short_name = "PLW"


@admin.register(SuperLeagueMenMatch)
class SuperLeagueMenMatchAdmin(LeagueFilteredMatchAdmin):
    league_short_name = "SLM"


@admin.register(SuperLeagueWomenMatch)
class SuperLeagueWomenMatchAdmin(LeagueFilteredMatchAdmin):
    league_short_name = "SLW"


@admin.register(NationalLeagueCentralZoneMatch)
class NationalLeagueCentralZoneMatchAdmin(LeagueFilteredMatchAdmin):
    league_short_name = "NLM-CZ"


@admin.register(NationalLeagueEasternZoneMatch)
class NationalLeagueEasternZoneMatchAdmin(LeagueFilteredMatchAdmin):
    league_short_name = "NLM-EZ"


@admin.register(NationalLeagueSouthernZoneMatch)
class NationalLeagueSouthernZoneMatchAdmin(LeagueFilteredMatchAdmin):
    league_short_name = "NLM-SZ"


@admin.register(NationalLeagueWesternZoneMatch)
class NationalLeagueWesternZoneMatchAdmin(LeagueFilteredMatchAdmin):
    league_short_name = "NLM-WZ"