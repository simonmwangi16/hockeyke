<template>
  <div class="grid grid-cols-1 gap-6 xl:grid-cols-2">
    <TeamRecentForm
      v-if="formData?.home_team"
      :team="formData.home_team"
    />

    <TeamRecentForm
      v-if="formData?.away_team"
      :team="formData.away_team"
    />

    <div v-if="loading" class="text-sm text-gray-500">
      Loading team form...
    </div>

    <div v-if="error" class="text-sm text-red-500">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { getMatchForm } from "@/services/leagueApi";
import TeamRecentForm from "./TeamRecentForm.vue";

const props = defineProps({
  matchId: {
    type: [String, Number],
    required: true,
  },
});

const formData = ref(null);
const loading = ref(false);
const error = ref("");

const fetchForm = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await getMatchForm(props.matchId);
    formData.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = "Unable to load team form.";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchForm);
</script>