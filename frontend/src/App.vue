<script setup lang="ts">
import ThemeToggle from './components/ThemeToggle.vue'
</script>

<template>
  <div class="min-h-screen w-full flex flex-col bg-white dark:bg-gray-800">
    <header class="flex items-center justify-between p-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100">Course Manager</h1>
      <div class="flex items-center gap-4">
        <ThemeToggle />
        <button
          class="px-4 py-2 bg-black hover:bg-gray-800 text-white dark:bg-red-700 dark:hover:bg-red-800 rounded-md transition-colors">
          Logout
        </button>
      </div>
    </header>
    <router-view class="flex-1"></router-view>
  </div>
</template>
<style scoped>
</style>