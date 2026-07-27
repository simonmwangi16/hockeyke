<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div
      class="min-h-screen rounded-2xl border border-gray-200 bg-white px-5 py-7 dark:border-gray-800 dark:bg-white/[0.03] xl:px-10 xl:py-12"
    >
      
            <!-- Tab Navigation Headers -->
            <div class="flex border-b border-gray-200">
                <button
                    v-for="tab in tabs"
                    :key="tab.id"
                    @click="activeTab = tab.id"
                    :class="[
                    'flex-1 py-2.5 text-sm font-medium text-center border-b-2 transition-all duration-200 focus:outline-none',
                    activeTab === tab.id
                        ? 'border-indigo-600 text-indigo-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    ]"
                >
                    {{ tab.label }}
                </button>
            </div>

            <!-- Tab Content Display -->
            <div class="mt-6">
                <div 
                    v-for="tab in tabs" 
                    :key="tab.id"
                    v-show="activeTab === tab.id" 
                    class="text-gray-600 text-sm leading-relaxed"
                >
                    {{ tab.content }}
                </div>
            </div>
        </div>

  </AdminLayout>
</template>

<script setup>
import { ref } from "vue";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";

const currentPageTitle = ref("Fixtures");

// Define the tabs and their associated content
const tabs = [
  { id: 'profile', label: 'My Profile', content: 'Manage your personal details, profile picture, and security settings.' },
  { id: 'settings', label: 'Settings', content: 'Customize your system preferences, email notifications, and privacy options.' },
  { id: 'billing', label: 'Billing', content: 'View your invoices, update payment methods, and manage subscription plans.' }
]

// Keep track of the active tab
const activeTab = ref('profile')
</script>

<style></style>
