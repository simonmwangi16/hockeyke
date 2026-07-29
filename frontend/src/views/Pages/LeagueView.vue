<template>
  <AdminLayout>
    <div
      class="min-h-screen rounded-2xl border border-gray-200 bg-white px-5 py-7 dark:border-gray-800 dark:bg-white/[0.03] xl:px-10 xl:py-12"
    >
      <!-- League Header -->
      <div class="mb-6">     

        <h1 class="mt-1 text-2xl font-bold text-gray-900 dark:text-white">
          {{ leagueTitle }}
        </h1>
      </div>

      <!-- Tabs -->
      <div
        class="sticky top-[60px] z-30 -mx-5 border-b border-gray-200 bg-white/95 px-1 backdrop-blur before:absolute before:inset-x-0 before:-top-2 before:h-2 before:bg-white/95 dark:border-gray-800 dark:bg-gray-900/95 dark:before:bg-gray-900/95 lg:static lg:mx-0 lg:bg-transparent lg:px-0 lg:backdrop-blur-none lg:before:hidden lg:dark:bg-transparent"
      >
        <nav class="flex gap-2 overflow-x-auto">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="changeTab(tab.id)"
            :class="[
              'whitespace-nowrap border-b-2 px-4 py-3 text-sm font-medium transition-all duration-200 focus:outline-none',
              activeTab === tab.id
                ? 'border-brand-500 text-brand-500'
                : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200',
            ]"
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>

      <AdSenseUnit class="my-6" :slot-id="leagueAdSlotId" />

      <!-- Tab Content -->
      <div class="mt-6">
        <div v-if="activeTab === 'table'">
          <p class="text-sm text-gray-500 dark:text-gray-400">
            <LeagueTableTab
                v-if="activeTab === 'table'"
                :leagueParams="leagueParams"
            />
          </p>
        </div>

        <div v-else-if="activeTab === 'fixtures'">
          <p class="text-sm text-gray-500 dark:text-gray-400">
            <LeagueFixturesTab
                v-if="activeTab === 'fixtures'"
                :leagueParams="leagueParams"
            />
          </p>
        </div>

        <div v-else-if="activeTab === 'stats'">
          <p class="text-sm text-gray-500 dark:text-gray-400">
            <LeagueStatsTab
                v-if="activeTab === 'stats'"
                :leagueParams="leagueParams"
            />
          </p>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import AdminLayout from "@/components/layout/AdminLayout.vue";
import AdSenseUnit from "@/components/ads/AdSenseUnit.vue";
import LeagueTableTab from "@/components/league/LeagueTableTab.vue";
import LeagueFixturesTab from "@/components/league/LeagueFixturesTab.vue";
import LeagueStatsTab from "@/components/league/LeagueStatsTab.vue";

const route = useRoute();
const router = useRouter();
const leagueAdSlotId = import.meta.env.VITE_ADSENSE_LEAGUE_SLOT?.trim() || "";

const tabs = [
  { id: "table", label: "League Table" },
  { id: "fixtures", label: "Fixtures" },
  { id: "stats", label: "Team Stats" },
];

const activeTab = ref(route.query.tab || "table");

watch(
  () => route.query.tab,
  (newTab) => {
    activeTab.value = newTab || "table";
  }
);

const cleanLabel = (value: string | string[] | undefined) => {
  if (!value) return "";

  return value
    .toString()
    .replace(/-/g, " ")
    .replace(/\b\w/g, (char: string) => char.toUpperCase());
};

const leagueTitle = computed(() => {
  const gender = cleanLabel(route.params.gender);
  const competition = cleanLabel(route.params.competition);
  const division = cleanLabel(route.params.division);

  return [competition, gender, division].filter(Boolean).join(" - ");
});

const changeTab = (tabId: string) => {
  router.replace({
    path: route.path,
    query: {
      ...route.query,
      tab: tabId,
    },
  });
};

const leagueSlug = computed(() => {
  const gender = route.params.gender;
  const competition = route.params.competition;
  const division = route.params.division;

  if (competition === "premier-league") {
    return `premier-league-${gender}`;
  }

  if (competition === "national-league") {
    return division
      ? `national-league-${gender}-${division}`
      : `national-league-${gender}`;
  }

  if (competition === "super-league") {
    return division
      ? `super-league-${gender}-${division}`
      : `super-league-${gender}`;
  }

  return `${competition}-${gender}`;
});

const leagueParams = computed(() => ({
  league: leagueSlug.value,
  season: Array.isArray(route.query.season)
    ? route.query.season[0] || "2026"
    : route.query.season || "2026",
}));
</script>
