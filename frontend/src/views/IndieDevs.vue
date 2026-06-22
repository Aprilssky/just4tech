<template>
  <div>
    <section class="hero-gradient py-20">
      <div class="max-w-4xl mx-auto px-4 text-center relative z-10">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 text-amber-400 text-sm font-medium mb-6 border border-white/10">
          <span class="w-2 h-2 bg-amber-400 rounded-full animate-pulse-dot"></span>
          <span>Spotlight</span>
        </div>
        <h1 class="text-4xl sm:text-5xl font-bold text-white mb-4">🌟 Indie Dev Spotlight</h1>
        <p class="text-lg text-gray-400 max-w-2xl mx-auto">Outstanding indie developers, bootstrappers, and solopreneurs — their stories, projects, and lessons learned.</p>
      </div>
    </section>

    <section class="py-16 bg-white dark:bg-slate-900">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div v-if="devs.length" class="divide-y divide-gray-100 dark:divide-slate-700">
          <router-link v-for="dev in devs" :key="dev.slug" :to="'/blog/' + dev.slug"
            class="flex items-start gap-4 py-5 px-2 -mx-2 rounded-lg hover:bg-gray-50 dark:hover:bg-slate-800 transition-colors no-underline group">
            <IconDisplay :icon="dev.icon" fallback="🌟" size="2.5rem" />
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-xs px-2 py-0.5 rounded-full font-medium bg-rose-100 text-rose-700">Indie Dev</span>
                <span v-if="dev.subtitle" class="text-xs text-gray-400 dark:text-slate-500">{{ dev.subtitle }}</span>
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors mb-1">{{ dev.title }}</h3>
              <p class="text-sm text-gray-500 dark:text-slate-400 line-clamp-2">{{ dev.excerpt }}</p>
            </div>
            <svg class="w-5 h-5 text-gray-300 dark:text-slate-600 flex-shrink-0 mt-1 group-hover:text-amber-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </router-link>
        </div>
        <div v-else class="text-center py-12 text-gray-500">No indie devs featured yet.</div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePageMeta } from '../utils/meta.js'
import IconDisplay from '../components/IconDisplay.vue'

const devs = ref([])
onMounted(async () => {
  try {
    const all = await (await fetch('/api/posts')).json()
    devs.value = (all || []).filter(p => p.category === 'Indie Dev' && p.status === 'active')
  } catch { devs.value = [] }
  usePageMeta({ title: 'Indie Dev Spotlight', description: 'Outstanding indie developers and their stories.' })
})
</script>
