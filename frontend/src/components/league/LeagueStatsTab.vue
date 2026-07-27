<template>
  <div>
    <h2 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">
      Team Stats
    </h2>

    <div v-if="loading" class="text-sm text-gray-500">Loading stats...</div>
    <div v-else-if="error" class="text-sm text-red-500">{{ error }}</div>

    <div v-else class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
      <div
        v-for="card in statCards"
        :key="card.key"
        class="rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]"
      >
        <h3 class="mb-3 text-sm font-bold text-gray-900 dark:text-white">
          {{ card.title }}
        </h3>

        <div
          v-for="row in card.rows"
          :key="`${card.key}-${row.team_id}`"
          class="flex items-center justify-between border-b border-gray-100 py-2 last:border-0 dark:border-gray-800"
        >
          <div class="flex items-center gap-3">
            <span class="w-5 text-xs font-semibold text-gray-400">
              {{ row.rank }}
            </span>

            <span class="text-sm font-medium text-gray-900 dark:text-white">
              <RouterLink
                :to="`/teams/${row.team_id}/${makeTeamSlug(row.team)}`"
                class="text-sm font-medium text-gray-900 hover:text-brand-500 hover:underline dark:text-white"
              >
                {{ row.short_name || row.team }}
              </RouterLink>
            </span>
          </div>

          <span class="text-sm font-bold text-gray-900 dark:text-white">
            {{ row.value }}
          </span>
        </div>

        <div v-if="card.rows.length === 0" class="text-sm text-gray-500">
          No data available.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { getLeagueSeasonStats } from "@/services/leagueApi";

const props = defineProps({
  leagueParams: {
    type: Object,
    required: true,
  },
});

const stats = ref({});
const loading = ref(false);
const error = ref("");

const statCards = computed(() => [
  {
    key: "goals_scored",
    title: "Goals Scored",
    rows: stats.value.goals_scored || [],
  },
  {
    key: "goals_conceded",
    title: "Goals Conceded",
    rows: stats.value.goals_conceded || [],
  },
  {
    key: "clean_sheets",
    title: "Clean Sheets",
    rows: stats.value.clean_sheets || [],
  },
  {
    key: "longest_winning_streak",
    title: "Longest Winning Streak",
    rows: stats.value.longest_winning_streak || [],
  },
  {
    key: "longest_losing_streak",
    title: "Longest Losing Streak",
    rows: stats.value.longest_losing_streak || [],
  },
]);

const makeTeamSlug = (name) => {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
};

const fetchStats = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await getLeagueSeasonStats(props.leagueParams);
    stats.value = response.data.stats || {};
  } catch (err) {
    console.error(err);
    error.value = "Unable to load stats.";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchStats);

watch(
  () => props.leagueParams,
  fetchStats,
  { deep: true }
);
</script>