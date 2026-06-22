<template>
  <nav class="navbar bg-gray-900/95 backdrop-blur-md sticky top-0 z-50" :class="{ 'shadow-lg shadow-black/20': scrolled }" role="navigation" aria-label="Main navigation">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <router-link to="/" class="flex items-center gap-2 text-white font-bold text-xl no-underline">
          <span class="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-500 to-rose-500 flex items-center justify-center text-white text-sm font-bold">JT</span>
          <span>Just4Tech</span>
        </router-link>
        <div class="desktop-nav flex items-center gap-8">
          <router-link to="/blog" :class="{ active: $route.path.startsWith('/blog') }">Blog</router-link>
          <router-link to="/aitools" :class="{ active: $route.path.startsWith('/aitools') }">AI Tools</router-link>
          <router-link to="/projects" :class="{ active: $route.path.startsWith('/projects') }">Projects</router-link>
          <router-link to="/indie-devs" :class="{ active: $route.path === '/indie-devs' }">Indie Devs</router-link>
          <router-link to="/tutorials" :class="{ active: $route.path === '/tutorials' }">Tutorial</router-link>
          <router-link to="/sites" :class="{ active: $route.path === '/sites' }">Sites</router-link>
          <router-link to="/about" :class="{ active: $route.path === '/about' }">About</router-link>
          <!-- Search -->
          <button
            @click="openSearch"
            class="text-gray-400 hover:text-white p-2 transition-colors"
            aria-label="Search"
            title="Search"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
          <button
            @click="toggleSound"
            class="text-gray-400 hover:text-white p-2 transition-colors"
            :aria-label="soundEnabled ? 'Mute sound effects' : 'Enable sound effects'"
            :title="soundEnabled ? 'Sound on' : 'Sound off'"
          >
            <svg v-if="soundEnabled" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
            </svg>
          </button>
          <button
            @click="toggleTheme"
            class="text-gray-400 hover:text-white p-2 transition-colors"
            :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
            :title="isDark ? 'Light mode' : 'Dark mode'"
          >
            <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
          <router-link to="/contact" class="btn btn-primary !py-2 !px-4 !text-sm">Contact</router-link>
        </div>
        <button
          @click="toggleMobileMenu"
          class="md:hidden text-white p-2"
          :aria-expanded="mobileOpen"
          aria-label="Toggle navigation menu"
        >
          <svg v-if="!mobileOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
    <div v-if="mobileOpen" class="mobile-nav md:hidden">
      <router-link to="/blog" @click="mobileOpen = false">Blog</router-link>
      <router-link to="/aitools" @click="mobileOpen = false">AI Tools</router-link>
      <router-link to="/projects" @click="mobileOpen = false">Projects</router-link>
      <router-link to="/indie-devs" @click="mobileOpen = false">Indie Devs</router-link>
      <router-link to="/tutorials" @click="mobileOpen = false">Tutorial</router-link>
      <router-link to="/sites" @click="mobileOpen = false">Sites</router-link>
      <router-link to="/about" @click="mobileOpen = false">About</router-link>
      <router-link to="/contact" class="btn btn-primary !py-2 !px-4 !text-sm" @click="mobileOpen = false">Contact</router-link>
      <button
        @click="toggleTheme"
        class="flex items-center gap-2 text-gray-400 hover:text-white py-2"
      >
        <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
        <span>{{ isDark ? 'Light Mode' : 'Dark Mode' }}</span>
      </button>
    </div>
  </nav>

  <!-- Search Overlay -->
  <Transition name="fade">
    <div v-if="searchOpen" class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm" @click="closeSearch"></div>
  </Transition>
  <Transition name="slide-down">
    <div v-if="searchOpen" class="fixed top-0 left-0 right-0 z-[101] bg-white dark:bg-slate-900 shadow-xl border-b border-slate-200 dark:border-slate-700">
      <div class="max-w-3xl mx-auto px-4 py-6">
        <div class="flex items-center gap-3 mb-6">
          <svg class="w-5 h-5 text-slate-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            id="search-input"
            v-model="searchQuery"
            @input="doSearch"
            @keydown.escape="closeSearch"
            @keydown.enter="searchResults.length && goTo(searchResults[0].url)"
            placeholder="Search posts and tools..."
            class="flex-1 text-lg bg-transparent border-none outline-none text-slate-900 dark:text-white placeholder-slate-400"
          >
          <kbd class="hidden sm:inline-flex px-2 py-1 text-xs text-slate-400 border border-slate-300 dark:border-slate-600 rounded">ESC</kbd>
        </div>
        <div v-if="searchLoading" class="text-center py-8 text-slate-500">
          <div class="inline-block w-5 h-5 border-2 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
        <div v-else-if="searchQuery && !resultsCount" class="text-center py-8 text-slate-500">
          No results found for "{{ searchQuery }}"
        </div>
        <div v-else-if="resultsCount" class="space-y-0.5 -mx-4">
          <div
            v-for="r in searchResults"
            :key="r.url"
            @click="goTo(r.url)"
            class="flex items-start gap-3 px-4 py-3 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg transition-colors"
          >
            <span class="mt-0.5 flex-shrink-0">{{ r.type === 'post' ? '📝' : '🔧' }}</span>
            <div class="min-w-0">
              <div class="text-sm font-medium text-slate-900 dark:text-white truncate">{{ r.title }}</div>
              <div class="text-xs text-slate-500 truncate">{{ r.excerpt }}</div>
            </div>
            <span class="ml-auto text-xs text-slate-400 flex-shrink-0">{{ r.type }}</span>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { isSoundEnabled, toggleSound as toggleSnd } from '../utils/sound.js'

