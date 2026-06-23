<template>
  <div>
    <section class="hero-gradient py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="mb-4">
          <router-link to="/aitools" class="text-amber-400 hover:text-amber-300 text-sm flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back to AI Tools
          </router-link>
        </div>
        <div class="flex items-center gap-4 mb-4">
          <div class="w-14 h-14 rounded-xl flex items-center justify-center text-2xl bg-amber-100 dark:bg-amber-900/50 overflow-hidden">
            <IconDisplay :icon="item.icon" fallback="🤖" size="1.75rem" />
          </div>
          <div>
            <h1 class="text-3xl sm:text-4xl font-bold text-white">{{ item.title || capitalize(slug) }}</h1>
            <div class="flex items-center gap-3 mt-1 text-sm text-gray-400">
              <span v-if="item.category">{{ item.category }}</span>
              <span v-if="item.subtitle">{{ item.subtitle }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 bg-white dark:bg-slate-900">
      <div class="max-w-4xl mx-auto px-4 sm:px-6">
        <!-- Markdown content -->
        <div v-if="item.content" class="blog-content" v-html="rendered"></div>
        <div v-else class="text-center py-12 text-gray-500">
          <p>{{ item.excerpt || 'Details coming soon.' }}</p>
        </div>

        <!-- Metadata cards -->
        <div v-if="item.subtitle || item.tags" class="grid grid-cols-2 gap-4 mt-10">
          <div v-if="item.subtitle" class="bg-slate-50 dark:bg-slate-800 rounded-xl p-4 border border-slate-200 dark:border-slate-700">
            <div class="text-xs text-slate-500 uppercase tracking-wider mb-1">Details</div>
            <div class="text-sm font-semibold text-gray-900 dark:text-white">{{ item.subtitle }}</div>
          </div>
          <div v-if="item.tags" class="bg-slate-50 dark:bg-slate-800 rounded-xl p-4 border border-slate-200 dark:border-slate-700">
            <div class="text-xs text-slate-500 uppercase tracking-wider mb-1">Tags</div>
            <div class="text-sm text-gray-900 dark:text-white">{{ item.tags }}</div>
          </div>
        </div>

        <!-- External link -->
        <div v-if="item.external_url" class="mt-6">
          <a :href="item.external_url" target="_blank" rel="noopener"
            class="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-white text-sm font-medium no-underline transition-colors"
            style="background:var(--color-brand)">
            🔗 Visit Website →
          </a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePageMeta } from '../utils/meta.js'
import { useRoute } from 'vue-router'
import IconDisplay from '../components/IconDisplay.vue'

let markedModule = null
async function getMarked() {
  if (!markedModule) {
    markedModule = await import('marked')
  }
  return markedModule.marked
}

const route = useRoute()
const slug = route.params.slug
const item = ref({})
const rendered = ref('')

onMounted(async () => {
  try {
    const res = await fetch('/api/software/slug/' + slug)
    if (res.ok) {
      item.value = await res.json()
      usePageMeta({ title: item.value.title, description: item.value.excerpt })
    }
  } catch {}
  if (!item.value.title) {
    item.value.title = capitalize(slug)
  }
  // Lazy-render markdown content
  if (item.value.content) {
    try {
      const marked = await getMarked()
      rendered.value = marked.parse(item.value.content)
    } catch { rendered.value = '' }
  }
})

function capitalize(str) {
  return str.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}
</script>
