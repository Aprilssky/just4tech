<template>
  <div class="p-6 max-w-5xl">
    <router-link to="/admin/posts" class="text-sm mb-4 inline-block" style="color:var(--color-brand)">← Back to Posts</router-link>
    <h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-white">{{ isNew ? 'New Post' : 'Edit Post' }}</h1>

    <form @submit.prevent="save" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Title</label>
          <input v-model="title" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none" required>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Slug</label>
          <input v-model="slug" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none" required>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Category</label>
          <select v-model="category" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none">
            <optgroup label="Blog"><option value="Tutorial">Tutorial</option><option value="Vibe Coding">Vibe Coding</option><option value="Indie Diary">Indie Diary</option><option value="Dev Tools">Dev Tools</option></optgroup>
            <optgroup label="Content"><option value="AI Tool">🤖 AI Tool</option><option value="Project">🚀 Project</option><option value="Indie Dev">🌟 Indie Dev</option><option value="Site">🌐 Personal Site</option></optgroup>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Status</label>
          <select v-model="status" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none">
            <option value="active">Active</option><option value="draft">Draft</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Cover Image</label>
          <div class="flex gap-2">
            <input v-model="cover_image" class="flex-1 px-3 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none text-sm" placeholder="URL or pick from media">
            <label class="inline-flex items-center gap-1 px-3 py-2 rounded-lg text-sm font-medium cursor-pointer text-white transition-colors" style="background:var(--color-brand)" :class="{ 'opacity-50': uploading }">
              <span v-if="uploading">⏳</span>
              <span v-else>📷</span>
              <span class="hidden sm:inline">Upload</span>
              <input type="file" accept="image/*" @change="handleUpload" class="hidden" :disabled="uploading">
            </label>
            <button type="button" @click="showMediaPicker = !showMediaPicker"
              class="inline-flex items-center gap-1 px-3 py-2 rounded-lg text-sm font-medium border border-gray-300 dark:border-slate-600 text-gray-700 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors">
              🖼 <span class="hidden sm:inline">Browse</span>
            </button>
          </div>
          <div v-if="cover_image" class="mt-2">
            <img :src="cover_image" class="h-20 rounded border border-gray-200 dark:border-slate-600 object-cover" alt="Cover preview">
          </div>
          <!-- Media Picker -->
          <div v-if="showMediaPicker" class="mt-3 p-4 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 max-h-64 overflow-y-auto">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-medium text-gray-700 dark:text-slate-300">Recent uploads</span>
              <button type="button" @click="showMediaPicker = false" class="text-xs text-gray-400 hover:text-gray-600">✕ Close</button>
            </div>
            <div v-if="mediaLoading" class="text-xs text-gray-400 py-4 text-center">Loading...</div>
            <div v-else-if="!mediaFiles.length" class="text-xs text-gray-400 py-4 text-center">No images yet. Upload one above.</div>
            <div v-else class="grid grid-cols-4 gap-2">
              <div v-for="f in mediaFiles" :key="f.filename"
                @click="cover_image = f.url; showMediaPicker = false"
                class="aspect-square rounded-lg overflow-hidden border-2 cursor-pointer hover:border-amber-400 transition-colors bg-gray-100 dark:bg-slate-700"
                :class="{ 'border-amber-500': cover_image === f.url, 'border-transparent': cover_image !== f.url }">
                <img :src="f.url" :alt="f.filename" class="w-full h-full object-cover" :title="f.filename">
              </div>
            </div>
            <router-link to="/admin/media" class="inline-block mt-3 text-xs font-medium" style="color:var(--color-brand)">Open Media Library →</router-link>
          </div>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Excerpt</label>
        <input v-model="excerpt" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none">
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Icon (emoji or image URL)</label>
          <input v-model="icon" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none" placeholder="🤖  or  https://example.com/icon.png">
          <div v-if="icon && /^https?:\/\//.test(icon)" class="mt-2"><img :src="icon" class="h-8 w-8 rounded object-cover border" alt="Icon preview"></div>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Subtitle</label>
          <input v-model="subtitle" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none" placeholder="Freemium · Web">
        </div>
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">External Link</label>
          <input v-model="external_url" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none" placeholder="https://...">
        </div>
      </div>

      <!-- Markdown Editor with tabs -->
      <div>
        <div class="flex items-center justify-between mb-1">
          <label class="text-sm font-medium text-gray-700 dark:text-slate-300">Content (Markdown)</label>
          <div class="flex gap-1">
            <button type="button" @click="tab='edit'" :class="tab==='edit' ? 'bg-white dark:bg-slate-800 font-semibold shadow-sm' : 'bg-gray-100 dark:bg-slate-700 text-gray-500'" class="px-3 py-1.5 rounded-t-lg border border-gray-200 dark:border-slate-600 text-xs">✏️ Edit</button>
            <button type="button" @click="tab='preview'" :class="tab==='preview' ? 'bg-white dark:bg-slate-800 font-semibold shadow-sm' : 'bg-gray-100 dark:bg-slate-700 text-gray-500'" class="px-3 py-1.5 rounded-t-lg border border-gray-200 dark:border-slate-600 text-xs">👁 Preview</button>
            <button type="button" @click="tab='split'" :class="tab==='split' ? 'bg-white dark:bg-slate-800 font-semibold shadow-sm' : 'bg-gray-100 dark:bg-slate-700 text-gray-500'" class="px-3 py-1.5 rounded-t-lg border border-gray-200 dark:border-slate-600 text-xs">↔ Split</button>
          </div>
        </div>

        <div class="flex gap-0">
          <div v-show="tab==='edit' || tab==='split'" :class="tab==='split' ? 'w-1/2 border-r border-gray-200 dark:border-slate-600' : 'w-full'">
            <textarea v-model="content" rows="25"
              class="w-full px-4 py-3 border border-gray-200 dark:border-slate-600 rounded-b-lg font-mono text-sm bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none resize-y"
              placeholder="Write in Markdown..."></textarea>
          </div>
          <div v-show="tab==='preview' || tab==='split'" :class="tab==='split' ? 'w-1/2' : 'w-full'">
            <div class="px-5 py-3 border border-gray-200 dark:border-slate-600 rounded-b-lg bg-white dark:bg-slate-800 min-h-[400px] blog-content" v-html="renderedContent"></div>
          </div>
        </div>
      </div>

      <div class="flex gap-3 pt-4">
        <button type="submit" class="px-6 py-2.5 rounded-lg text-white font-medium" style="background:var(--color-brand)">Save</button>
        <button type="button" @click="$router.push('/admin/posts')" class="px-6 py-2.5 rounded-lg font-medium border border-gray-300 dark:border-slate-600 text-gray-700 dark:text-slate-300">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
