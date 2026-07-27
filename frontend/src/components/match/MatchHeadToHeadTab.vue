<template>
  <div>

    <div v-if="loading" class="text-sm text-gray-500">
      Loading head-to-head...
    </div>

    <div v-else-if="error" class="text-sm text-red-500">
      {{ error }}
    </div>

    <div v-else-if="matches.length === 0" class="text-sm text-gray-500">
      No previous meetings found.
    </div>

    

    <div v-else class="overflow-hidden rounded-xl border border-gray-200 dark:border-gray-800">

        <div
        v-if="summary"
        class="mb-6 rounded-xl border border-gray-800 bg-gray-900/40 p-5"
        >
            <!-- Team Names -->
            <div class="mb-6 grid grid-cols-3 items-center">
                <div class="text-left text-base font-bold text-white">
                {{ summary.home_team }}
                </div>

                <div></div>

                <div class="text-right text-base font-bold text-white">
                {{ summary.away_team }}
                </div>
            </div>

            <!-- Wins / Draws / Wins -->
            <div class="mb-6">
                <div class="mb-3 grid grid-cols-3 items-center text-sm">
                <div class="text-center">
                    <div class="text-2xl font-bold text-blue-500">
                    {{ summary.home_wins }}
                    </div>
                    <div class="text-gray-400">Wins</div>
                </div>

                <div class="text-center">
                    <div class="text-2xl font-bold text-gray-300">
                    {{ summary.draws }}
                    </div>
                    <div class="text-gray-400">Draws</div>
                </div>

                <div class="text-center">
                    <div class="text-2xl font-bold text-orange-500">
                    {{ summary.away_wins }}
                    </div>
                    <div class="text-gray-400">Wins</div>
                </div>
                </div>

                <div class="grid grid-cols-[1fr_16px_1fr] items-center">
                <div class="h-3 overflow-hidden rounded-l-full bg-gray-800">
                    <div
                    class="ml-auto h-full rounded-l-full bg-blue-500"
                    :style="{ width: winsHomeWidth + '%' }"
                    ></div>
                </div>

                <div></div>

                <div class="h-3 overflow-hidden rounded-r-full bg-gray-800">
                    <div
                    class="h-full rounded-r-full bg-orange-500"
                    :style="{ width: winsAwayWidth + '%' }"
                    ></div>
                </div>
                </div>
            </div>

            <StatCompareRow
                label="Goals"
                :home="summary.home_goals"
                :away="summary.away_goals"
            />

            <StatCompareRow
                label="Clean Sheets"
                :home="summary.home_clean_sheets"
                :away="summary.away_clean_sheets"
            />
        </div>

      <router-link
        v-for="match in matches"
        :key="match.id"
        :to="{
            name: 'MatchDetail',
            params: {
            id: match.id,
            slug: makeMatchSlug(match.home_team, match.away_team),
            },
        }"
        class="grid grid-cols-[120px_1fr] items-center gap-4 border-b border-gray-200 px-4 py-4 last:border-b-0 transition hover:bg-gray-100 dark:border-gray-800 dark:hover:bg-indigo-950"
        >
        <!-- Date -->
        <div class="text-xs text-gray-500 dark:text-gray-400">
            {{ match.match_date }}
        </div>

        <!-- Match -->
        <div class="flex items-center justify-center gap-4">
            <div
            class="w-1/3 text-right text-sm text-gray-900 dark:text-white"
            :class="match.home_score > match.away_score ? 'font-bold' : 'font-medium'"
            >
            {{ match.home_short_name }}
            </div>

            <div class="min-w-[70px] text-center text-sm font-bold text-gray-900 dark:text-white">
            {{ match.home_score }} - {{ match.away_score }}
            </div>

            <div
            class="w-1/3 text-left text-sm text-gray-900 dark:text-white"
            :class="match.away_score > match.home_score ? 'font-bold' : 'font-medium'"
            >
            {{ match.away_short_name }}
            </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { getMatchHeadToHead } from "@/services/leagueApi";
import { makeMatchSlug } from "@/utils/slugs";
import StatCompareRow from "./StatCompareRow.vue";

const props = defineProps({
  matchId: {
    type: [String, Number],
    required: true,
  },
});

const matches = ref([]);
const loading = ref(false);
const error = ref("");
const summary = ref(null);

const winsTotal = computed(() => {
  if (!summary.value) return 1;
  return summary.value.home_wins + summary.value.away_wins || 1;
});

const winsHomeWidth = computed(() => {
  if (!summary.value) return 0;
  return (summary.value.home_wins / winsTotal.value) * 100;
});

const winsAwayWidth = computed(() => {
  if (!summary.value) return 0;
  return (summary.value.away_wins / winsTotal.value) * 100;
});

const fetchHeadToHead = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await getMatchHeadToHead(props.matchId);
    matches.value = response.data.matches || [];
    summary.value = response.data.summary || null;
  } catch (err) {
    console.error(err);
    error.value = "Unable to load head-to-head.";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchHeadToHead);
</script>