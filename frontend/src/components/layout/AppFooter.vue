<template>
  <footer class="border-t border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900">
    <div
      class="mx-auto flex max-w-(--breakpoint-2xl) flex-col gap-6 px-4 py-8 md:flex-row md:items-end md:justify-between md:px-6"
    >
      <div class="max-w-md">
        <RouterLink
          to="/"
          class="text-base font-bold text-gray-900 hover:text-brand-500 dark:text-white"
        >
          HockeyKE
        </RouterLink>
        <p class="mt-2 text-sm leading-6 text-gray-500 dark:text-gray-400">
          Kenyan field hockey fixtures, results, standings and team statistics.
        </p>
      </div>

      <nav aria-label="Footer navigation">
        <ul class="flex flex-wrap gap-x-5 gap-y-3 text-sm">
          <li>
            <RouterLink
              class="text-gray-500 transition hover:text-brand-500 focus-visible:text-brand-500 dark:text-gray-400"
              to="/"
            >
              Home
            </RouterLink>
          </li>
          <li>
            <RouterLink
              class="text-gray-500 transition hover:text-brand-500 focus-visible:text-brand-500 dark:text-gray-400"
              to="/fixtures"
            >
              Fixtures
            </RouterLink>
          </li>
          <li>
            <RouterLink
              class="text-gray-500 transition hover:text-brand-500 focus-visible:text-brand-500 dark:text-gray-400"
              to="/league/men/premier-league"
            >
              Men
            </RouterLink>
          </li>
          <li>
            <RouterLink
              class="text-gray-500 transition hover:text-brand-500 focus-visible:text-brand-500 dark:text-gray-400"
              to="/league/women/premier-league"
            >
              Women
            </RouterLink>
          </li>
          <li>
            <RouterLink
              class="text-gray-500 transition hover:text-brand-500 focus-visible:text-brand-500 dark:text-gray-400"
              to="/about"
            >
              About
            </RouterLink>
          </li>
          <li>
            <RouterLink
              class="text-gray-500 transition hover:text-brand-500 focus-visible:text-brand-500 dark:text-gray-400"
              to="/contact"
            >
              Contact
            </RouterLink>
          </li>
          <li>
            <RouterLink
              class="text-gray-500 transition hover:text-brand-500 focus-visible:text-brand-500 dark:text-gray-400"
              to="/privacy"
            >
              Privacy
            </RouterLink>
          </li>
        </ul>
      </nav>

      <p class="text-xs text-gray-400">
        © {{ currentYear }} HockeyKE
      </p>
    </div>
  </footer>
</template>

<script setup lang="ts">
defineOptions({
  name: "AppFooter",
});

const currentYear = new Date().getFullYear();
</script>
