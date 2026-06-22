<template>
  <div>
    <section class="hero-gradient py-20">
      <div class="max-w-4xl mx-auto px-4 text-center relative z-10">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 text-amber-400 text-sm font-medium mb-6 border border-white/10">
          <span class="w-2 h-2 bg-amber-400 rounded-full animate-pulse-dot"></span>
          <span>Legal</span>
        </div>
        <h1 class="text-4xl sm:text-5xl font-bold text-white mb-4">{{ page.title || 'Privacy Policy' }}</h1>
        <p v-if="page.meta_description" class="text-lg text-gray-400">{{ page.meta_description }}</p>
      </div>
    </section>

    <section class="py-16 bg-white dark:bg-slate-900">
      <div class="max-w-4xl mx-auto px-4 sm:px-6">
        <div v-if="loading" class="text-center py-12 text-gray-500">Loading...</div>
        <div v-else-if="page.content" class="blog-content" v-html="renderedContent"></div>
        <div v-else class="text-center py-12 text-gray-500">Content coming soon.</div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePageMeta } from '../utils/meta.js'
import { marked } from 'marked'

const page = ref({ title: '', content: '', meta_description: '' })
const loading = ref(true)

const renderedContent = computed(() => {
  try { return marked(page.value.content || '') } catch { return page.value.content || '' }
})

onMounted(async () => {
  try {
    const resp = await fetch('/api/page/privacy')
    if (resp.ok) page.value = await resp.json()
  } catch {}
  loading.value = false
  usePageMeta({
    title: page.value.meta_title || 'Privacy Policy',
    description: page.value.meta_description || 'Privacy Policy for Just4Tech.'
  })
})
</script>
