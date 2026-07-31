<template>
  <AdminLayout>
    <article
      class="rounded-2xl border border-gray-200 bg-white px-5 py-7 dark:border-gray-800 dark:bg-white/[0.03] md:px-8 md:py-10"
    >
      <div class="max-w-3xl">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Privacy Policy</h1>
        <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">Last updated: 30 July 2026</p>

        <p class="mt-6 leading-7 text-gray-600 dark:text-gray-300">
          HockeyKE does not currently operate a contact form or directly collect information
          submitted through the public content pages. The website uses Google and Meta services
          that may use cookies and similar technologies.
        </p>

        <section class="mt-10">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">
            Analytics and advertising
          </h2>
          <p class="mt-3 leading-7 text-gray-600 dark:text-gray-300">
            HockeyKE uses Google Analytics and Meta Pixel to understand how the website is used and
            measure advertising, and Google AdSense to display advertising. Google and Meta may
            process information such as cookie identifiers, browser and device information, pages
            visited, interactions, IP-derived approximate location and advertising data.
          </p>
        </section>

        <section class="mt-8">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Cookie choices</h2>
          <p class="mt-3 leading-7 text-gray-600 dark:text-gray-300">
            You can restrict or delete cookies through your browser settings and manage advertising
            preferences through the relevant Google and Meta account settings. You can manage how
            Google personalises advertising through
            <a
              href="https://myadcenter.google.com/"
              target="_blank"
              rel="noopener noreferrer"
              class="font-semibold text-brand-500 hover:text-brand-600 hover:underline"
            >
              My Ad Center
            </a>
            and review
            <a
              href="https://policies.google.com/technologies/partner-sites"
              target="_blank"
              rel="noopener noreferrer"
              class="font-semibold text-brand-500 hover:text-brand-600 hover:underline"
            >
              how Google uses information from partner sites
            </a>
            .
          </p>
        </section>

        <section class="mt-8">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">External links</h2>
          <p class="mt-3 leading-7 text-gray-600 dark:text-gray-300">
            HockeyKE may link to other websites. Their privacy practices are governed by their own
            policies, and HockeyKE is not responsible for how those sites handle information.
          </p>
        </section>

        <section class="mt-8">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Contact</h2>
          <p class="mt-3 leading-7 text-gray-600 dark:text-gray-300">
            For privacy questions, email
            <a
              href="mailto:hockeyke@gmail.com"
              class="font-semibold text-brand-500 hover:text-brand-600 hover:underline"
            >
              hockeyke@gmail.com
            </a>
            .
          </p>
        </section>
      </div>
    </article>
  </AdminLayout>
</template>

<script setup lang="ts">
import AdminLayout from "@/components/layout/AdminLayout.vue";
</script>
