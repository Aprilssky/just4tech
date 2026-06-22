<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-slate-900 dark:text-white">URL Encoder / Decoder</h2>
      <p class="text-slate-600 dark:text-slate-400 mt-1">Encode and decode full URLs or URL components.</p>
    </div>

    <div class="space-y-4">
      <div class="flex flex-wrap gap-4">
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="radio" v-model="mode" value="component" class="border-slate-300 dark:border-slate-600 text-amber-600 focus:ring-amber-500">
          <span class="text-sm text-slate-700 dark:text-slate-300">Component</span>
        </label>
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="radio" v-model="mode" value="full" class="border-slate-300 dark:border-slate-600 text-amber-600 focus:ring-amber-500">
          <span class="text-sm text-slate-700 dark:text-slate-300">Full URL</span>
        </label>
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Input</label>
        <textarea
          v-model="input"
          class="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none resize-y min-h-[80px] font-mono text-sm"
          placeholder="https://example.com?q=hello world&lang=en"
          rows="4"
        ></textarea>
      </div>

      <div class="flex flex-wrap gap-2">
        <button @click="encode" class="px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-amber-600 hover:bg-amber-700 transition">Encode</button>
        <button @click="decode" class="px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-emerald-600 hover:bg-emerald-700 transition">Decode</button>
        <button @click="swap" class="px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-slate-600 hover:bg-slate-700 transition">Swap</button>
        <button @click="clear" class="px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-red-500 hover:bg-red-600 transition">Clear</button>
      </div>

      <div v-if="error" class="p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 text-sm font-mono">
        {{ error }}
      </div>

      <div v-if="output" class="space-y-2">
        <div class="flex items-center justify-between">
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Result</label>
          <button @click="copyOutput" class="text-xs text-amber-600 dark:text-amber-400 hover:underline">{{ copied ? 'Copied!' : 'Copy' }}</button>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 font-mono text-sm break-all">{{ output }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const mode = ref('component')
const input = ref('')
const output = ref('')
const error = ref('')
const copied = ref(false)

function encode() {
  error.value = ''
  if (!input.value) { error.value = 'Please enter text to encode.'; return }
  try {
    if (mode.value === 'component') {
      output.value = encodeURIComponent(input.value)
    } else {
      output.value = encodeURI(input.value)
    }
  } catch (e) {
    error.value = 'Encoding failed: ' + e.message
  }
}

function decode() {
  error.value = ''
  if (!input.value) { error.value = 'Please enter text to decode.'; return }
  try {
    if (mode.value === 'component') {
      output.value = decodeURIComponent(input.value.trim())
    } else {
      output.value = decodeURI(input.value.trim())
    }
  } catch (e) {
    error.value = 'Decoding failed: malformed URI'
  }
}

function swap() {
  const tmp = input.value
  input.value = output.value
  output.value = tmp
  error.value = ''
}

function clear() {
  input.value = ''
  output.value = ''
  error.value = ''
  copied.value = false
}

async function copyOutput() {
  if (!output.value) return
  try {
    await navigator.clipboard.writeText(output.value)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch {}
}
</script>
