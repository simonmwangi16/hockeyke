<template>
  <AdminLayout>
    <div class="space-y-8">
      <section>
        <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
          <template
            v-for="(competition, competitionIndex) in competitions"
            :key="competition.slug"
          >
            <article
              class="flex min-h-[390px] flex-col rounded-2xl border border-gray-200 bg-white p-5 transition hover:border-brand-300 dark:border-gray-800 dark:bg-white/[0.03] dark:hover:border-brand-700"
            >
            <div>
              <div>
                <h2 class="text-base font-semibold text-gray-900 dark:text-white">
                  {{ competition.name }}
                </h2>
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

            <AdSenseUnit v-if="competitionIndex === 3" />
          </template>
        </div>
      </section>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import AdSenseUnit from "@/components/ads/AdSenseUnit.vue";
import AdminLayout from "@/components/layout/AdminLayout.vue";
// @ts-expect-error The existing JavaScript API service has no declaration file.
import { getLeagueStandings } from "@/services/leagueApi";
// @ts-expect-error The existing JavaScript slug utility has no declaration file.
import { makeTeamSlug } from "@/utils/slugs";

const season = "2026";

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

const fetchCompetitionStandings = async (competition: Competition) => {
  loadingByLeague.value[competition.slug] = true;
  errorsByLeague.value[competition.slug] = "";

  try {
    const response = await getLeagueStandings({
      league: competition.slug,
      season,
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

onMounted(() => {
  competitions.forEach(fetchCompetitionStandings);
});
</script>