const route = useRoute(); const router = useRouter()
const isNew = route.params.id === 'new'
const title = ref(''); const slug = ref(''); const category = ref('Tutorial'); const excerpt = ref('')
const content = ref(''); const cover_image = ref(''); const status = ref('active')
const icon = ref(''); const subtitle = ref(''); const external_url = ref('')
const tab = ref('edit')
const uploading = ref(false)
const showMediaPicker = ref(false)
const mediaFiles = ref([])
const mediaLoading = ref(false)

async function loadMedia() {
  mediaLoading.value = true
  try {
    const resp = await fetch('/api/admin/media')
    if (resp.ok) {
      const data = await resp.json()
      mediaFiles.value = (data.files || []).slice(0, 12)
    }
  } catch {}
  mediaLoading.value = false
}

watch(showMediaPicker, (val) => { if (val) loadMedia() })

const renderedContent = computed(() => {
  if (!content.value) return '<p style="color:#999">Nothing to preview.</p>'
  try {
    let html = marked(content.value)
    html = html.replace(/<img\s+src="([^"]+)"([^>]*)>/g, (match, src, rest) => {
      return `<a href="${src}" target="_blank" class="blog-img-link"><img src="${src}"${rest}></a>`
    })
    return html
  } catch { return '<p style="color:red">Invalid Markdown</p>' }
})

onMounted(async () => {
  if (!isNew) {
    try {
      const p = await (await fetch('/api/posts/' + route.params.id)).json()
      title.value = p.title; slug.value = p.slug; category.value = p.category; excerpt.value = p.excerpt
      content.value = p.content; cover_image.value = p.cover_image || ''; status.value = p.status
      icon.value = p.icon || ''; subtitle.value = p.subtitle || ''; external_url.value = p.external_url || ''
    } catch {}
  }
})

async function handleUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const resp = await fetch('/api/admin/upload', { method: 'POST', body: formData })
    const data = await resp.json()
    if (data.ok) cover_image.value = data.url
    else alert(data.error || 'Upload failed')
  } catch { alert('Upload failed - network error') }
  uploading.value = false
}

async function save() {
  const resp = await fetch(isNew ? '/api/posts' : '/api/posts/' + route.params.id, {
    method: isNew ? 'POST' : 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ slug: slug.value, title: title.value, category: category.value, excerpt: excerpt.value, content: content.value, cover_image: cover_image.value, status: status.value, icon: icon.value, subtitle: subtitle.value, external_url: external_url.value })
  })
  const data = await resp.json()
  if (data.ok) router.push('/admin/posts')
}
</script>
