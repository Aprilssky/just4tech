<template>
  <div>
    <section class="hero-gradient py-20">
      <div class="max-w-4xl mx-auto px-4 text-center relative z-10">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 text-amber-400 text-sm font-medium mb-6 border border-white/10">
          <span class="w-2 h-2 bg-amber-400 rounded-full animate-pulse-dot"></span>
          <span>Projects</span>
        </div>
        <h1 class="text-4xl sm:text-5xl font-bold text-white mb-4">🚀 Featured Projects</h1>
        <p class="text-lg text-gray-400 max-w-2xl mx-auto">Inspiring indie and vibe-coded projects from the community.</p>
      </div>
    </section>

    <section class="py-16 bg-white dark:bg-slate-900">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div v-if="projects.length" class="divide-y divide-gray-100 dark:divide-slate-700">
          <router-link v-for="p in projects" :key="p.slug" :to="'/blog/' + p.slug"
            class="flex items-start gap-4 py-5 px-2 -mx-2 rounded-lg hover:bg-gray-50 dark:hover:bg-slate-800 transition-colors no-underline group">
            <IconDisplay :icon="p.icon" fallback="🚀" size="2.5rem" />
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-xs px-2 py-0.5 rounded-full font-medium bg-emerald-100 text-emerald-700">Project</span>
                <span v-if="p.subtitle" class="text-xs text-gray-400 dark:text-slate-500">{{ p.subtitle }}</span>
                <span v-for="tag in (p.tags || '').split(',').slice(0,2)" :key="tag" v-if="tag && tag.trim()"
                  class="text-xs px-1.5 py-0.5 rounded bg-gray-100 dark:bg-slate-700 text-gray-500 dark:text-slate-400">{{ tag.trim() }}</span>
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors mb-1">{{ p.title }}</h3>
              <p class="text-sm text-gray-500 dark:text-slate-400 line-clamp-2">{{ p.excerpt }}</p>
            </div>
            <a v-if="p.external_url" :href="p.external_url" target="_blank" rel="noopener" @click.stop
              class="text-xs font-semibold flex-shrink-0 mt-1.5 px-2 py-1 rounded hover:bg-gray-100 dark:hover:bg-slate-700 transition-colors" style="color:var(--color-brand)">View ↗</a>
            <svg v-else class="w-5 h-5 text-gray-300 dark:text-slate-600 flex-shrink-0 mt-1 group-hover:text-amber-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </router-link>
        </div>
        <div v-else class="text-center py-12 text-gray-500">Loading projects...</div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePageMeta } from '../utils/meta.js'
import IconDisplay from '../components/IconDisplay.vue'

const projects = ref([])
onMounted(async () => {
  try { projects.value = await (await fetch('/api/projects')).json() } catch { projects.value = [] }
  usePageMeta({ title: 'Featured Projects', description: 'Inspiring indie and vibe-coded projects.' })
})
</script>
