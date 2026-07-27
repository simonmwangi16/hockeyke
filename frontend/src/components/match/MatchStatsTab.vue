<template>
  <div>
    <div v-if="loading" class="text-sm text-gray-500">
      Loading team stats...
    </div>

    <div v-else-if="error" class="text-sm text-red-500">
      {{ error }}
    </div>

    <div v-else-if="stats" class="rounded-xl border border-gray-800 bg-gray-900/40 p-5">
      <div class="mb-6 grid grid-cols-3 items-center">
        <div class="text-left text-base font-bold text-white">
          {{ stats.home_team.team }}
        </div>

        <div class="text-center text-sm font-semibold text-gray-400">
          Season Stats
        </div>

        <div class="text-right text-base font-bold text-white">
          {{ stats.away_team.team }}
        </div>
      </div>

      <StatCompareRow label="Played" :home="stats.home_team.played" :away="stats.away_team.played" />
      <StatCompareRow label="Wins" :home="stats.home_team.won" :away="stats.away_team.won" />
      <StatCompareRow label="Draws" :home="stats.home_team.drawn" :away="stats.away_team.drawn" />
      <StatCompareRow label="Losses" :home="stats.home_team.lost" :away="stats.away_team.lost" />
      <StatCompareRow label="Goals For" :home="stats.home_team.goals_for" :away="stats.away_team.goals_for" />
      <StatCompareRow label="Goals Against" :home="stats.home_team.goals_against" :away="stats.away_team.goals_against" />
      <StatCompareRow label="Goal Difference" :home="stats.home_team.goal_difference" :away="stats.away_team.goal_difference" />
      <StatCompareRow label="Points" :home="stats.home_team.points" :away="stats.away_team.points" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { getMatchTeamStats } from "@/services/leagueApi";
import StatCompareRow from "./StatCompareRow.vue";

const props = defineProps({
  matchId: {
    type: [String, Number],
    required: true,
  },
});

const stats = ref(null);
const loading = ref(false);
const error = ref("");

const fetchStats = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await getMatchTeamStats(props.matchId);
    stats.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = "Unable to load team stats.";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchStats);
</script>