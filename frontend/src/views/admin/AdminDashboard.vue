<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-white">📊 Dashboard</h1>

    <!-- Error state -->
    <div v-if="error" class="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-xl p-6 mb-6 text-center">
      <p class="text-red-700 dark:text-red-300 mb-3">{{ error }}</p>
      <router-link to="/admin/login" class="inline-block px-5 py-2 rounded-lg text-white text-sm font-medium" style="background:var(--color-brand)">Re-login</router-link>
    </div>

    <!-- Loading -->
    <div v-else-if="!stats" class="text-gray-500 dark:text-slate-400 text-center py-12">
      <div class="text-4xl mb-3">⏳</div>
      <p>Loading dashboard data...</p>
    </div>

    <!-- Stats Grid -->
    <template v-else>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-white dark:bg-slate-800 rounded-xl p-5 border border-gray-200 dark:border-slate-700 hover:shadow-md transition-shadow">
          <div class="text-sm text-gray-500 dark:text-slate-400">📝 Blog Posts</div>
          <div class="text-3xl font-bold mt-1 text-gray-900 dark:text-white">{{ stats.total_posts }}</div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-xl p-5 border border-gray-200 dark:border-slate-700 hover:shadow-md transition-shadow">
          <div class="text-sm text-gray-500 dark:text-slate-400">🤖 AI Tools</div>
          <div class="text-3xl font-bold mt-1 text-gray-900 dark:text-white">{{ stats.total_software }}</div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-xl p-5 border border-gray-200 dark:border-slate-700 hover:shadow-md transition-shadow">
          <div class="text-sm text-gray-500 dark:text-slate-400">🚀 Projects</div>
          <div class="text-3xl font-bold mt-1 text-gray-900 dark:text-white">{{ stats.total_projects }}</div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-xl p-5 border border-gray-200 dark:border-slate-700 hover:shadow-md transition-shadow">
          <div class="text-sm text-gray-500 dark:text-slate-400">👁 Page Views Today</div>
          <div class="text-3xl font-bold mt-1 text-gray-900 dark:text-white">{{ stats.today_views }}</div>
        </div>
      </div>

      <!-- Sub stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-white dark:bg-slate-800 rounded-xl p-4 border border-gray-200 dark:border-slate-700">
          <div class="text-xs text-gray-500 dark:text-slate-400">Total Page Views</div>
          <div class="text-xl font-bold mt-0.5 text-gray-900 dark:text-white">{{ stats.total_views?.toLocaleString() }}</div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-xl p-4 border border-gray-200 dark:border-slate-700">
          <div class="text-xs text-gray-500 dark:text-slate-400">Contact Messages</div>
          <div class="text-xl font-bold mt-0.5 text-gray-900 dark:text-white">{{ stats.contact_count }}</div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-xl p-4 border border-gray-200 dark:border-slate-700">
          <div class="text-xs text-gray-500 dark:text-slate-400">Top Page</div>
          <div class="text-sm font-semibold mt-0.5 truncate" :style="{color: 'var(--color-brand)'}">{{ topPage }}</div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-xl p-4 border border-gray-200 dark:border-slate-700">
          <div class="text-xs text-gray-500 dark:text-slate-400">7-Day Trend</div>
          <div class="text-xl font-bold mt-0.5" :class="trend >= 0 ? 'text-green-600' : 'text-red-500'">{{ trend >= 0 ? '↑' : '↓' }} {{ Math.abs(trend) }}%</div>
        </div>
      </div>

      <!-- Top Pages Table -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden">
          <div class="px-5 py-4 border-b border-gray-100 dark:border-slate-700 font-semibold text-gray-900 dark:text-white">🔗 Top Pages</div>
          <table class="w-full text-sm">
            <thead><tr class="text-left text-gray-500 dark:text-slate-400 text-xs uppercase tracking-wider"><th class="px-5 py-3">Path</th><th class="px-5 py-3 text-right">Views</th></tr></thead>
            <tbody>
              <tr v-for="(p, i) in (stats.top_pages || []).slice(0, 8)" :key="i" class="border-t border-gray-50 dark:border-slate-700/50 hover:bg-gray-50 dark:hover:bg-slate-700/30">
                <td class="px-5 py-2.5 font-medium text-gray-900 dark:text-white truncate max-w-[200px]">{{ p.path }}</td>
                <td class="px-5 py-2.5 text-right text-gray-600 dark:text-slate-400">{{ p.count }}</td>
              </tr>
            </tbody>
          </table>
          <div v-if="!stats.top_pages?.length" class="px-5 py-8 text-center text-sm text-gray-400">No data yet</div>
        </div>

        <!-- Daily Views (simple bar chart) -->
        <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden">
          <div class="px-5 py-4 border-b border-gray-100 dark:border-slate-700 font-semibold text-gray-900 dark:text-white">📈 Daily Views (30 days)</div>
          <div class="p-5">
            <div class="flex items-end gap-1 h-32" v-if="stats.daily_views?.length">
              <div v-for="(d, i) in stats.daily_views.slice(-30)" :key="i"
                class="flex-1 rounded-t transition-all hover:opacity-80"
                style="min-width:4px"
                :style="{ height: (d.count / maxDailyCount * 100) + '%', background: 'var(--color-brand)', opacity: 0.3 + (d.count / maxDailyCount * 0.7) }"
                :title="d.date + ': ' + d.count + ' views'"></div>
            </div>
            <div v-else class="text-center py-8 text-sm text-gray-400">No view data yet</div>
            <div class="text-xs text-gray-400 text-center mt-2">each bar = 1 day</div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-5">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-4">⚡ Quick Actions</h3>
        <div class="flex flex-wrap gap-3">
          <router-link to="/admin/posts" class="px-4 py-2 rounded-lg text-sm font-medium no-underline bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-slate-300 hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors">✍️ Manage Posts</router-link>
          <router-link to="/admin/media" class="px-4 py-2 rounded-lg text-sm font-medium no-underline bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-slate-300 hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors">🖼 Media Library</router-link>
          <router-link to="/admin/pages" class="px-4 py-2 rounded-lg text-sm font-medium no-underline bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-slate-300 hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors">📄 Edit Pages</router-link>
          <router-link to="/admin/messages" class="px-4 py-2 rounded-lg text-sm font-medium no-underline bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-slate-300 hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors">✉️ View Messages</router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const stats = ref(null)
const error = ref('')

const topPage = computed(() => stats.value?.top_pages?.[0]?.path || '—')
const trend = computed(() => {
  const dv = stats.value?.daily_views || []
  if (dv.length < 14) return 0
  const recent = dv.slice(-7).reduce((s, d) => s + d.count, 0)
  const prior = dv.slice(-14, -7).reduce((s, d) => s + d.count, 0)
  if (prior === 0) return recent > 0 ? 100 : 0
  return Math.round((recent - prior) / prior * 100)
})
const maxDailyCount = computed(() => {
  const dv = stats.value?.daily_views || []
  return Math.max(...dv.map(d => d.count), 1)
})

onMounted(async () => {
  try {
    const resp = await fetch('/api/admin/analytics')
    if (!resp.ok) {
      if (resp.status === 401) error.value = 'Session expired. Please log in again.'
      else error.value = `Server error (${resp.status}). Try refreshing.`
      return
    }
    stats.value = await resp.json()
  } catch {
    error.value = 'Cannot connect to server. Check your network.'
  }
})
</script>
