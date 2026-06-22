<template>
  <div class="p-6 max-w-3xl">
    <h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-white">⚙️ Settings</h1>

    <!-- Change Username -->
    <section class="bg-white dark:bg-slate-800 rounded-xl p-6 mb-6 border border-gray-200 dark:border-slate-700">
      <h2 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Change Username</h2>
      <form @submit.prevent="changeUsername" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">New Username</label>
          <input v-model="usernameForm.newUsername" type="text" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white outline-none" required minlength="3">
        </div>
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Current Password</label>
          <input v-model="usernameForm.password" type="password" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white outline-none" required>
        </div>
        <p v-if="usernameMsg" :class="usernameOk ? 'text-green-600' : 'text-red-500'" class="text-sm">{{ usernameMsg }}</p>
        <button type="submit" class="px-5 py-2 rounded-lg text-white font-medium" style="background:var(--color-brand)">Update Username</button>
      </form>
    </section>

    <!-- Change Password -->
    <section class="bg-white dark:bg-slate-800 rounded-xl p-6 mb-6 border border-gray-200 dark:border-slate-700">
      <h2 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Change Password</h2>
      <form @submit.prevent="changePassword" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">Current Password</label>
          <input v-model="passwordForm.oldPassword" type="password" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white outline-none" required>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-slate-300">New Password</label>
          <input v-model="passwordForm.newPassword" type="password" class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white outline-none" required minlength="6">
        </div>
        <p v-if="passwordMsg" :class="passwordOk ? 'text-green-600' : 'text-red-500'" class="text-sm">{{ passwordMsg }}</p>
        <button type="submit" class="px-5 py-2 rounded-lg text-white font-medium" style="background:var(--color-brand)">Update Password</button>
      </form>
    </section>

    <!-- Quick Links to edit pages -->
    <section class="bg-white dark:bg-slate-800 rounded-xl p-6 border border-gray-200 dark:border-slate-700">
      <h2 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Site Pages</h2>
      <p class="text-sm text-gray-500 dark:text-slate-400 mb-4">Edit the content of your static pages using Markdown or HTML.</p>
      <div class="space-y-2">
        <router-link v-for="p in pages" :key="p.id" :to="'/admin/pages/edit/' + p.id"
          class="flex items-center justify-between px-4 py-3 rounded-lg border border-gray-100 dark:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-700/50 no-underline">
          <span class="font-medium text-gray-900 dark:text-white">{{ p.title }}</span>
          <span class="text-xs text-gray-400">{{ p.slug }}</span>
        </router-link>
        <div v-if="!pages.length" class="text-sm text-gray-400 py-4 text-center">
          No pages yet. Go to <router-link to="/admin/pages" class="text-brand">Static Pages</router-link> to manage.
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const pages = ref([])
const usernameForm = ref({ newUsername: '', password: '' })
const passwordForm = ref({ oldPassword: '', newPassword: '' })
const usernameMsg = ref('')
const usernameOk = ref(false)
const passwordMsg = ref('')
const passwordOk = ref(false)

onMounted(async () => {
  try { pages.value = await (await fetch('/api/pages')).json() } catch { pages.value = [] }
})

async function changeUsername() {
  usernameMsg.value = ''
  try {
    const resp = await fetch('/api/admin/change-username', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ new_username: usernameForm.value.newUsername, password: usernameForm.value.password })
    })
    const data = await resp.json()
    if (data.ok) {
      usernameMsg.value = `Username changed to "${data.username}"`
      usernameOk.value = true
      localStorage.setItem('admin_username', data.username)
      usernameForm.value = { newUsername: '', password: '' }
    } else {
      usernameMsg.value = data.error || 'Failed to change username'
      usernameOk.value = false
    }
  } catch { usernameMsg.value = 'Network error'; usernameOk.value = false }
}

async function changePassword() {
  passwordMsg.value = ''
  try {
    const resp = await fetch('/api/admin/change-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ old_password: passwordForm.value.oldPassword, new_password: passwordForm.value.newPassword })
    })
    const data = await resp.json()
    if (data.ok) {
      passwordMsg.value = 'Password changed successfully!'
      passwordOk.value = true
      passwordForm.value = { oldPassword: '', newPassword: '' }
    } else {
      passwordMsg.value = data.error || 'Failed to change password'
      passwordOk.value = false
    }
  } catch { passwordMsg.value = 'Network error'; passwordOk.value = false }
}
</script>
