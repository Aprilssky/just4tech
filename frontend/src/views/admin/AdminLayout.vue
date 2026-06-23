<template>
  <div class="flex min-h-screen bg-gray-50 dark:bg-slate-900">
    <!-- Sidebar -->
    <aside class="w-56 bg-gray-900 text-white flex flex-col flex-shrink-0">
      <div class="p-5 border-b border-gray-800">
        <router-link to="/" class="flex items-center gap-2 font-bold no-underline text-white">
          <span class="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-xs" style="background:linear-gradient(135deg,#d55c3a,#e8874a)">J4</span>
          <span>Admin</span>
        </router-link>
      </div>
      <nav class="flex-1 p-3 space-y-0.5 overflow-y-auto text-sm">
        <router-link to="/admin/dashboard" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800 no-underline transition-colors">📊 Dashboard</router-link>
        <router-link to="/admin/posts" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800 no-underline transition-colors">📝 Posts (All Content)</router-link>
        <router-link to="/admin/pages" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800 no-underline transition-colors">📄 Pages</router-link>
        <router-link to="/admin/media" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800 no-underline transition-colors">🖼 Media</router-link>
        <router-link to="/admin/messages" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800 no-underline transition-colors">✉️ Messages</router-link>
        <router-link to="/admin/settings" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800 no-underline transition-colors">⚙️ Settings</router-link>
      </nav>
      <div class="p-4 border-t border-gray-800">
        <div class="text-xs text-gray-500 mb-2">Logged in as <span class="text-gray-400">{{ username }}</span></div>
        <button @click="logout" class="w-full text-left px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 text-sm transition-colors">↪ Sign Out</button>
      </div>
    </aside>
    <main class="flex-1 min-w-0">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('Admin')

onMounted(async () => {
  // Verify session is still valid, redirect to login if not
  try {
    const resp = await fetch('/api/admin/session-status')
    const data = await resp.json()
    if (!data.authenticated) {
      router.push('/admin/login')
    } else if (data.user) {
      username.value = data.user
    }
  } catch {
    // Network error — still show layout, API calls will fail individually
  }
})

async function logout() {
  try { await fetch('/api/admin/logout', { method: 'POST' }) } catch {}
  router.push('/admin/login')
}
</script>

<style scoped>
.router-link-exact-active { background: rgb(55 55 55 / 0.6); color: white !important; font-weight: 600; }
</style>
