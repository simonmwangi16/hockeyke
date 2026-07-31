<template>
  <AdminLayout>
    <article
      class="rounded-2xl border border-gray-200 bg-white px-5 py-7 dark:border-gray-800 dark:bg-white/[0.03] md:px-8 md:py-10"
    >
      <div class="max-w-3xl">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Contact HockeyKE</h1>
        <p class="mt-4 text-base leading-7 text-gray-600 dark:text-gray-300">
          Contact us to report an incorrect fixture, result or team detail, or to share feedback
          about the platform.
        </p>

        <div
          class="mt-8 rounded-xl border border-gray-200 bg-gray-50 p-5 dark:border-gray-800 dark:bg-gray-900"
        >
          <h2 class="text-sm font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
            Email
          </h2>
          <a
            href="mailto:hockeyke@gmail.com"
            class="mt-2 inline-flex text-base font-semibold text-brand-500 hover:text-brand-600 hover:underline"
          >
            hockeyke@gmail.com
          </a>
        </div>

        <p class="mt-6 text-sm leading-6 text-gray-500 dark:text-gray-400">
          When reporting a correction, include the competition, teams, match date and the
          information that should be reviewed.
        </p>
      </div>
    </article>
  </AdminLayout>
</template>

<script setup lang="ts">
import AdminLayout from "@/components/layout/AdminLayout.vue";
</script>
