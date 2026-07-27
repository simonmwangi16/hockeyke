<template>
  <AdminLayout>
    <div v-if="loading" class="text-sm text-gray-500">
      Loading match...
    </div>

    <div v-else-if="!match" class="text-sm text-red-500">
      Match not found.
    </div>

    <template v-else>
      <!-- Overview Card -->
      <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
        <div class="flex items-center justify-between border-b border-gray-200 px-5 py-4 dark:border-gray-800">
          <button
            @click="router.back()"
            class="flex items-center gap-2 rounded-full bg-white px-3 py-2 text-sm font-medium text-gray-900 transition hover:bg-gray-200 dark:bg-white dark:text-indigo-900"
            >
            <svg
                class="h-5 w-5"
                viewBox="0 0 24 25"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M10.2829 5.80707C10.5632 5.92312 10.746 6.19663 10.746 6.50002V11.7466V13.2466L10.746 18.5C10.746 18.8034 10.5632 19.0769 10.2829 19.193C10.0026 19.309 9.67994 19.2448 9.46548 19.0302L3.46949 13.03C3.32276 12.8831 3.24959 12.6906 3.25 12.4982V12.4966C3.25 12.2685 3.35184 12.0642 3.51254 11.9266L9.4655 5.96986C9.67996 5.75526 10.0026 5.69101 10.2829 5.80707Z"
                fill="currentColor"
                />

                <path
                opacity="0.4"
                d="M10.7461 13.2466L20.0015 13.2466C20.4157 13.2466 20.7515 12.9108 20.7515 12.4966C20.7515 12.0824 20.4157 11.7466L10.7461 11.7466V13.2466Z"
                fill="currentColor"
                />
            </svg>

            <span>Matches</span>
          </button>

          <div class="text-center">
            <p class="text-lg font-semibold text-gray-900 dark:text-white">
              {{ match.league_name || match.league || "Match" }}
            </p>
            <p class="text-xs text-gray-500">
              {{ match.season }}
            </p>
          </div>

          <div class="w-20"></div>
        </div>

        <div class="border-b border-gray-200 px-5 py-4 text-center text-sm text-gray-300 dark:border-gray-800">
          <span>{{ match.match_date }}</span>
          <span class="mx-2">•</span>
          <span>{{ match.match_time || "TBC" }}</span>
        </div>

        <div class="grid grid-cols-3 items-center gap-4 px-5 py-10">
          <div class="text-center">
            <p class="text-lg font-semibold text-gray-900 dark:text-white">
              {{ match.home_team }}
            </p>
          </div>

          <div class="text-center">
            <div v-if="isPlayed" class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ match.home_score }} - {{ match.away_score }}
            </div>

            <div v-else class="text-xl font-bold text-gray-900 dark:text-white">
              {{ match.match_time || "TBC" }}
            </div>

            <p class="mt-1 text-sm text-gray-300">
              {{ isPlayed ? "Full Time" : "Fixture" }}
            </p>
          </div>

          <div class="text-center">
            <p class="text-lg font-semibold text-gray-900 dark:text-white">
              {{ match.away_team }}
            </p>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="mt-6 rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
        <div class="border-b border-gray-200 dark:border-gray-800">
          <nav class="flex overflow-x-auto">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              class="whitespace-nowrap border-b-2 px-5 py-3 text-sm font-medium"
              :class="
                activeTab === tab.id
                  ? 'border-brand-500 text-brand-500'
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400'
              "
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>

        <div class="p-5">
          <MatchFormTab
            v-if="activeTab === 'form'"
            :matchId="route.params.id"
          />

          <MatchLeagueTableTab
            v-else-if="activeTab === 'table'"
            :matchId="route.params.id"
          />

          <MatchHeadToHeadTab
            v-else-if="activeTab === 'h2h'"
            :matchId="route.params.id"
           />

          <MatchStatsTab
            v-else-if="activeTab === 'stats'"
            :matchId="route.params.id"
          />
        </div>
      </div>
    </template>
  </AdminLayout>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import AdminLayout from "@/components/layout/AdminLayout.vue";
import MatchFormTab from "@/components/match/MatchFormTab.vue";
import MatchLeagueTableTab from "@/components/match/MatchLeagueTableTab.vue";
import MatchHeadToHeadTab from "@/components/match/MatchHeadToHeadTab.vue";
import MatchStatsTab from "@/components/match/MatchStatsTab.vue";
import { getMatchDetail } from "@/services/leagueApi";
import { makeMatchSlug } from "@/utils/slugs";

const route = useRoute();
const router = useRouter();

const match = ref(null);
const loading = ref(false);

const tabs = [
  { id: "form", label: "Form" },
  { id: "table", label: "League Table" },
  { id: "h2h", label: "H2H" },
  { id: "stats", label: "Stats" },
];

const activeTab = ref("form");

const isPlayed = computed(() => {
  return match.value?.home_score !== null && match.value?.away_score !== null;
});

const fetchMatch = async () => {
  loading.value = true;

  try {
    const response = await getMatchDetail(route.params.id);
    match.value = response.data.match || response.data;

    const expectedSlug = makeMatchSlug(
      match.value.home_team,
      match.value.away_team
    );

    if (route.params.slug !== expectedSlug) {
      router.replace({
        name: "MatchDetail",
        params: {
          id: match.value.id,
          slug: expectedSlug,
        },
      });
    }
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchMatch);
</script>