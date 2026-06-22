<template>
  <div class="p-6 max-w-5xl">
    <router-link to="/admin/pages" class="text-sm mb-4 inline-block" style="color:var(--color-brand)">← Back</router-link>
    <h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Edit Page</h1>

    <form @submit.prevent="save" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Title</label>
          <input v-model="title" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none" required>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Slug</label>
          <input v-model="slug" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none" disabled>
        </div>
      </div>

      <!-- Editor Tabs -->
      <div>
        <div class="flex gap-2 mb-2">
          <button type="button" @click="tab='edit'" :class="tab==='edit' ? 'bg-white dark:bg-slate-800 border-b-0 font-semibold' : 'bg-gray-100 dark:bg-slate-700 text-gray-500'" class="px-4 py-2 rounded-t-lg border border-gray-200 dark:border-slate-600 text-sm">✏️ Edit (Markdown)</button>
          <button type="button" @click="tab='preview'" :class="tab==='preview' ? 'bg-white dark:bg-slate-800 border-b-0 font-semibold' : 'bg-gray-100 dark:bg-slate-700 text-gray-500'" class="px-4 py-2 rounded-t-lg border border-gray-200 dark:border-slate-600 text-sm">👁 Preview</button>
          <button type="button" @click="tab='split'" :class="tab==='split' ? 'bg-white dark:bg-slate-800 border-b-0 font-semibold' : 'bg-gray-100 dark:bg-slate-700 text-gray-500'" class="px-4 py-2 rounded-t-lg border border-gray-200 dark:border-slate-600 text-sm">↔ Split</button>
        </div>

        <div v-show="tab==='edit' || tab==='split'" :class="tab==='split' ? 'w-1/2' : 'w-full'">
          <textarea v-model="content" rows="30"
            class="w-full px-4 py-3 border border-gray-200 dark:border-slate-600 rounded-b-lg font-mono text-sm bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none resize-y"
            placeholder="Write your content in Markdown..."></textarea>
        </div>

        <div v-show="tab==='preview' || tab==='split'" :class="tab==='split' ? 'w-1/2' : 'w-full'" class="blog-content">
          <div v-if="tab==='split'" style="margin-left:-1px">
            <div class="px-4 py-3 border border-gray-200 dark:border-slate-600 rounded-b-lg bg-white dark:bg-slate-800 min-h-[400px] blog-content" v-html="renderedContent"></div>
          </div>
          <div v-else class="px-4 py-3 border border-gray-200 dark:border-slate-600 rounded-b-lg bg-white dark:bg-slate-800 min-h-[400px] blog-content" v-html="renderedContent"></div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div><label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Meta Title (SEO)</label><input v-model="metaTitle" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none"></div>
        <div><label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Meta Description (SEO)</label><input v-model="metaDesc" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-gray-900 dark:text-white outline-none"></div>
      </div>

      <div class="flex gap-3 pt-4">
        <button type="submit" class="px-6 py-2.5 rounded-lg text-white font-medium" style="background:var(--color-brand)">Save Changes</button>
        <button type="button" @click="$router.push('/admin/pages')" class="px-6 py-2.5 rounded-lg font-medium border border-gray-300 dark:border-slate-600 text-gray-700 dark:text-slate-300">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'

const route = useRoute(); const router = useRouter()
const title = ref(''); const slug = ref(''); const content = ref('')
const metaTitle = ref(''); const metaDesc = ref('')
const tab = ref('edit')

const renderedContent = computed(() => {
  if (!content.value) return '<p style="color:#999">Nothing to preview.</p>'
  try { return marked(content.value) } catch { return '<p style="color:red">Invalid Markdown</p>' }
})

onMounted(async () => {
  try {
    const p = await (await fetch('/api/pages/' + route.params.id)).json()
    title.value = p.title; slug.value = p.slug; content.value = p.content || ''
    metaTitle.value = p.meta_title || ''; metaDesc.value = p.meta_description || ''
  } catch {}
})

async function save() {
  const resp = await fetch('/api/pages/' + route.params.id, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: title.value,
      content: content.value,
      meta_title: metaTitle.value,
      meta_description: metaDesc.value
    })
  })
  const data = await resp.json()
  if (data.ok) router.push('/admin/pages')
}
</script>
