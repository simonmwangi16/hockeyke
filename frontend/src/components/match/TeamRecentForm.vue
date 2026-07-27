<template>
  <div class="rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
    <div class="border-b border-gray-200 px-4 py-3 dark:border-gray-800">
      <h3 class="text-sm font-semibold text-gray-900 dark:text-white">
        {{ team.name }} - Last 5 Matches
      </h3>
    </div>

    <div v-if="team.matches.length === 0" class="p-4 text-sm text-gray-500">
      No recent matches found.
    </div>

    <div v-else class="divide-y divide-gray-200 dark:divide-gray-800">
      <router-link
        v-for="match in team.matches"
        :key="match.id"
        :to="{
          name: 'MatchDetail',
          params: {
            id: match.id,
            slug: makeMatchSlug(
              match.home_team,
              match.away_team
            ),
          },
        }"
        class="block px-4 py-3 transition hover:bg-gray-100 dark:hover:bg-gray-700"
      >
        <div class="mb-2 flex items-center justify-between text-xs text-gray-400">
          <span>{{ match.match_date }}</span>

          <span
            class="inline-flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold text-white"
            :class="resultClass(match.result)"
          >
            {{ match.result }}
          </span>
        </div>

        <div class="flex items-center justify-between gap-3">
          <div
            class="flex-1 text-right text-sm text-gray-900 dark:text-white"
            :class="match.home_score > match.away_score ? 'font-bold' : 'font-medium'"
          >
            {{ match.home_team }}
          </div>

          <div class="min-w-[64px] rounded-lg bg-gray-100 px-3 py-2 text-center text-sm font-bold text-gray-900 dark:bg-gray-800 dark:text-white">
            {{ match.home_score }} - {{ match.away_score }}
          </div>

          <div
            class="flex-1 text-left text-sm text-gray-900 dark:text-white"
            :class="match.away_score > match.home_score ? 'font-bold' : 'font-medium'"
          >
            {{ match.away_team }}
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { makeMatchSlug } from "@/utils/slugs";

defineProps({
  team: {
    type: Object,
    required: true,
  },
});

const resultClass = (result) => {
  if (result === "W") return "bg-green-600";
  if (result === "D") return "bg-gray-500";
  if (result === "L") return "bg-red-600";
  return "bg-gray-400";
};
</script>