<template>
  <div>
    <h2 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">
      League Table
    </h2>

    <div v-if="loading" class="text-sm text-gray-500">
      Loading standings...
    </div>

    <div v-else-if="error" class="text-sm text-red-500">
      {{ error }}
    </div>

    <div v-else class="overflow-hidden rounded-xl border border-gray-200 dark:border-gray-800">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
        <thead class="bg-gray-50 dark:bg-gray-900">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500">#</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500">Team</th>
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500">P</th>
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500">W</th>
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500">D</th>
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500">L</th>
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500">GD</th>
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500">Pts</th>
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500">Form</th>
          </tr>
        </thead>

        <tbody class="divide-y text-white dark:divide-gray-800 dark:bg-white/[0.03]">
          <tr
            v-for="team in standings"
            :key="team.team_id || team.team"
            class="transition-colors hover:bg-gray-600/30"
            :class="team.is_profile_team ? 'bg-brand-500/15 dark:bg-brand-500/20' : ''"
          >
            <td class="px-4 py-3 text-sm text-gray-500">
              {{ team.position }}
            </td>

            <td
              class="px-4 py-3 text-sm font-medium"
              :class="team.is_profile_team ? 'text-white font-bold' : 'text-gray-900 dark:text-white'"
            >
              <RouterLink
                    :to="`/teams/${team.team_id}/${makeTeamSlug(team.team)}`"
                    class="text-sm font-medium text-gray-900 hover:text-brand-500 hover:underline dark:text-white"
                >
                    {{ team.short_name || team.team }}
              </RouterLink>
            </td>

            <td class="px-4 py-3 text-center text-sm">{{ team.played }}</td>
            <td class="px-4 py-3 text-center text-sm">{{ team.won }}</td>
            <td class="px-4 py-3 text-center text-sm">{{ team.drawn }}</td>
            <td class="px-4 py-3 text-center text-sm">{{ team.lost }}</td>
            <td class="px-4 py-3 text-center text-sm">{{ team.goal_difference }}</td>
            <td class="px-4 py-3 text-center text-sm font-semibold">{{ team.points }}</td>

            <td class="px-4 py-3">
              <div class="flex justify-center gap-1">
                <span
                  v-for="(result, index) in team.form"
                  :key="index"
                  class="flex h-6 w-6 items-center justify-center rounded-md text-[12px] font-bold text-white"
                  :class="{
                    'bg-green-500': result === 'W',
                    'bg-yellow-500 text-black': result === 'D',
                    'bg-red-500': result === 'L',
                  }"
                >
                  {{ result }}
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div
        v-if="standings.length === 0"
        class="px-4 py-6 text-center text-sm text-gray-500 dark:text-gray-400"
      >
        No standings available.
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { getTeamTable } from "@/services/teamApi";

const props = defineProps({
  teamId: {
    type: [String, Number],
    required: true,
  },
});

const standings = ref([]);
const loading = ref(false);
const error = ref("");

const makeTeamSlug = (name) => {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
};

const fetchStandings = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await getTeamTable(props.teamId);
    standings.value = response.data.standings || [];
  } catch (err) {
    error.value = "Unable to load league table.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchStandings);

watch(
  () => props.teamId,
  fetchStandings
);
</script>