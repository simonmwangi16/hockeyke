<template>
  <AdminLayout>
    <div class="flex flex-col gap-8">
      <h1 class="sr-only">Kenya Hockey Fixtures, Results and Standings</h1>

      <section class="order-3">
        <h2 class="sr-only">Kenya Hockey League Tables</h2>
        <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
          <template
            v-for="competition in competitions"
            :key="competition.slug"
          >
            <article
              class="flex min-h-[390px] flex-col rounded-2xl border border-gray-200 bg-white p-5 transition hover:border-brand-300 dark:border-gray-800 dark:bg-white/[0.03] dark:hover:border-brand-700"
            >
            <div>
              <div>
                <h3 class="text-base font-semibold text-gray-900 dark:text-white">
                  {{ competition.name }}
                </h3>
                <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                  {{ competition.category }}
                </p>
              </div>
            </div>

            <div
              v-if="loadingByLeague[competition.slug]"
              class="flex flex-1 items-center justify-center py-8 text-sm text-gray-500"
            >
              Loading table...
            </div>

            <div
              v-else-if="errorsByLeague[competition.slug]"
              class="flex flex-1 flex-col items-center justify-center py-8 text-center"
            >
              <p class="text-sm text-red-500">
                {{ errorsByLeague[competition.slug] }}
              </p>
              <button
                type="button"
                class="mt-2 text-sm font-semibold text-brand-500 hover:underline"
                @click="fetchCompetitionStandings(competition)"
              >
                Try again
              </button>
            </div>

            <div
              v-else-if="!standingsByLeague[competition.slug]?.length"
              class="flex flex-1 items-center justify-center py-8 text-center text-sm text-gray-500"
            >
              No standings available.
            </div>

            <div v-else class="mt-5 flex-1 overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-gray-200 dark:border-gray-800">
                    <th class="py-2 text-left text-xs font-medium text-gray-500">#</th>
                    <th class="py-2 text-left text-xs font-medium text-gray-500">Team</th>
                    <th class="py-2 text-center text-xs font-medium text-gray-500">P</th>
                    <th class="py-2 text-center text-xs font-medium text-gray-500">GD</th>
                    <th class="py-2 text-right text-xs font-medium text-gray-500">Pts</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                  <tr
                    v-for="team in standingsByLeague[competition.slug]"
                    :key="team.team_id"
                  >
                    <td class="py-2.5 text-xs text-gray-500">{{ team.position }}</td>
                    <td class="py-2.5">
                      <RouterLink
                        :to="`/teams/${team.team_id}/${makeTeamSlug(team.team)}`"
                        class="text-xs font-semibold text-gray-900 hover:text-brand-500 hover:underline dark:text-white"
                      >
                        {{ team.short_name || team.team }}
                      </RouterLink>
                    </td>
                    <td class="py-2.5 text-center text-xs text-gray-700 dark:text-gray-300">
                      {{ team.played }}
                    </td>
                    <td class="py-2.5 text-center text-xs text-gray-700 dark:text-gray-300">
                      {{ team.goal_difference }}
                    </td>
                    <td class="py-2.5 text-right text-xs font-bold text-gray-900 dark:text-white">
                      {{ team.points }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="mt-4 border-t border-gray-200 pt-4 dark:border-gray-800">
              <RouterLink
                :to="{ path: competition.path, query: { season, tab: 'table' } }"
                class="text-sm font-semibold text-brand-500 hover:text-brand-600 hover:underline"
              >
                View more...
              </RouterLink>
            </div>
            </article>
          </template>
        </div>
      </section>

      <AdSenseUnit class="order-2" />

      <section class="order-1" aria-label="Fixtures and results">
        <div
          v-if="feedLoading"
          class="rounded-2xl border border-gray-200 bg-white px-5 py-8 text-center text-sm text-gray-500 dark:border-gray-800 dark:bg-white/[0.03]"
        >
          Loading fixtures and results...
        </div>
        <div
          v-else-if="feedError"
          class="rounded-2xl border border-gray-200 bg-white px-5 py-8 text-center dark:border-gray-800 dark:bg-white/[0.03]"
        >
          <p class="text-sm text-red-500">{{ feedError }}</p>
          <button
            type="button"
            class="mt-2 text-sm font-semibold text-brand-500 hover:underline"
            @click="fetchHomeFeed"
          >
            Try again
          </button>
        </div>
        <div v-else class="grid gap-4 lg:grid-cols-2">
          <article
            class="flex flex-col rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03]"
          >
            <div class="border-b border-gray-200 pb-4 dark:border-gray-800">
              <h2 class="text-base font-semibold text-gray-900 dark:text-white">
                Upcoming fixtures
              </h2>
            </div>

            <div
              v-if="upcomingMatches.length"
              class="flex-1 divide-y divide-gray-100 dark:divide-gray-800"
            >
              <RouterLink
                v-for="match in upcomingMatches"
                :key="match.id"
                :to="matchUrl(match)"
                class="block py-4 transition hover:text-brand-500 focus:outline-hidden focus:ring-2 focus:ring-brand-500"
              >
                <span class="block truncate text-center text-xs text-gray-500 dark:text-gray-400">
                  {{ match.competition }} · {{ match.gender }}
                </span>
                <span class="mt-2 grid grid-cols-[1fr_auto_1fr] items-center gap-3">
                  <span class="truncate text-right text-sm font-semibold text-gray-900 dark:text-white">
                    {{ match.home_short_name || match.home_team }}
                  </span>
                  <span class="rounded-lg bg-brand-50 px-3 py-2 text-sm font-bold text-brand-600 dark:bg-brand-500/10 dark:text-brand-400">
                    {{ match.match_time || "TBC" }}
                  </span>
                  <span class="truncate text-left text-sm font-semibold text-gray-900 dark:text-white">
                    {{ match.away_short_name || match.away_team }}
                  </span>
                </span>
                <span class="mt-2 block text-center text-xs text-gray-500 dark:text-gray-400">
                  {{ match.match_date }}
                  <template v-if="match.venue"> · {{ match.venue }}</template>
                </span>
              </RouterLink>
            </div>
            <p v-else class="flex flex-1 items-center justify-center py-8 text-sm text-gray-500">
              No upcoming fixtures are currently scheduled.
            </p>

          </article>

          <article
            class="flex flex-col rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03]"
          >
            <div class="border-b border-gray-200 pb-4 dark:border-gray-800">
              <h2 class="text-base font-semibold text-gray-900 dark:text-white">
                Latest results
              </h2>
            </div>

            <div
              v-if="recentResults.length"
              class="flex-1 divide-y divide-gray-100 dark:divide-gray-800"
            >
              <RouterLink
                v-for="match in recentResults"
                :key="match.id"
                :to="matchUrl(match)"
                class="block py-4 transition hover:text-brand-500 focus:outline-hidden focus:ring-2 focus:ring-brand-500"
              >
                <span class="block truncate text-center text-xs text-gray-500 dark:text-gray-400">
                  {{ match.competition }} · {{ match.gender }}
                </span>
                <span class="mt-2 grid grid-cols-[1fr_auto_1fr] items-center gap-3">
                  <span
                    class="truncate text-right text-sm text-gray-900 dark:text-white"
                    :class="resultTeamClass(match, 'home')"
                  >
                    {{ match.home_short_name || match.home_team }}
                  </span>
                  <span class="rounded-lg bg-gray-100 px-3 py-2 text-sm font-bold text-gray-900 dark:bg-gray-800 dark:text-white">
                    {{ match.home_score }}–{{ match.away_score }}
                  </span>
                  <span
                    class="truncate text-left text-sm text-gray-900 dark:text-white"
                    :class="resultTeamClass(match, 'away')"
                  >
                    {{ match.away_short_name || match.away_team }}
                  </span>
                </span>
                <span class="mt-2 block text-center text-xs text-gray-500 dark:text-gray-400">
                  {{ match.match_date }}
                </span>
              </RouterLink>
            </div>
            <p v-else class="flex flex-1 items-center justify-center py-8 text-sm text-gray-500">
              No completed results are available.
            </p>

          </article>
        </div>
      </section>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import AdSenseUnit from "@/components/ads/AdSenseUnit.vue";
import AdminLayout from "@/components/layout/AdminLayout.vue";
// @ts-expect-error The existing JavaScript API service has no declaration file.
import { getHomeMatchFeed, getLeagueStandings } from "@/services/leagueApi";
// @ts-expect-error The existing JavaScript slug utility has no declaration file.
import { makeTeamSlug } from "@/utils/slugs";

const route = useRoute();
const season = computed(() =>
  typeof route.query.season === "string" ? route.query.season : "2026",
);

defineOptions({
  name: "HockeyHomePage",
});

interface Competition {
  name: string;
  category: string;
  slug: string;
  path: string;
}

interface Standing {
  position: number;
  team_id: number;
  team: string;
  short_name: string;
  played: number;
  goal_difference: number;
  points: number;
}

interface HomeMatch {
  id: number;
  home_team: string;
  away_team: string;
  home_short_name: string;
  away_short_name: string;
  home_score: number;
  away_score: number;
  match_date: string;
  match_time: string | null;
  venue: string;
  status: string;
  competition: string;
  gender: string;
}

const competitions: Competition[] = [
  {
    name: "Premier League Men",
    category: "Men",
    slug: "premier-league-men",
    path: "/league/men/premier-league",
  },
  {
    name: "Super League Men",
    category: "Men",
    slug: "super-league-men",
    path: "/league/men/super-league",
  },
  {
    name: "National League Eastern Zone",
    category: "Men · National League",
    slug: "national-league-men-eastern-zone",
    path: "/league/men/national-league/eastern-zone",
  },
  {
    name: "National League Central Zone",
    category: "Men · National League",
    slug: "national-league-men-central-zone",
    path: "/league/men/national-league/central-zone",
  },
  {
    name: "National League Southern Zone",
    category: "Men · National League",
    slug: "national-league-men-southern-zone",
    path: "/league/men/national-league/southern-zone",
  },
  {
    name: "National League Western Zone",
    category: "Men · National League",
    slug: "national-league-men-western-zone",
    path: "/league/men/national-league/western-zone",
  },
  {
    name: "Premier League Women",
    category: "Women",
    slug: "premier-league-women",
    path: "/league/women/premier-league",
  },
  {
    name: "Super League Women",
    category: "Women",
    slug: "super-league-women",
    path: "/league/women/super-league",
  },
];

const standingsByLeague = ref<Record<string, Standing[]>>({});
const loadingByLeague = ref<Record<string, boolean>>({});
const errorsByLeague = ref<Record<string, string>>({});
const upcomingMatches = ref<HomeMatch[]>([]);
const recentResults = ref<HomeMatch[]>([]);
const feedLoading = ref(false);
const feedError = ref("");

const matchUrl = (match: HomeMatch) =>
  `/match/${match.id}/${makeTeamSlug(match.home_team)}-vs-${makeTeamSlug(match.away_team)}`;

const resultTeamClass = (match: HomeMatch, side: "home" | "away") => {
  if (match.home_score === match.away_score) return "font-semibold";

  const homeWon = match.home_score > match.away_score;
  const teamWon = side === "home" ? homeWon : !homeWon;
  return teamWon ? "font-bold" : "font-semibold";
};

const fetchCompetitionStandings = async (competition: Competition) => {
  loadingByLeague.value[competition.slug] = true;
  errorsByLeague.value[competition.slug] = "";

  try {
    const response = await getLeagueStandings({
      league: competition.slug,
      season: season.value,
    });

    standingsByLeague.value[competition.slug] = (
      response.data.standings || []
    ).slice(0, 5);
  } catch (requestError) {
    console.error(requestError);
    standingsByLeague.value[competition.slug] = [];
    errorsByLeague.value[competition.slug] = "Unable to load this table.";
  } finally {
    loadingByLeague.value[competition.slug] = false;
  }
};

const fetchHomeFeed = async () => {
  feedLoading.value = true;
  feedError.value = "";

  try {
    const response = await getHomeMatchFeed({ season: season.value });
    upcomingMatches.value = response.data.upcoming || [];
    recentResults.value = response.data.recent_results || [];
  } catch (requestError) {
    console.error(requestError);
    upcomingMatches.value = [];
    recentResults.value = [];
    feedError.value = "Unable to load fixtures and results.";
  } finally {
    feedLoading.value = false;
  }
};

onMounted(() => {
  competitions.forEach(fetchCompetitionStandings);
  fetchHomeFeed();
});

watch(season, () => {
  competitions.forEach(fetchCompetitionStandings);
  fetchHomeFeed();
});
</script>
