<template>
  <div>
    <section class="hero-gradient py-20">
      <div class="max-w-4xl mx-auto px-4 text-center relative z-10">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 text-amber-400 text-sm font-medium mb-6 border border-white/10">
          <span class="w-2 h-2 bg-amber-400 rounded-full animate-pulse-dot"></span>
          <span>AI Tool Picks</span>
        </div>
        <h1 class="text-4xl sm:text-5xl font-bold text-white mb-4">AI Tools for <span class="gradient-text">Indie Devs</span></h1>
        <p class="text-lg text-gray-400 max-w-2xl mx-auto">Hand-picked tools I actually use and recommend — from AI coding agents to creative tools.</p>
      </div>
    </section>

    <section class="py-16 bg-white dark:bg-slate-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div v-if="tools.length" class="tool-grid">
          <router-link v-for="t in tools" :key="t.slug" :to="'/aitools/' + t.slug"
            class="tool-card no-underline block">
            <IconDisplay :icon="t.icon" fallback="🤖" size="2rem" />
            <h3 class="text-lg font-bold text-slate-900 dark:text-white mb-2">{{ t.title }}</h3>
            <div class="flex flex-wrap gap-2 mb-2">
              <span v-if="t.category" class="text-xs px-2 py-0.5 rounded-full" style="background:var(--color-brand-lightest);color:var(--color-brand)">AI Tool</span>
              <span v-if="t.subtitle" class="text-xs px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300">{{ t.subtitle }}</span>
            </div>
            <p class="text-sm text-slate-600 dark:text-slate-400 line-clamp-2">{{ t.excerpt }}</p>
            <span v-if="t.external_url" class="inline-block mt-3 text-xs font-semibold" style="color:var(--color-brand)">Visit →</span>
          </router-link>
        </div>
        <div v-else class="text-center py-12 text-gray-500">Loading tools...</div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePageMeta } from '../utils/meta.js'
import IconDisplay from '../components/IconDisplay.vue'

const tools = ref([])
onMounted(async () => {
  try { tools.value = await (await fetch('/api/software')).json() } catch { tools.value = [] }
  usePageMeta({ title: 'AI Tool Picks', description: 'Hand-picked AI tools for indie developers.' })
})
</script>
