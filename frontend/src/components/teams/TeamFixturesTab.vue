<template>
  <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03]">
    <h3 class="mb-4 text-sm font-bold text-gray-900 dark:text-white">
      Fixtures & Results
    </h3>

    <div v-if="loading" class="text-sm text-gray-500 dark:text-gray-400">
      Loading matches...
    </div>

    <div v-else-if="matches.length === 0" class="text-sm text-gray-500 dark:text-gray-400">
      No matches available.
    </div>

    <div v-else class="space-y-4">
      <MatchMiniCard
        v-for="match in matches"
        :key="match.id"
        :match="match"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { getTeamMatches } from "@/services/teamApi";
import MatchMiniCard from "./MatchMiniCard.vue";

const props = defineProps({
  teamId: {
    type: [String, Number],
    required: true,
  },
});

const loading = ref(false);
const matches = ref([]);

const fetchMatches = async () => {
  loading.value = true;

  try {
    const response = await getTeamMatches(props.teamId);
    matches.value = response.data.matches || [];
  } finally {
    loading.value = false;
  }
};

onMounted(fetchMatches);
</script>