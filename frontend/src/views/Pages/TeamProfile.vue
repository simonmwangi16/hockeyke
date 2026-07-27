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

          <!-- Tabs -->
          <div
            class="mt-6 flex flex-wrap gap-6 border-b border-gray-200 dark:border-gray-800"
          >
            <button
              v-for="tab in tabs"
              :key="tab.key"
              @click="activeTab = tab.key"
              class="pb-3 text-sm font-medium transition-colors"
              :class="
                activeTab === tab.key
                  ? 'border-b-2 border-brand-500 text-brand-500'
                  : 'text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white'
              "
            >
              {{ tab.label }}
            </button>
          </div>
        </template>
      </div>

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

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";

import TeamOverviewTab from "@/components/teams/TeamOverviewTab.vue";
import TeamTableTab from "@/components/teams/TeamTableTab.vue";
import TeamFixturesTab from "@/components/teams/TeamFixturesTab.vue";
import TeamStatsTab from "@/components/teams/TeamStatsTab.vue";

import { getTeamOverview } from "@/services/teamApi";

const route = useRoute();

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