<template>
  <AdminLayout>
    <div class="space-y-6">
      <!-- Team Header -->
      <div
        class="rounded-2xl border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-white/[0.03]"
      >
        <div v-if="loading">
          <div class="text-sm text-gray-500 dark:text-gray-400">
            Loading team...
          </div>
        </div>

        <template v-else-if="team">
          <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
                {{ team.name }}
              </h1>

              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                {{ overview?.league_season?.league }}
                •
                {{ overview?.league_season?.season }}
              </p>
            </div>
          </div>

        </template>
      </div>

      <!-- Tabs -->
      <div
        v-if="team"
        class="sticky top-[60px] z-30 -mx-5 border-b border-gray-200 bg-white/95 px-1 backdrop-blur before:absolute before:inset-x-0 before:-top-6 before:h-6 before:bg-white/95 dark:border-gray-800 dark:bg-gray-900/95 dark:before:bg-gray-900/95 lg:static lg:mx-0 lg:bg-transparent lg:px-0 lg:backdrop-blur-none lg:before:hidden lg:dark:bg-transparent"
      >
        <nav class="flex gap-2 overflow-x-auto" aria-label="Team profile sections">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            type="button"
            @click="activeTab = tab.key"
            class="whitespace-nowrap border-b-2 px-4 py-3 text-sm font-medium transition-colors"
            :class="
              activeTab === tab.key
                ? 'border-brand-500 text-brand-500'
                : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white'
            "
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>

      <AdSenseUnit :slot-id="teamAdSlotId" />

      <!-- Overview -->
      <TeamOverviewTab
        v-if="activeTab === 'overview'"
        :overview="overview"
      />

      <!-- League Table -->
      <TeamTableTab
        v-if="activeTab === 'table'"
        :team-id="teamId"
      />

      <!-- Fixtures -->
      <TeamFixturesTab
        v-if="activeTab === 'fixtures'"
        :team-id="teamId"
      />

      <!-- Team Stats -->
      <TeamStatsTab
        v-if="activeTab === 'stats'"
        :team-id="teamId"
      />
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import AdminLayout from "@/components/layout/AdminLayout.vue";
import AdSenseUnit from "@/components/ads/AdSenseUnit.vue";

import TeamOverviewTab from "@/components/teams/TeamOverviewTab.vue";
import TeamTableTab from "@/components/teams/TeamTableTab.vue";
import TeamFixturesTab from "@/components/teams/TeamFixturesTab.vue";
import TeamStatsTab from "@/components/teams/TeamStatsTab.vue";

import { getTeamOverview } from "@/services/teamApi";

const route = useRoute();
const teamAdSlotId = import.meta.env.VITE_ADSENSE_TEAM_SLOT?.trim() || "";

const teamId = computed(() => route.params.teamId);

const loading = ref(false);
const overview = ref(null);
const team = ref(null);

const activeTab = ref("overview");

const tabs = [
  { key: "overview", label: "Overview" },
  { key: "table", label: "Table" },
  { key: "fixtures", label: "Fixtures" },
  { key: "stats", label: "Stats" },
];

const fetchTeam = async () => {
  loading.value = true;

  try {
    const response = await getTeamOverview(teamId.value);

    overview.value = response.data;
    team.value = response.data.team;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchTeam);

watch(
  () => route.params.teamId,
  () => {
    overview.value = null;
    team.value = null;
    activeTab.value = "overview";
    fetchTeam();
  }
);
</script>
