<template>
  <div class="min-h-[60vh] flex items-center justify-center">
    <div class="text-center px-4">
      <div class="text-7xl font-extrabold text-amber-600 mb-4">404</div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Page Not Found</h1>
      <p class="text-slate-600 dark:text-slate-400 mb-8 max-w-md mx-auto">The page you're looking for doesn't exist or has been moved.</p>
      <div class="flex items-center justify-center gap-4">
        <router-link to="/" class="inline-flex items-center gap-2 px-5 py-2.5 bg-amber-600 text-white rounded-lg hover:bg-amber-700 no-underline text-sm font-medium transition-colors">
          Go Home
        </router-link>
        <router-link to="/blog" class="inline-flex items-center gap-2 px-5 py-2.5 border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 no-underline text-sm font-medium transition-colors">
          Browse Blog
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue"
import { usePageMeta } from "../utils/meta.js"

onMounted(() => usePageMeta({title: "404 Not Found", description: "The page you're looking for doesn't exist."}))
</script>
