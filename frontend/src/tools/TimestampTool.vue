<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Timestamp Converter</h2>
      <p class="text-slate-600 dark:text-slate-400 mt-1">Convert between Unix timestamps and human-readable dates.</p>
    </div>

    <div class="space-y-6">
      <!-- Unix → Date -->
      <div class="space-y-3">
        <h3 class="text-lg font-semibold text-slate-800 dark:text-slate-200">Unix → Date</h3>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Timestamp (seconds)</label>
            <input type="number" v-model.number="unixSeconds" class="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none font-mono">
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Timestamp (milliseconds)</label>
            <input type="number" v-model.number="unixMs" class="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none font-mono">
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="setNow" class="px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-amber-600 hover:bg-amber-700 transition">Now</button>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-sm">
          <div class="grid grid-cols-2 gap-2">
            <div><span class="text-slate-500 dark:text-slate-400">UTC:</span> <span class="font-mono text-slate-900 dark:text-white">{{ dateFromUnixUtc }}</span></div>
            <div><span class="text-slate-500 dark:text-slate-400">Local:</span> <span class="font-mono text-slate-900 dark:text-white">{{ dateFromUnixLocal }}</span></div>
            <div><span class="text-slate-500 dark:text-slate-400">ISO:</span> <span class="font-mono text-slate-900 dark:text-white">{{ dateFromUnixIso }}</span></div>
          </div>
        </div>
      </div>

      <hr class="border-slate-200 dark:border-slate-700">

      <!-- Date → Unix -->
      <div class="space-y-3">
        <h3 class="text-lg font-semibold text-slate-800 dark:text-slate-200">Date → Unix</h3>
        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Date & Time</label>
          <input type="datetime-local" v-model="dateInput" class="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none">
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-sm">
            <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">Seconds</div>
            <div class="font-mono text-slate-900 dark:text-white text-lg">{{ unixFromDate }}</div>
          </div>
          <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-sm">
            <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">Milliseconds</div>
            <div class="font-mono text-slate-900 dark:text-white text-lg">{{ unixFromDateMs }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const unixSeconds = ref(Math.floor(Date.now() / 1000))
const unixMs = ref(Date.now())
const dateInput = ref(new Date().toISOString().slice(0, 16))

function setNow() {
  unixSeconds.value = Math.floor(Date.now() / 1000)
  unixMs.value = Date.now()
  dateInput.value = new Date().toISOString().slice(0, 16)
}

// Keep seconds/ms in sync (user edits one, update the other)
function syncFromSeconds() {
  unixMs.value = unixSeconds.value * 1000
}

function syncFromMs() {
  unixSeconds.value = Math.floor(unixMs.value / 1000)
}

const dateFromUnixUtc = computed(() => {
  const d = new Date(unixSeconds.value * 1000)
  if (isNaN(d.getTime())) return 'Invalid date'
  return d.toUTCString()
})

const dateFromUnixLocal = computed(() => {
  const d = new Date(unixSeconds.value * 1000)
  if (isNaN(d.getTime())) return 'Invalid date'
  return d.toLocaleString()
})

const dateFromUnixIso = computed(() => {
  const d = new Date(unixSeconds.value * 1000)
  if (isNaN(d.getTime())) return 'Invalid date'
  return d.toISOString()
})

const unixFromDate = computed(() => {
  const d = new Date(dateInput.value)
  if (isNaN(d.getTime())) return 'Invalid date'
  return Math.floor(d.getTime() / 1000)
})

const unixFromDateMs = computed(() => {
  const d = new Date(dateInput.value)
  if (isNaN(d.getTime())) return 'Invalid date'
  return d.getTime()
})
</script>
