<template>
  <div class="border-t border-gray-800/80 py-5 first:border-t-0 first:pt-0 last:pb-0">
    <div class="mb-3 grid grid-cols-3 items-center text-sm">
      <div class="font-bold text-white">
        {{ home }}
      </div>

      <div class="text-center text-gray-400">
        {{ label }}
      </div>

      <div class="text-right font-bold text-white">
        {{ away }}
      </div>
    </div>

    <div class="grid grid-cols-[1fr_16px_1fr] items-center">
      <div class="h-3 overflow-hidden rounded-l-full bg-gray-800">
        <div
          class="ml-auto h-full rounded-l-full bg-blue-500"
          :style="{ width: homeWidth + '%' }"
        ></div>
      </div>

      <div></div>

      <div class="h-3 overflow-hidden rounded-r-full bg-gray-800">
        <div
          class="h-full rounded-r-full bg-orange-500"
          :style="{ width: awayWidth + '%' }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  label: String,
  home: { type: Number, default: 0 },
  away: { type: Number, default: 0 },
});

const total = computed(() => props.home + props.away || 1);
const homeWidth = computed(() => (props.home / total.value) * 100);
const awayWidth = computed(() => (props.away / total.value) * 100);
</script>