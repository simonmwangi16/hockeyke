<template>
  <div class="rounded-xl pb-4">
    <div class="mb-3 text-center text-xs font-semibold text-gray-500 dark:text-gray-400">
      {{ match.match_date }}
    </div>

    <div class="grid grid-cols-[1fr_auto_1fr] items-center gap-3">
      <div class="text-right text-sm font-semibold text-gray-900 dark:text-white">
        {{ match.home_short_name || match.home_team }}
      </div>

      <div class="min-w-[72px] text-center">
        <template v-if="match.status === 'FT'">
          <span
            class="inline-flex rounded-lg px-3 py-2 text-sm font-bold"
            :class="resultClass"
            >
            {{ match.home_score }} - {{ match.away_score }}
           </span>
        </template>

        <template v-else-if="match.status === 'SCHEDULED'">
          <div class="text-sm font-bold text-gray-900 dark:text-white">
            {{ match.match_time || "TBC" }}
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-400">
            {{ match.venue || "Venue TBC" }}
          </div>
        </template>

        <template v-else>
          <span class="rounded-lg bg-red-900/30 px-3 py-2 text-xs font-bold uppercase text-red-400">
            {{ match.status }}
          </span>
        </template>
      </div>

      <div class="text-left text-sm font-semibold text-gray-900 dark:text-white">
        {{ match.away_short_name || match.away_team }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  match: {
    type: Object,
    required: true,
  },
});

const resultClass = computed(() => {
  if (props.match.status !== "FT") {
    return "bg-gray-200 text-gray-900 dark:bg-gray-700 dark:text-white";
  }

  const isHome = props.match.is_home;

  const teamScore = isHome
    ? props.match.home_score
    : props.match.away_score;

  const opponentScore = isHome
    ? props.match.away_score
    : props.match.home_score;

  if (teamScore > opponentScore) {
    return "bg-green-600 text-white";
  }

  if (teamScore < opponentScore) {
    return "bg-red-600 text-white";
  }

  return "bg-gray-200 text-gray-900 dark:bg-gray-700 dark:text-white";
});
</script>