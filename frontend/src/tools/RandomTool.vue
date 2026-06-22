<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Random Number Generator</h2>
      <p class="text-slate-600 dark:text-slate-400 mt-1">Generate random integers or decimals within a specified range.</p>
    </div>

    <div class="space-y-4">
      <div class="flex flex-wrap gap-4">
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="radio" v-model="mode" value="integer" class="border-slate-300 dark:border-slate-600 text-amber-600 focus:ring-amber-500">
          <span class="text-sm text-slate-700 dark:text-slate-300">Integer</span>
        </label>
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="radio" v-model="mode" value="decimal" class="border-slate-300 dark:border-slate-600 text-amber-600 focus:ring-amber-500">
          <span class="text-sm text-slate-700 dark:text-slate-300">Decimal</span>
        </label>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Min</label>
          <input type="number" v-model.number="min" class="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none">
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Max</label>
          <input type="number" v-model.number="max" class="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none">
        </div>
      </div>

      <div v-if="mode === 'decimal'">
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Decimal Places</label>
        <input type="number" v-model.number="decimals" min="0" max="10" class="w-32 px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none">
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Count</label>
        <select v-model.number="count" class="w-32 px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none">
          <option :value="1">1</option>
          <option :value="5">5</option>
          <option :value="10">10</option>
          <option :value="25">25</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
      </div>

      <div class="flex flex-wrap gap-2">
        <button @click="generate" class="px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-amber-600 hover:bg-amber-700 transition">Generate</button>
        <button @click="copyResults" class="px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-slate-600 hover:bg-slate-700 transition" :disabled="!results.length">{{ copied ? 'Copied!' : 'Copy' }}</button>
      </div>

      <div v-if="error" class="p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 text-sm">
        {{ error }}
      </div>

      <div v-if="results.length" class="space-y-2">
        <div class="flex items-center justify-between">
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Results</label>
          <span class="text-xs text-slate-400">Sum: {{ sum }} | Avg: {{ average }}</span>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 font-mono text-sm break-all space-y-1">
          <div v-for="(r, i) in results" :key="i" class="py-0.5">{{ r }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const mode = ref('integer')
const min = ref(1)
const max = ref(100)
const decimals = ref(2)
const count = ref(1)
const results = ref([])
const error = ref('')
const copied = ref(false)

const sum = computed(() => {
  if (!results.value.length) return 0
  return results.value.reduce((a, b) => a + b, 0).toFixed(mode.value === 'decimal' ? decimals.value : 0)
})

const average = computed(() => {
  if (!results.value.length) return 0
  return (results.value.reduce((a, b) => a + b, 0) / results.value.length).toFixed(mode.value === 'decimal' ? decimals.value : 0)
})

function generate() {
  error.value = ''
  copied.value = false
  if (min.value >= max.value) {
    error.value = 'Min must be less than Max.'
    return
  }
  const items = []
  for (let i = 0; i < count.value; i++) {
    let val
    if (mode.value === 'integer') {
      val = Math.floor(Math.random() * (max.value - min.value + 1)) + min.value
    } else {
      val = Math.random() * (max.value - min.value) + min.value
      val = parseFloat(val.toFixed(decimals.value))
    }
    items.push(val)
  }
  results.value = items
}

async function copyResults() {
  if (!results.value.length) return
  try {
    await navigator.clipboard.writeText(results.value.join('\n'))
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch {}
}
</script>
