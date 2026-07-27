<template>
  <router-link to="/" class="lg:hidden">
    <img
      class="h-auto w-[110px] dark:hidden"
      src="/images/logo/hke-logo-horizontal.png"
      alt="HockeyKE"
    />
    <img
      class="hidden h-auto w-[110px] dark:block"
      src="/images/logo/hke-logo-horizontal.png"
      alt="HockeyKE"
    />
  </router-link>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
