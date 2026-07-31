<template>
  <aside v-if="isConfigured" class="col-span-full py-2" aria-label="Advertisement">
    <p class="mb-2 text-center text-[10px] uppercase tracking-wider text-gray-400">
      Advertisement
    </p>
    <div
      class="min-h-[90px] overflow-hidden rounded-xl bg-gray-50 dark:bg-white/[0.02]"
    >
      <ins
        class="adsbygoogle block"
        style="display: block"
        :data-ad-client="clientId"
        :data-ad-slot="slotId"
        data-ad-format="auto"
        data-full-width-responsive="true"
      ></ins>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted } from "vue";

defineOptions({
  name: "AdSenseUnit",
});

declare global {
  interface Window {
    adsbygoogle?: Record<string, unknown>[];
  }
}

const props = defineProps<{
  slotId?: string;
}>();

const clientId = import.meta.env.VITE_ADSENSE_CLIENT_ID?.trim() || "";
const slotId = computed(
  () => props.slotId?.trim() || import.meta.env.VITE_ADSENSE_HOME_SLOT?.trim() || "",
);
const isConfigured = computed(() => Boolean(clientId && slotId.value));

const loadAdSenseScript = () => {
  const existingScript = document.querySelector<HTMLScriptElement>(
    'script[src^="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]',
  );

  if (existingScript) {
    return Promise.resolve();
  }

  return new Promise<void>((resolve, reject) => {
    const script = document.createElement("script");
    script.async = true;
    script.crossOrigin = "anonymous";
    script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${encodeURIComponent(clientId)}`;
    script.addEventListener("load", () => resolve(), { once: true });
    script.addEventListener("error", () => reject(new Error("Unable to load AdSense.")), {
      once: true,
    });
    document.head.appendChild(script);
  });
};

const initializeAd = async () => {
  if (!isConfigured.value) return;

  try {
    await loadAdSenseScript();
    await nextTick();
    window.adsbygoogle = window.adsbygoogle || [];
    window.adsbygoogle.push({});
  } catch (error) {
    console.error(error);
  }
};

onMounted(initializeAd);
</script>
