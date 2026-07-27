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
            <th class="hidden md:table-cell px-4 py-3 text-center text-xs font-medium text-gray-500">W</th>
            <th class="hidden md:table-cell px-4 py-3 text-center text-xs font-medium text-gray-500">D</th>
            <th class="hidden md:table-cell px-4 py-3 text-center text-xs font-medium text-gray-500">L</th>
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500">GD</th>
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500">Pts</th>
            <th class="hidden md:table-cell px-4 py-3 text-center text-xs font-medium text-gray-500">Form</th>
          </tr>
        </thead>

        <tbody class="divide-y text-white dark:divide-gray-800 dark:bg-white/[0.03]">
          <tr v-for="(team, index) in standings" :key="team.team_id || team.team" class="transition-colors hover:bg-gray-600/30">
            <td class="px-4 py-3 text-sm text-gray-500">{{ index + 1 }}</td>
            <td class="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">
              <RouterLink
                :to="`/teams/${team.team_id}/${makeTeamSlug(team.team)}`"
                class="hover:underline"
              >
                {{ team.short_name }}
              </RouterLink>
            </td>
            <td class="px-4 py-3 text-center text-sm">{{ team.played }}</td>
            <td class="hidden md:table-cell px-4 py-3 text-center text-sm">{{ team.won }}</td>
            <td class="hidden md:table-cell px-4 py-3 text-center text-sm">{{ team.drawn }}</td>
            <td class="hidden md:table-cell px-4 py-3 text-center text-sm">{{ team.lost }}</td>
            <td class="px-4 py-3 text-center text-sm">{{ team.goal_difference }}</td>
            <td class="px-4 py-3 text-center text-sm font-semibold">{{ team.points }}</td>
            <td class="hidden md:table-cell">
                <div class="flex gap-1 justify-center">
                    <span
                    v-for="(result, index) in team.form"
                    :key="index"
                    class="flex h-6 w-6 items-center justify-center rounded-md text-[12px] font-bold text-white"
                    :class="{
                        'bg-green-500': result === 'W',
                        'bg-yellow-500': result === 'D',
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
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { getLeagueStandings } from "@/services/leagueApi";

const props = defineProps({
  leagueParams: {
    type: Object,
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
    const response = await getLeagueStandings(props.leagueParams);
    standings.value = response.data.standings;
  } catch (err) {
    error.value = "Unable to load league table.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchStandings);

watch(
  () => props.leagueParams,
  fetchStandings,
  { deep: true }
);
</script>