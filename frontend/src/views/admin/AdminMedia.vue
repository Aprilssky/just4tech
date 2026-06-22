<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">🖼 Media Library</h1>
      <span class="text-xs text-gray-400 dark:text-slate-500">{{ files.length }} files</span>
    </div>

    <!-- Upload area -->
    <label class="block mb-8 p-8 border-2 border-dashed border-gray-300 dark:border-slate-600 rounded-xl text-center cursor-pointer hover:border-amber-400 dark:hover:border-amber-500 transition-colors bg-white dark:bg-slate-800"
      :class="{ 'opacity-50': uploading }">
      <div class="text-3xl mb-2">{{ uploading ? '⏳' : '📤' }}</div>
      <p class="text-gray-700 dark:text-slate-300 font-medium">{{ uploading ? 'Uploading...' : 'Click or drag to upload' }}</p>
      <p class="text-xs text-gray-400 mt-1">PNG, JPG, GIF, WebP, SVG · Max 5MB</p>
      <input type="file" accept="image/*" @change="handleUpload" class="hidden" :disabled="uploading">
    </label>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-12 text-gray-500">Loading...</div>

    <!-- Empty -->
    <div v-else-if="!files.length" class="text-center py-16 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700">
      <div class="text-5xl mb-4">📭</div>
      <p class="text-gray-500">No media files yet</p>
    </div>

    <!-- Grid -->
    <div v-else class="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
      <div v-for="f in files" :key="f.filename"
        class="group relative bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden hover:shadow-lg transition-all">
        <!-- Image -->
        <div class="aspect-square bg-gray-100 dark:bg-slate-700 flex items-center justify-center overflow-hidden">
          <img :src="f.url" :alt="f.filename" class="w-full h-full object-cover" loading="lazy">
        </div>
        <!-- Info overlay on hover -->
        <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-2 p-2">
          <p class="text-white text-xs font-mono truncate w-full text-center">{{ f.filename }}</p>
          <p class="text-gray-300 text-xs">{{ f.size_display }}</p>
          <div class="flex gap-2 mt-1">
            <button @click="copyUrl(f.url)" class="px-2 py-1 text-xs rounded bg-white/20 text-white hover:bg-white/30">📋 Copy URL</button>
            <button @click="deleteFile(f)" class="px-2 py-1 text-xs rounded bg-red-500/60 text-white hover:bg-red-500/80">🗑</button>
          </div>
        </div>
        <!-- Filename below -->
        <div class="p-2">
          <p class="text-xs text-gray-500 dark:text-slate-400 truncate" :title="f.filename">{{ f.filename }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const files = ref([])
const loading = ref(true)
const uploading = ref(false)

async function loadFiles() {
  try {
    const resp = await fetch('/api/admin/media')
    if (resp.ok) {
      const data = await resp.json()
      files.value = data.files || []
    }
  } catch {}
  loading.value = false
}

async function handleUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('file', file)
    const resp = await fetch('/api/admin/upload', { method: 'POST', body: fd })
    if ((await resp.json()).ok) await loadFiles()
  } catch {}
  uploading.value = false
}

async function deleteFile(f) {
  if (!confirm('Delete ' + f.filename + '?')) return
  try {
    await fetch('/api/admin/media/' + f.filename, { method: 'DELETE' })
    files.value = files.value.filter(x => x.filename !== f.filename)
  } catch { alert('Delete failed') }
}

function copyUrl(url) {
  const full = 'https://just4.tech' + url
  navigator.clipboard.writeText(full).then(() => {
    alert('Copied: ' + full)
  }).catch(() => {
    prompt('Copy this URL:', full)
  })
}

onMounted(loadFiles)
</script>
