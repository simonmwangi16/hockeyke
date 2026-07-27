<template>
  <div class="min-h-screen xl:flex">
    <app-sidebar />
    <Backdrop />
    <div
      class="flex min-h-screen flex-1 flex-col transition-all duration-300 ease-in-out"
      :class="[isExpanded || isHovered ? 'lg:ml-[290px]' : 'lg:ml-[90px]']"
    >
      <app-header />
      <main class="mx-auto w-full max-w-(--breakpoint-2xl) flex-1 p-4 md:p-6">
        <slot></slot>
      </main>
      <div class="mx-auto w-full max-w-(--breakpoint-2xl) px-4 pb-6 md:px-6">
        <AdSenseUnit :slot-id="footerSlotId" />
      </div>
      <AppFooter />
    </div>
  </div>
</template>

<script setup lang="ts">
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'
import AdSenseUnit from '@/components/ads/AdSenseUnit.vue'
import { useSidebar } from '@/composables/useSidebar'
import Backdrop from './Backdrop.vue'
const { isExpanded, isHovered } = useSidebar()
const footerSlotId = import.meta.env.VITE_ADSENSE_FOOTER_SLOT?.trim() || ''
</script>
