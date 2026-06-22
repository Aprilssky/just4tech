<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-slate-900">
    <div class="bg-white dark:bg-slate-800 p-8 rounded-xl shadow-lg w-full max-w-sm">
      <div class="text-center mb-8">
        <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white font-bold text-lg mx-auto mb-3"
             style="background:linear-gradient(135deg,var(--color-brand),var(--color-accent2))">JT</div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Admin Login</h1>
        <p class="text-gray-500 dark:text-slate-400 text-sm mt-1">Just4Tech Management</p>
      </div>
      <form @submit.prevent="login" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Username</label>
          <input v-model="form.username" type="text" class="w-full px-4 py-2 border border-gray-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white outline-none" required>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Password</label>
          <input v-model="form.password" type="password" class="w-full px-4 py-2 border border-gray-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white outline-none" required>
        </div>
        <div v-if="error" class="text-red-600 text-sm">{{ error }}</div>
        <button type="submit" :disabled="loading"
          class="w-full py-2.5 rounded-lg font-semibold transition-colors"
          :style="{ background: 'var(--color-brand)', color: 'white' }">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = reactive({ username: '', password: '' })
const error = ref('')
const loading = ref(false)

async function login() {
  error.value = ''
  loading.value = true
  try {
    const resp = await fetch('/api/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    const data = await resp.json()
    if (data.ok) {
      localStorage.setItem('admin_username', form.username)
      router.push('/admin/dashboard')
    } else {
      error.value = data.error || 'Login failed'
    }
  } catch {
    error.value = 'Network error'
  }
  loading.value = false
}
</script>
