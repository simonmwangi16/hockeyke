<template>
  <div>
    <div
      v-if="loading"
      class="text-sm text-gray-500"
    >
      Loading standings...
    </div>

    <div
      v-else
      class="overflow-hidden rounded-xl border border-gray-200 dark:border-gray-800"
    >
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
        <thead class="bg-gray-50 dark:bg-gray-900">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500">#</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500">Team</th>
            <th class="px-4 py-3 text-xs font-medium text-gray-500 text-center">P</th>
            <th class="hidden md:table-cell px-4 py-3 text-xs font-medium text-gray-500 text-center">W</th>
            <th class="hidden md:table-cell px-4 py-3 text-xs font-medium text-gray-500 text-center">D</th>
            <th class="hidden md:table-cell px-4 py-3 text-xs font-medium text-gray-500 text-center">L</th>
            <th class="px-4 py-3 text-xs font-medium text-gray-500 text-center">GD</th>
            <th class="px-4 py-3 text-xs font-medium text-gray-500 text-center">Pts</th>
          </tr>
        </thead>

        <tbody class="divide-y text-white dark:divide-gray-800 dark:bg-white/[0.03]">
          <tr
            v-for="team in standings"
            :key="team.team_id"
            :class="rowClass(team.team_id)"
          >
            <td class="px-4 py-3 text-sm">
              {{ team.position }}
            </td>

            <td class="px-4 py-3 font-medium text-sm">
              <router-link
                :to="{
                    name: 'TeamProfile',
                    params: {
                    teamId: team.team_id,
                    teamSlug: makeTeamSlug(team.team),
                    },
                }"
                class="hover:underline"
               >
                    {{ team.team }}
               </router-link>
            </td>

            <td class="px-4 py-3 text-center text-sm">{{ team.played }}</td>
            <td class="hidden md:table-cell px-4 py-3 text-center text-sm">{{ team.won }}</td>
            <td class="hidden md:table-cell px-4 py-3 text-center text-sm">{{ team.drawn }}</td>
            <td class="hidden md:table-cell px-4 py-3 text-center text-sm">{{ team.lost }}</td>
            <td class="px-4 py-3 text-center text-sm">{{ team.goal_difference }}</td>
            <td class="px-4 py-3 text-center text-sm font-bold">{{ team.points }}</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { getMatchLeagueTable } from "@/services/leagueApi";
import { makeTeamSlug } from "@/utils/slugs";

const props = defineProps({
  matchId: {
    type: [String, Number],
    required: true,
  },
});

const standings = ref([]);
const homeTeamId = ref(null);
const awayTeamId = ref(null);
const loading = ref(false);

const fetchTable = async () => {
  loading.value = true;

  try {
    const response = await getMatchLeagueTable(props.matchId);

    standings.value = response.data.standings;
    homeTeamId.value = response.data.home_team_id;
    awayTeamId.value = response.data.away_team_id;
  } finally {
    loading.value = false;
  }
};

const rowClass = (teamId) => {
  if (teamId === homeTeamId.value) {
    return " bg-brand-500/15 dark: bg-brand-500/15 font-bold";
  }

  if (teamId === awayTeamId.value) {
    return " bg-brand-500/15 dark: bg-brand-500/15 font-bold";
  }

  return "";
};

onMounted(fetchTable);
</script>