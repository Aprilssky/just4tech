<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-white">✉️ Messages</h1>

    <div v-if="error" class="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-xl p-4 mb-6 text-sm text-red-700 dark:text-red-300">{{ error }}</div>

    <div v-else-if="loading" class="text-center py-12 text-gray-500 dark:text-slate-400">Loading messages...</div>

    <div v-else-if="!messages.length" class="text-center py-16 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700">
      <div class="text-5xl mb-4">📭</div>
      <p class="text-gray-500 dark:text-slate-400 mb-1">No messages yet</p>
      <p class="text-xs text-gray-400 dark:text-slate-500">Contact form submissions will appear here</p>
    </div>

    <div v-else class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden">
      <table class="w-full text-sm">
        <thead><tr class="bg-gray-50 dark:bg-slate-700 text-left font-semibold text-gray-600 dark:text-slate-300"><th class="p-4">From</th><th class="p-4 hidden md:table-cell">Subject</th><th class="p-4 hidden md:table-cell">Date</th><th class="p-4">Message</th><th class="p-4 w-20">Action</th></tr></thead>
        <tbody>
          <tr v-for="m in messages" :key="m.id" class="border-t border-gray-100 dark:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-700/50">
            <td class="p-4"><span class="font-medium text-gray-900 dark:text-white">{{ m.name }}</span><br><span class="text-xs text-gray-500">{{ m.email }}</span></td>
            <td class="p-4 text-gray-600 dark:text-slate-400 hidden md:table-cell"><span class="px-2 py-0.5 rounded-full text-xs bg-gray-100 dark:bg-slate-700">{{ m.subject }}</span></td>
            <td class="p-4 text-gray-500 dark:text-slate-400 text-xs hidden md:table-cell whitespace-nowrap">{{ m.created_at?.slice(0, 10) }}</td>
            <td class="p-4 text-gray-600 dark:text-slate-400 text-sm max-w-xs truncate">{{ m.message }}</td>
            <td class="p-4">
              <button @click="deleteMsg(m.id)" class="text-xs font-medium text-red-500 hover:text-red-700 hover:underline" :disabled="deleting === m.id">
                {{ deleting === m.id ? '...' : '🗑 Delete' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const messages = ref([])
const loading = ref(true)
const error = ref('')
const deleting = ref(null)

async function deleteMsg(id) {
  if (!confirm('Delete this message?')) return
  deleting.value = id
  try {
    await fetch('/api/admin/contact-messages/' + id, { method: 'DELETE' })
    messages.value = messages.value.filter(m => m.id !== id)
  } catch { alert('Delete failed') }
  deleting.value = null
}

onMounted(async () => {
  try {
    const resp = await fetch('/api/admin/contact-messages')
    if (!resp.ok) throw new Error(resp.status === 401 ? 'Please log in again' : `Server error (${resp.status})`)
    messages.value = await resp.json()
  } catch (e) {
    error.value = e.message
  }
  loading.value = false
})
</script>
