<template>
  <div>
    <h2 class="mb-4 text-lg font-semibold text-gray-900 dark:text-white">
      Fixtures & Results
    </h2>

    <div class="mb-4 flex items-center justify-between rounded-xl border border-gray-200 p-3 dark:border-gray-800 dark:bg-white/[0.03]">
      <button
        type="button"
        @click="previousMonth"
        class="rounded-xl pt-0 px-5 py-2 pb-1 text-2xl font-semibold text-white bg-gray-700 dark:hover:text-gray-700 dark:text-gray-300 dark:hover:bg-gray-300"
      >
        ‹
      </button>

      <div class="text-md font-bold text-white dark:text-gray-100">
        {{ monthLabel }}
      </div>

      <button
        type="button"
        @click="nextMonth"
        class="rounded-xl pt-0 px-5 py-2 pb-1 text-2xl font-semibold text-white bg-gray-700 dark:hover:text-gray-700 dark:text-gray-300 dark:hover:bg-gray-300"
      >
        ›
      </button>
    </div>

    <div v-if="loading" class="text-sm text-gray-500">Loading fixtures...</div>
    <div v-else-if="error" class="text-sm text-red-500">{{ error }}</div>

    <div v-else-if="fixtures.length === 0" class="text-sm text-gray-500">
      No fixtures available for {{ monthLabel }}.
    </div>

    <div v-else class="space-y-6">
        <div
            v-for="(matches, date) in groupedFixtures"
            :key="date"
            class="overflow-hidden rounded-xl border border-gray-800 bg-gray-900/40"
        >
            <!-- Date Header -->
            <div
            class="border-b border-gray-800 bg-gray-800/50 px-4 py-3 text-center text-sm font-bold text-white"
            >
            {{ date }}
            </div>

            <!-- Matches -->
           
            <router-link
              v-for="match in matches"
              :key="match.id"
              :to="{
                name: 'MatchDetail',
                params: {
                  id: match.id,
                  slug: makeMatchSlug(match.home_team, match.away_team)
                }
              }"
              class="block border-b border-gray-800 px-4 py-4 last:border-b-0 transition-colors hover:bg-gray-800/30"
            >
                <div class="flex items-center justify-between gap-4">
                    <div
                        class="flex-1 text-right text-sm text-white"
                        :class="match.home_score > match.away_score ? 'font-bold' : 'font-medium'"
                    >
                        {{ match.home_team }}
                    </div>

                    <div class="min-w-[90px] text-center text-xs font-semibold text-gray-400">
                        <template v-if="match.status === 'SCHEDULED'">
                        <div class="text-sm font-bold text-white">
                            {{ match.match_time || 'TBC' }}
                        </div>
                        <div class="text-xs">
                            {{ match.venue || 'Venue TBC' }}
                        </div>
                        </template>

                        <template v-else-if="match.status === 'FT'">
                        <div
                            class="inline-flex rounded-lg bg-gray-700 px-3 py-2 text-sm font-bold text-white"
                        >
                            {{ match.home_score }} - {{ match.away_score }}
                        </div>
                        </template>

                        <template v-else-if="match.status === 'POSTPONED'">
                        <div
                            class="inline-flex rounded-lg bg-amber-900/30 px-3 py-2 text-xs font-bold uppercase text-amber-400"
                        >
                            Postponed
                        </div>
                        </template>

                        <template v-else-if="match.status === 'CANCELLED'">
                        <div
                            class="inline-flex rounded-lg bg-red-900/30 px-3 py-2 text-xs font-bold uppercase text-red-400"
                        >
                            Cancelled
                        </div>
                        </template>
                    </div>

                    <div
                        class="flex-1 text-left text-sm text-white"
                        :class="match.away_score > match.home_score ? 'font-bold' : 'font-medium'"
                    >
                        {{ match.away_team }}
                    </div>
                </div>
              </router-link>
      </div>
        
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { getLeagueFixtures } from "@/services/leagueApi";
import { makeMatchSlug } from "@/utils/slugs";

const props = defineProps({
  leagueParams: {
    type: Object,
    required: true,
  },
});

const fixtures = ref([]);
const loading = ref(false);
const error = ref("");

const selectedYear = ref(null);
const selectedMonth = ref(null);

const monthLabel = computed(() => {
  if (!selectedYear.value || !selectedMonth.value) return "Fixtures";

  const date = new Date(selectedYear.value, selectedMonth.value - 1, 1);

  return date.toLocaleString("en-US", {
    month: "long",
    year: "numeric",
  });
});

const fetchFixtures = async () => {
  loading.value = true;
  error.value = "";

  try {
    const params = {
      ...props.leagueParams,
    };

    if (selectedYear.value && selectedMonth.value) {
      params.year = selectedYear.value;
      params.month = selectedMonth.value;
    }

    const response = await getLeagueFixtures(params);

    fixtures.value = response.data.matches || [];
    selectedYear.value = response.data.year;
    selectedMonth.value = response.data.month;
  } catch (err) {
    console.error(err);
    error.value = "Unable to load fixtures.";
  } finally {
    loading.value = false;
  }
};

const groupedFixtures = computed(() => {
  return fixtures.value.reduce((groups, match) => {
    const date = match.match_date;

    if (!groups[date]) {
      groups[date] = [];
    }

    groups[date].push(match);
    return groups;
  }, {});
});

const previousMonth = () => {
  const date = new Date(selectedYear.value, selectedMonth.value - 2, 1);

  selectedYear.value = date.getFullYear();
  selectedMonth.value = date.getMonth() + 1;

  fetchFixtures();
};

const nextMonth = () => {
  const date = new Date(selectedYear.value, selectedMonth.value, 1);

  selectedYear.value = date.getFullYear();
  selectedMonth.value = date.getMonth() + 1;

  fetchFixtures();
};

onMounted(fetchFixtures);

watch(
  () => props.leagueParams,
  () => {
    selectedYear.value = null;
    selectedMonth.value = null;
    fetchFixtures();
  },
  { deep: true }
);
</script>