const router = useRouter()
const mobileOpen = ref(false)
const isDark = ref(true)
const scrolled = ref(false)
const soundEnabled = ref(isSoundEnabled())
const searchOpen = ref(false)
const searchQuery = ref('')
const searchResults = ref([])
const searchLoading = ref(false)

function onScroll() {
  scrolled.value = window.scrollY > 10
}

function toggleMobileMenu() {
  mobileOpen.value = !mobileOpen.value
}

function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
  localStorage.setItem('j4t-theme', isDark.value ? 'dark' : 'light')
}

function toggleSound() {
  soundEnabled.value = toggleSnd()
}

// ── Search ──

async function openSearch() {
  searchOpen.value = true
  searchQuery.value = ''
  searchResults.value = []
  await doSearch()
  setTimeout(() => document.getElementById('search-input')?.focus(), 100)
}

function closeSearch() {
  searchOpen.value = false
  searchResults.value = []
  searchQuery.value = ''
}

const resultsCount = computed(() => searchResults.value.length)

async function doSearch() {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) {
    searchResults.value = []
    return
  }
  searchLoading.value = true
  try {
    const [posts, software, projects] = await Promise.all([
      fetch('/api/posts').then(r => r.ok ? r.json() : []),
      fetch('/api/software').then(r => r.ok ? r.json() : []),
      fetch('/api/projects').then(r => r.ok ? r.json() : [])
    ])
    const results = []
    for (const p of (posts || [])) {
      const title = (p.title || '').toLowerCase()
      const excerpt = (p.excerpt || '').toLowerCase()
      const cat = (p.category || '').toLowerCase()
      if (title.includes(q) || excerpt.includes(q) || cat === q) {
        results.push({ type: '📝 Blog', title: p.title, url: '/blog/' + p.slug, excerpt: p.excerpt || p.category })
      }
    }
    for (const s of (software || [])) {
      const name = (s.title || '').toLowerCase()
      const desc = (s.description || '').toLowerCase()
      const cat = (s.category || '').toLowerCase()
      const tags = (s.tags || '').toLowerCase()
      if (name.includes(q) || desc.includes(q) || cat.includes(q) || tags.includes(q)) {
        results.push({ type: '🤖 Tool', title: s.title, url: '/aitools/' + s.slug, excerpt: s.excerpt })
      }
    }
    for (const p of (projects || [])) {
      const name = (p.title || '').toLowerCase()
      const desc = (p.description || '').toLowerCase()
      const tech = (p.tech_stack || '').toLowerCase()
      if (name.includes(q) || desc.includes(q) || tech.includes(q)) {
        results.push({ type: '🚀 Project', title: p.title, url: '/projects/' + p.slug, excerpt: p.excerpt })
      }
    }
    searchResults.value = results.slice(0, 12)
  } catch {}
  searchLoading.value = false
}

function goTo(url) {
  closeSearch()
  router.push(url)
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  const saved = localStorage.getItem('j4t-theme')
  if (saved) {
    isDark.value = saved === 'dark'
  }
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
})
</script>
