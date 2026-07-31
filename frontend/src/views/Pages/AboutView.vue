<template>
  <AdminLayout>
    <article
      class="rounded-2xl border border-gray-200 bg-white px-5 py-7 dark:border-gray-800 dark:bg-white/[0.03] md:px-8 md:py-10"
    >
      <div class="max-w-3xl">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">About HockeyKE</h1>
        <p class="mt-4 text-base leading-7 text-gray-600 dark:text-gray-300">
          HockeyKE is a dedicated platform for following Kenyan field hockey competitions. It
          brings fixtures, results, league tables and team statistics together in one accessible
          place.
        </p>

        <section class="mt-10">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">What we cover</h2>
          <p class="mt-3 leading-7 text-gray-600 dark:text-gray-300">
            The platform covers men's and women's Premier and Super League competitions, together
            with supported National League zones. Current and historical competition information
            is presented separately so that previous results remain available.
          </p>
        </section>

        <section class="mt-8">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Our purpose</h2>
          <p class="mt-3 leading-7 text-gray-600 dark:text-gray-300">
            HockeyKE is designed to make Kenyan hockey information easier to find on desktop and
            mobile devices. We aim to present schedules, scores and standings clearly while
            preserving the history of each competition.
          </p>
        </section>

        <section class="mt-8">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">
            Corrections and feedback
          </h2>
          <p class="mt-3 leading-7 text-gray-600 dark:text-gray-300">
            If you notice an incorrect fixture, result or team detail, please
            <RouterLink
              to="/contact"
              class="font-semibold text-brand-500 hover:text-brand-600 hover:underline"
            >
              contact HockeyKE
            </RouterLink>
            so it can be reviewed.
          </p>
        </section>
      </div>
    </article>
  </AdminLayout>
</template>

<script setup lang="ts">
import AdminLayout from "@/components/layout/AdminLayout.vue";
</script>
