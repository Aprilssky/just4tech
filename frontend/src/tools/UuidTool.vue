<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-slate-900 dark:text-white">UUID Generator</h2>
      <p class="text-slate-600 dark:text-slate-400 mt-1">Generate random UUID v4 identifiers with optional formatting.</p>
    </div>

    <div class="space-y-4">
      <div class="flex flex-wrap gap-4">
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="uppercase" class="rounded border-slate-300 dark:border-slate-600 text-amber-600 focus:ring-amber-500">
          <span class="text-sm text-slate-700 dark:text-slate-300">Uppercase</span>
        </label>
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="noDashes" class="rounded border-slate-300 dark:border-slate-600 text-amber-600 focus:ring-amber-500">
          <span class="text-sm text-slate-700 dark:text-slate-300">No Dashes</span>
        </label>
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Count</label>
        <select v-model.number="count" class="w-32 px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none">
          <option :value="1">1</option>
          <option :value="5">5</option>
          <option :value="10">10</option>
          <option :value="25">25</option>
          <option :value="50">50</option>
        </select>
      </div>

      <div class="flex flex-wrap gap-2">
        <button @click="generate" class="px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-amber-600 hover:bg-amber-700 transition">Generate</button>
        <button @click="copyAll" class="px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-slate-600 hover:bg-slate-700 transition" :disabled="!uuids.length">{{ copied ? 'Copied!' : 'Copy All' }}</button>
      </div>

      <div v-if="uuids.length" class="space-y-2">
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 font-mono text-sm break-all space-y-1">
          <div v-for="(uuid, i) in uuids" :key="i" class="py-1">{{ uuid }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const uppercase = ref(false)
const noDashes = ref(false)
const count = ref(1)
const uuids = ref([])
const copied = ref(false)

function generateUuid() {
  const hex = '0123456789abcdef'
  let uuid = ''
  for (let i = 0; i < 36; i++) {
    if (i === 8 || i === 13 || i === 18 || i === 23) {
      uuid += '-'
    } else if (i === 14) {
      uuid += '4'
    } else if (i === 19) {
      uuid += hex[(Math.random() * 4) | 0 + 8]
    } else {
      uuid += hex[(Math.random() * 16) | 0]
    }
  }
  return uuid
}

function generate() {
  const items = []
  for (let i = 0; i < count.value; i++) {
    let uuid = generateUuid()
    if (noDashes.value) uuid = uuid.replace(/-/g, '')
    if (uppercase.value) uuid = uuid.toUpperCase()
    items.push(uuid)
  }
  uuids.value = items
  copied.value = false
}

async function copyAll() {
  if (!uuids.value.length) return
  try {
    await navigator.clipboard.writeText(uuids.value.join('\n'))
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch {}
}
</script>
