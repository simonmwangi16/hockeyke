<template>
  <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03]">
    <h3 class="mb-4 text-sm font-bold text-gray-900 dark:text-white">
      Team Stats
    </h3>

    <div v-if="loading" class="text-sm text-gray-500 dark:text-gray-400">
      Loading team stats...
    </div>

    <div v-else-if="!stats" class="text-sm text-gray-500 dark:text-gray-400">
      No team stats available.
    </div>

    <div v-else class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-5">
      <div
        v-for="item in statCards"
        :key="item.label"
        class="rounded-xl bg-gray-50 p-4 text-center dark:bg-gray-900/60"
      >
        <div class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ item.value }}
        </div>
        <div class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          {{ item.label }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { getTeamStats } from "@/services/teamApi";

const props = defineProps({
  teamId: {
    type: [String, Number],
    required: true,
  },
});

const loading = ref(false);
const stats = ref(null);

const statCards = computed(() => [
  { label: "Goals Scored", value: stats.value?.goals_scored ?? 0 },
  { label: "Goals Conceded", value: stats.value?.goals_conceded ?? 0 },
  { label: "Clean Sheets", value: stats.value?.clean_sheets ?? 0 },
  { label: "Longest Win Streak", value: stats.value?.longest_winning_streak ?? 0 },
  { label: "Longest Losing Streak", value: stats.value?.longest_losing_streak ?? 0 },
]);

const fetchStats = async () => {
  loading.value = true;

  try {
    const response = await getTeamStats(props.teamId);
    stats.value = response.data.stats;
  } finally {
    loading.value = false;
  }
};

onMounted(fetchStats);
</script>