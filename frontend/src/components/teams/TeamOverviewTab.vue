<template>
  <div v-if="!overview" class="text-sm text-gray-500 dark:text-gray-400">
    No team overview available.
  </div>

  <div v-else class="space-y-6">
    <div class="grid grid-cols-1 gap-6 xl:grid-cols-3">
      <!-- Team Form -->
      <div
        class="flex h-full flex-col rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03]"
        >
            <h3 class="text-sm font-bold text-gray-900 dark:text-white">
                Team Form
            </h3>

            <div class="flex flex-1 items-center justify-center">
                <div v-if="overview.form?.length" class="flex items-center justify-center gap-4">
                <span
                    v-for="(result, index) in overview.form"
                    :key="index"
                    class="flex h-8 w-8 items-center justify-center rounded-md text-xs font-bold text-white"
                    :class="{
                    'bg-green-600': result === 'W',
                    'bg-yellow-500 text-black': result === 'D',
                    'bg-red-600': result === 'L',
                    }"
                >
                    {{ result }}
                </span>
                </div>
            </div>
        </div>

      <!-- Last Match -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03]">
        <h3 class="mb-4 text-sm font-bold text-gray-900 dark:text-white">
          Last Match
        </h3>

        <MatchMiniCard
          v-if="overview.last_match"
          :match="overview.last_match"
        />

        <div v-else class="text-sm text-gray-500 dark:text-gray-400">
          No previous match.
        </div>
      </div>

      <!-- Next Match -->
      <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03]">
        <h3 class="mb-4 text-sm font-bold text-gray-900 dark:text-white">
          Next Match
        </h3>

        <MatchMiniCard
          v-if="overview.next_match"
          :match="overview.next_match"
        />

        <div v-else class="text-sm text-gray-500 dark:text-gray-400">
          No upcoming match.
        </div>
      </div>
    </div>

    <!-- League Table Snapshot -->
    <div class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03]">
      <div class="mb-4">
        <h3 class="text-sm font-bold text-gray-900 dark:text-white">
          Standings
        </h3>
        <p class="text-xs text-gray-500 dark:text-gray-400">
          {{ overview.league_season?.league }} table snapshot
        </p>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200 text-left text-xs text-gray-500 dark:border-gray-800 dark:text-gray-400">
              <th class="px-3 py-3">#</th>
              <th class="px-3 py-3">Team</th>
              <th class="px-3 py-3 text-center">P</th>
              <th class="px-3 py-3 text-center">GD</th>
              <th class="px-3 py-3 text-right">PTS</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="row in overview.table_snapshot"
              :key="row.team_id"
              class="border-b border-gray-100 last:border-0 dark:border-gray-800"
              :class="row.is_profile_team ? ' bg-brand-500/15 text-white' : 'text-gray-900 dark:text-white'"
            >
              <td class="px-3 py-3 font-medium">{{ row.position }}</td>
              <td class="px-3 py-3 font-semibold">
                <RouterLink
                    :to="`/teams/${row.team_id}/${makeTeamSlug(row.team)}`"
                    class="text-sm font-medium text-gray-900 hover:text-brand-500 hover:underline dark:text-white"
                >
                    {{ row.short_name || row.team }}
                </RouterLink>
              </td>
              <td class="px-3 py-3 text-center">{{ row.played }}</td>
              <td class="px-3 py-3 text-center">{{ row.goal_difference }}</td>
              <td class="px-3 py-3 text-right font-bold">{{ row.points }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="!overview.table_snapshot?.length" class="text-sm text-gray-500 dark:text-gray-400">
        No table data available.
      </div>
    </div>
  </div>
</template>

<script setup>
import MatchMiniCard from "./MatchMiniCard.vue";

defineProps({
  overview: {
    type: Object,
    required: true,
  },
});

const makeTeamSlug = (name) => {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
};
</script>