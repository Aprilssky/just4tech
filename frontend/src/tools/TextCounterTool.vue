<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Text Counter</h2>
      <p class="text-slate-600 dark:text-slate-400 mt-1">Real-time character, word, line, and paragraph counting.</p>
    </div>

    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Input Text</label>
        <textarea
          v-model="text"
          class="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none resize-y min-h-[120px] font-mono text-sm"
          placeholder="Type or paste your text here..."
          rows="8"
        ></textarea>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">Characters</div>
          <div class="text-xl font-bold text-slate-900 dark:text-white">{{ charCount }}</div>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">Characters (no spaces)</div>
          <div class="text-xl font-bold text-slate-900 dark:text-white">{{ charNoSpace }}</div>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">Words</div>
          <div class="text-xl font-bold text-slate-900 dark:text-white">{{ wordCount }}</div>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">Lines</div>
          <div class="text-xl font-bold text-slate-900 dark:text-white">{{ lineCount }}</div>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">Paragraphs</div>
          <div class="text-xl font-bold text-slate-900 dark:text-white">{{ paragraphCount }}</div>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">Sentences</div>
          <div class="text-xl font-bold text-slate-900 dark:text-white">{{ sentenceCount }}</div>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">Digits</div>
          <div class="text-xl font-bold text-slate-900 dark:text-white">{{ digitCount }}</div>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">Letters</div>
          <div class="text-xl font-bold text-slate-900 dark:text-white">{{ letterCount }}</div>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">Spaces</div>
          <div class="text-xl font-bold text-slate-900 dark:text-white">{{ spaceCount }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const text = ref('')

const charCount = computed(() => text.value.length)
const charNoSpace = computed(() => text.value.replace(/\s/g, '').length)
const wordCount = computed(() => {
  const trimmed = text.value.trim()
  return trimmed ? trimmed.split(/\s+/).length : 0
})
const lineCount = computed(() => {
  if (!text.value) return 0
  return text.value.split('\n').length
})
const paragraphCount = computed(() => {
  if (!text.value.trim()) return 0
  return text.value.split(/\n\s*\n/).filter(p => p.trim()).length
})
const sentenceCount = computed(() => {
  const trimmed = text.value.trim()
  if (!trimmed) return 0
  const matches = trimmed.match(/[^.!?]*[.!?]+/g)
  return matches ? matches.length : (trimmed.length > 0 ? 1 : 0)
})
const digitCount = computed(() => {
  const matches = text.value.match(/\d/g)
  return matches ? matches.length : 0
})
const letterCount = computed(() => {
  const matches = text.value.match(/[a-zA-Z]/g)
  return matches ? matches.length : 0
})
const spaceCount = computed(() => {
  const matches = text.value.match(/\s/g)
  return matches ? matches.length : 0
})
</script>
