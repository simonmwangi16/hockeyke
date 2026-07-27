<template>
  <div ref="searchContainer" class="relative hidden lg:block">
    <form role="search" @submit.prevent="openSelectedResult">
      <div class="relative">
        <span
          class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2"
          aria-hidden="true"
        >
          <svg
            class="fill-gray-500 dark:fill-gray-400"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M3.04175 9.37363C3.04175 5.87693 5.87711 3.04199 9.37508 3.04199C12.8731 3.04199 15.7084 5.87693 15.7084 9.37363C15.7084 12.8703 12.8731 15.7053 9.37508 15.7053C5.87711 15.7053 3.04175 12.8703 3.04175 9.37363ZM9.37508 1.54199C5.04902 1.54199 1.54175 5.04817 1.54175 9.37363C1.54175 13.6991 5.04902 17.2053 9.37508 17.2053C11.2674 17.2053 13.003 16.5344 14.357 15.4176L17.177 18.238C17.4699 18.5309 17.9448 18.5309 18.2377 18.238C18.5306 17.9451 18.5306 17.4703 18.2377 17.1774L15.418 14.3573C16.5365 13.0033 17.2084 11.2669 17.2084 9.37363C17.2084 5.04817 13.7011 1.54199 9.37508 1.54199Z"
            />
          </svg>
        </span>

        <input
          ref="searchInput"
          v-model="query"
          type="search"
          role="combobox"
          autocomplete="off"
          aria-label="Search teams, matches, seasons and competitions"
          aria-controls="global-search-results"
          :aria-expanded="isOpen"
          :aria-activedescendant="activeResultId"
          placeholder="Search teams, matches, seasons..."
          class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-200 bg-transparent py-2.5 pl-12 pr-12 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-800 dark:bg-gray-900 dark:bg-white/[0.03] dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800 xl:w-[430px]"
          @focus="handleFocus"
          @keydown.down.prevent="moveSelection(1)"
          @keydown.up.prevent="moveSelection(-1)"
          @keydown.esc="closeResults"
        />

        <button
          v-if="query"
          type="button"
          aria-label="Clear search"
          class="absolute right-3 top-1/2 -translate-y-1/2 rounded p-1 text-gray-400 hover:text-gray-700 focus:outline-hidden focus:ring-2 focus:ring-brand-500 dark:hover:text-white"
          @click="clearSearch"
        >
          <span aria-hidden="true">×</span>
        </button>
      </div>
    </form>

    <div
      v-if="isOpen"
      id="global-search-results"
      role="listbox"
      class="absolute left-0 right-0 z-50 mt-2 max-h-[28rem] overflow-y-auto rounded-xl border border-gray-200 bg-white p-2 shadow-theme-lg dark:border-gray-800 dark:bg-gray-900"
    >
      <p v-if="loading" class="px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
        Searching…
      </p>
      <p v-else-if="error" class="px-3 py-4 text-sm text-error-500">
        {{ error }}
      </p>
      <p
        v-else-if="query.trim().length >= 2 && results.length === 0"
        class="px-3 py-4 text-sm text-gray-500 dark:text-gray-400"
      >
        No competition data found for “{{ query.trim() }}”.
      </p>

      <button
        v-for="(result, index) in results"
        :id="resultId(index)"
        :key="`${result.type}-${result.id}`"
        type="button"
        role="option"
        :aria-selected="index === selectedIndex"
        class="flex w-full items-start gap-3 rounded-lg px-3 py-2.5 text-left transition"
        :class="
          index === selectedIndex
            ? 'bg-brand-50 dark:bg-brand-500/10'
            : 'hover:bg-gray-50 dark:hover:bg-white/[0.04]'
        "
        @mouseenter="selectedIndex = index"
        @click="openResult(result)"
      >
        <span
          class="mt-0.5 rounded-md bg-gray-100 px-2 py-1 text-[10px] font-semibold uppercase tracking-wide text-gray-600 dark:bg-gray-800 dark:text-gray-300"
        >
          {{ result.type }}
        </span>
        <span class="min-w-0">
          <span class="block truncate text-sm font-medium text-gray-900 dark:text-white">
            {{ result.title }}
          </span>
          <span class="block truncate text-xs text-gray-500 dark:text-gray-400">
            {{ result.subtitle }}
          </span>
        </span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";

// @ts-expect-error The existing JavaScript API service convention has no declaration files.
import { searchCompetitionData } from "@/services/searchApi";

interface SearchResult {
  type: "team" | "match" | "season" | "competition";
  id: number;
  title: string;
  subtitle: string;
  url: string;
}

const router = useRouter();
const searchContainer = ref<HTMLElement | null>(null);
const searchInput = ref<HTMLInputElement | null>(null);
const query = ref("");
const results = ref<SearchResult[]>([]);
const loading = ref(false);
const error = ref("");
const isOpen = ref(false);
const selectedIndex = ref(-1);
let debounceTimer: ReturnType<typeof setTimeout> | undefined;
let requestSequence = 0;

const resultId = (index: number) => `global-search-result-${index}`;
const activeResultId = computed(() =>
  selectedIndex.value >= 0 ? resultId(selectedIndex.value) : undefined,
);

const closeResults = () => {
  isOpen.value = false;
  selectedIndex.value = -1;
};

const clearSearch = () => {
  query.value = "";
  results.value = [];
  error.value = "";
  closeResults();
  searchInput.value?.focus();
};

const openResult = async (result: SearchResult) => {
  closeResults();
  await router.push(result.url);
  query.value = "";
};

const openSelectedResult = () => {
  const result = results.value[selectedIndex.value] || results.value[0];
  if (result) {
    void openResult(result);
  }
};

const moveSelection = (direction: number) => {
  if (!results.value.length) return;
  isOpen.value = true;
  selectedIndex.value =
    (selectedIndex.value + direction + results.value.length) % results.value.length;
};

const handleFocus = () => {
  if (query.value.trim().length >= 2) {
    isOpen.value = true;
  }
};

const handleOutsideClick = (event: MouseEvent) => {
  if (!searchContainer.value?.contains(event.target as Node)) {
    closeResults();
  }
};

watch(query, (value) => {
  window.clearTimeout(debounceTimer);
  const trimmedQuery = value.trim();

  if (trimmedQuery.length < 2) {
    requestSequence += 1;
    results.value = [];
    loading.value = false;
    error.value = "";
    closeResults();
    return;
  }

  isOpen.value = true;
  loading.value = true;
  error.value = "";
  selectedIndex.value = -1;
  const sequence = ++requestSequence;

  debounceTimer = window.setTimeout(async () => {
    try {
      const response = await searchCompetitionData(trimmedQuery);
      if (sequence !== requestSequence) return;
      results.value = response.data.results || [];
      selectedIndex.value = results.value.length ? 0 : -1;
    } catch (requestError) {
      if (sequence !== requestSequence) return;
      console.error(requestError);
      results.value = [];
      error.value = "Search is temporarily unavailable.";
    } finally {
      if (sequence === requestSequence) {
        loading.value = false;
      }
    }
  }, 250);
});

onMounted(() => {
  document.addEventListener("mousedown", handleOutsideClick);
});

onBeforeUnmount(() => {
  window.clearTimeout(debounceTimer);
  document.removeEventListener("mousedown", handleOutsideClick);
});
</script>
