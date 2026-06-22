<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">📝 Posts</h1>
      <button @click="$router.push('/admin/posts/edit/new')" class="px-4 py-2 rounded-lg text-white text-sm font-medium" style="background:var(--color-brand)">+ New Post</button>
    </div>

    <!-- Tabs -->
    <div class="flex gap-0 border-b border-gray-200 dark:border-slate-700 mb-6">
      <button @click="activeTab = 'published'" :class="tabClass('published')">
        📄 Published
      </button>
      <button @click="activeTab = 'trash'" :class="tabClass('trash')">
        🗑 Trash <span v-if="trashCount" class="ml-1.5 px-1.5 py-0.5 text-xs rounded-full bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300">{{ trashCount }}</span>
      </button>
    </div>

    <!-- Published Tab -->
    <template v-if="activeTab === 'published'">
      <!-- Category filters -->
      <div class="flex flex-wrap gap-2 mb-6">
        <button v-for="c in allCategories" :key="c"
          @click="activeCategory = (activeCategory === c ? '' : c)"
          class="filter-btn" :class="{ active: activeCategory === c }">
          {{ c }}
        </button>
      </div>

      <div v-if="!publishedPosts.length" class="text-center py-8 text-gray-500 dark:text-slate-400">
        No posts yet.
      </div>

      <div v-else-if="!filteredPosts.length" class="text-center py-8 text-gray-500 dark:text-slate-400">
        No posts in this category.
      </div>

      <div v-else class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden">
        <table class="w-full text-sm">
          <thead><tr class="bg-gray-50 dark:bg-slate-700 text-left font-semibold text-gray-600 dark:text-slate-300"><th class="p-4">Title</th><th class="p-4 hidden md:table-cell">Category</th><th class="p-4 hidden md:table-cell">Status</th><th class="p-4">Actions</th></tr></thead>
          <tbody>
            <tr v-for="p in filteredPosts" :key="p.id" class="border-t border-gray-100 dark:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-700/50">
              <td class="p-4 font-medium text-gray-900 dark:text-white">{{ p.title }}</td>
              <td class="p-4 text-gray-600 dark:text-slate-400 hidden md:table-cell">
                <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="catClass(p.category)">{{ p.category }}</span>
              </td>
              <td class="p-4 hidden md:table-cell"><span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="statusClass(p.status)">{{ p.status }}</span></td>
              <td class="p-4">
                <button @click="$router.push('/admin/posts/edit/'+(p.id))" class="text-sm font-medium no-underline" style="color:var(--color-brand)">Edit</button>
                <button @click="trashPost(p.id)" :disabled="actionInProgress === p.id" class="text-sm font-medium text-red-500 hover:text-red-700 hover:underline ml-3">
                  {{ actionInProgress === p.id ? '...' : '🗑 Trash' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- Trash Tab -->
    <template v-else>
      <div class="flex items-center justify-end mb-4" v-if="trashedPosts.length">
        <button @click="emptyTrash" :disabled="isBusy" class="px-4 py-2 rounded-lg text-white text-sm font-medium bg-red-600 hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
          {{ saving ? 'Emptying...' : '🗑 Empty Trash' }}
        </button>
      </div>

      <div v-if="!trashedPosts.length" class="text-center py-16 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700">
        <div class="text-5xl mb-4">🗑</div>
        <p class="text-gray-500 dark:text-slate-400">Trash is empty</p>
      </div>

      <div v-else class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden">
        <table class="w-full text-sm">
          <thead><tr class="bg-gray-50 dark:bg-slate-700 text-left font-semibold text-gray-600 dark:text-slate-300"><th class="p-4">Title</th><th class="p-4 hidden md:table-cell">Category</th><th class="p-4 hidden md:table-cell">Status</th><th class="p-4">Actions</th></tr></thead>
          <tbody>
            <tr v-for="p in trashedPosts" :key="p.id" class="border-t border-gray-100 dark:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-700/50">
              <td class="p-4 font-medium text-gray-900 dark:text-white">{{ p.title }}</td>
              <td class="p-4 text-gray-600 dark:text-slate-400 hidden md:table-cell">
                <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="catClass(p.category)">{{ p.category }}</span>
              </td>
              <td class="p-4 hidden md:table-cell"><span class="px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300">trash</span></td>
              <td class="p-4">
                <button @click="restorePost(p.id)" :disabled="actionInProgress === p.id" class="text-sm font-medium text-blue-500 hover:text-blue-700 hover:underline">
                  {{ actionInProgress === p.id ? '...' : '↩ Restore' }}
                </button>
                <button @click="deleteForever(p.id)" :disabled="actionInProgress === p.id" class="text-sm font-medium text-red-500 hover:text-red-700 hover:underline ml-3">
                  {{ actionInProgress === p.id ? '...' : '🗑 Delete Forever' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const posts = ref([])
const activeCategory = ref('')
const activeTab = ref('published')
const actionInProgress = ref(null)
const saving = ref(false)

const NAV_CATEGORIES = ['Tutorial', 'Vibe Coding', 'Indie Diary', 'Dev Tools', 'AI Tool', 'Project', 'Indie Dev', 'Site']

const publishedPosts = computed(() => {
  return posts.value.filter(p => p.status !== 'trash' && p.status !== 'deleted')
})

const trashedPosts = computed(() => {
  return posts.value.filter(p => p.status === 'trash')
})

const trashCount = computed(() => trashedPosts.value.length)

const isBusy = computed(() => saving.value || actionInProgress.value !== null)

const allCategories = computed(() => {
  const fromData = new Set(publishedPosts.value.map(p => p.category).filter(Boolean))
  NAV_CATEGORIES.forEach(c => fromData.add(c))
  return [...fromData].sort()
})

const filteredPosts = computed(() => {
  if (!activeCategory.value) return publishedPosts.value
  return publishedPosts.value.filter(p => p.category === activeCategory.value)
})

function tabClass(tab) {
  const base = 'px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px'
  return activeTab.value === tab
    ? `${base} border-amber-500 text-amber-600 dark:text-amber-400`
    : `${base} border-transparent text-gray-500 dark:text-slate-400 hover:text-gray-700 dark:hover:text-slate-300`
}

function catClass(cat) {
  const map = {
    'Tutorial': 'bg-blue-100 text-blue-700',
    'Vibe Coding': 'bg-purple-100 text-purple-700',
    'Indie Diary': 'bg-orange-100 text-orange-700',
    'Dev Tools': 'bg-sky-100 text-sky-700',
    'AI Tool': 'bg-amber-100 text-amber-700',
    'Project': 'bg-emerald-100 text-emerald-700',
    'Indie Dev': 'bg-rose-100 text-rose-700',
    'Site': 'bg-teal-100 text-teal-700',
  }
  return map[cat] || 'bg-gray-100 text-gray-700'
}

function statusClass(status) {
  if (status === 'active') return 'bg-green-100 text-green-700'
  if (status === 'trash') return 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300'
  return 'bg-gray-100 text-gray-600'
}

// Helper: partial PUT — backend supports updating individual fields
async function updatePostStatus(id, newStatus) {
  await fetch('/api/posts/' + id, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: newStatus })
  })
}

async function trashPost(id) {
  if (!confirm('Move this post to trash?')) return
  actionInProgress.value = id
  try {
    await updatePostStatus(id, 'trash')
    const post = posts.value.find(p => p.id === id)
    if (post) post.status = 'trash'
  } catch {
    alert('Failed to move post to trash.')
  }
  actionInProgress.value = null
}

async function restorePost(id) {
  actionInProgress.value = id
  try {
    await updatePostStatus(id, 'draft')
    const post = posts.value.find(p => p.id === id)
    if (post) post.status = 'draft'
  } catch {
    alert('Failed to restore post.')
  }
  actionInProgress.value = null
}

async function deleteForever(id) {
  if (!confirm('Permanently delete this post? This cannot be undone.')) return
  actionInProgress.value = id
  try {
    await fetch('/api/posts/' + id, { method: 'DELETE' })
    posts.value = posts.value.filter(p => p.id !== id)
  } catch {
    alert('Failed to delete post.')
  }
  actionInProgress.value = null
}

async function emptyTrash() {
  const count = trashedPosts.value.length
  if (!count) return
  if (!confirm(`Permanently delete ${count} trashed post${count > 1 ? 's' : ''}? This cannot be undone.`)) return
  saving.value = true
  let failed = 0
  const toDelete = [...trashedPosts.value]
  for (const p of toDelete) {
    try {
      await fetch('/api/posts/' + p.id, { method: 'DELETE' })
      posts.value = posts.value.filter(x => x.id !== p.id)
    } catch {
      failed++
    }
  }
  saving.value = false
  if (failed) alert(`${failed} post${failed > 1 ? 's' : ''} could not be deleted.`)
}

onMounted(async () => {
  try { posts.value = await (await fetch('/api/posts?status=all')).json() } catch { posts.value = [] }
})
</script>
