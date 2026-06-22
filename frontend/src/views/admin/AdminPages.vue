<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">📄 Pages</h1>
      <span class="text-xs text-gray-400 dark:text-slate-500">Edit your site's static page content</span>
    </div>

    <div v-if="loading" class="text-center py-12 text-gray-500">Loading...</div>

    <div v-else-if="!pages.length" class="text-center py-16 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700">
      <div class="text-5xl mb-4">📭</div>
      <p class="text-gray-500 dark:text-slate-400">No pages found</p>
    </div>

    <div v-else class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden">
      <table class="w-full text-sm">
        <thead><tr class="bg-gray-50 dark:bg-slate-700 text-left font-semibold text-gray-600 dark:text-slate-300"><th class="p-4">Title</th><th class="p-4 hidden md:table-cell">Slug</th><th class="p-4">Actions</th></tr></thead>
        <tbody>
          <tr v-for="p in pages" :key="p.id" class="border-t border-gray-100 dark:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-700/50">
            <td class="p-4 font-medium text-gray-900 dark:text-white">{{ p.title }}</td>
            <td class="p-4 text-gray-500 dark:text-slate-400 hidden md:table-cell text-xs font-mono">{{ p.slug }}</td>
            <td class="p-4">
              <button @click="$router.push('/admin/pages/edit/'+p.id)" class="text-sm font-medium no-underline hover:underline" style="color:var(--color-brand)">✏️ Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const pages = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const resp = await fetch('/api/pages')
    if (resp.ok) pages.value = await resp.json()
  } catch {}
  loading.value = false
})
</script>
