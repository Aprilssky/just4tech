<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Password Generator</h2>
      <p class="text-slate-600 dark:text-slate-400 mt-1">Generate secure, customizable passwords with configurable character sets.</p>
    </div>

    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Password Length: {{ length }}</label>
        <input type="range" v-model.number="length" min="4" max="128" class="w-full accent-amber-600">
        <div class="flex justify-between text-xs text-slate-400 mt-1">
          <span>4</span>
          <span>128</span>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <label class="flex items-center gap-2 cursor-pointer p-3 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800">
          <input type="checkbox" v-model="useUpper" class="rounded border-slate-300 dark:border-slate-600 text-amber-600 focus:ring-amber-500">
          <span class="text-sm text-slate-700 dark:text-slate-300">A–Z (Uppercase)</span>
        </label>
        <label class="flex items-center gap-2 cursor-pointer p-3 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800">
          <input type="checkbox" v-model="useLower" class="rounded border-slate-300 dark:border-slate-600 text-amber-600 focus:ring-amber-500">
          <span class="text-sm text-slate-700 dark:text-slate-300">a–z (Lowercase)</span>
        </label>
        <label class="flex items-center gap-2 cursor-pointer p-3 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800">
          <input type="checkbox" v-model="useDigits" class="rounded border-slate-300 dark:border-slate-600 text-amber-600 focus:ring-amber-500">
          <span class="text-sm text-slate-700 dark:text-slate-300">0–9 (Digits)</span>
        </label>
        <label class="flex items-center gap-2 cursor-pointer p-3 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800">
          <input type="checkbox" v-model="useSymbols" class="rounded border-slate-300 dark:border-slate-600 text-amber-600 focus:ring-amber-500">
          <span class="text-sm text-slate-700 dark:text-slate-300">!@#$% (Symbols)</span>
        </label>
      </div>

      <div class="flex flex-wrap gap-2">
        <button @click="generate" class="px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-amber-600 hover:bg-amber-700 transition">Generate</button>
        <button @click="copyPassword" class="px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-slate-600 hover:bg-slate-700 transition" :disabled="!password">{{ copied ? 'Copied!' : 'Copy' }}</button>
      </div>

      <div v-if="!haveSets" class="p-4 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 text-amber-700 dark:text-amber-400 text-sm">
        Select at least one character set.
      </div>

      <div v-if="password" class="space-y-3">
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 font-mono text-sm break-all">{{ password }}</div>

        <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
            <div class="text-xs text-slate-500 dark:text-slate-400">Length</div>
            <div class="text-lg font-bold text-slate-900 dark:text-white">{{ password.length }}</div>
          </div>
          <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
            <div class="text-xs text-slate-500 dark:text-slate-400">Entropy</div>
            <div class="text-lg font-bold" :class="entropyColor">{{ entropy }} bits</div>
          </div>
          <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 text-center">
            <div class="text-xs text-slate-500 dark:text-slate-400">Strength</div>
            <div class="text-lg font-bold" :class="strengthColor">{{ strength }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const length = ref(16)
const useUpper = ref(true)
const useLower = ref(true)
const useDigits = ref(true)
const useSymbols = ref(false)
const password = ref('')
const copied = ref(false)

const haveSets = computed(() => useUpper.value || useLower.value || useDigits.value || useSymbols.value)

const chars = computed(() => {
  let s = ''
  if (useUpper.value) s += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  if (useLower.value) s += 'abcdefghijklmnopqrstuvwxyz'
  if (useDigits.value) s += '0123456789'
  if (useSymbols.value) s += '!@#$%^&*()_+-=[]{}|;:,.<>?'
  return s
})

const poolSize = computed(() => chars.value.length)

const entropy = computed(() => {
  if (!password.value) return 0
  return Math.round(password.value.length * Math.log2(poolSize.value) * 10) / 10
})

const strength = computed(() => {
  const e = entropy.value
  if (e < 40) return 'Weak'
  if (e < 60) return 'Fair'
  if (e < 80) return 'Good'
  if (e < 100) return 'Strong'
  return 'Very Strong'
})

const entropyColor = computed(() => {
  const e = entropy.value
  if (e < 40) return 'text-red-500'
  if (e < 60) return 'text-amber-500'
  if (e < 80) return 'text-lime-500'
  if (e < 100) return 'text-emerald-500'
  return 'text-green-600'
})

const strengthColor = computed(() => {
  const e = entropy.value
  if (e < 40) return 'text-red-500'
  if (e < 60) return 'text-amber-500'
  if (e < 80) return 'text-lime-500'
  if (e < 100) return 'text-emerald-500'
  return 'text-green-600'
})

function randomPick(charset) {
  return charset[Math.floor(Math.random() * charset.length)]
}

function generate() {
  if (!haveSets.value) return
  copied.value = false
  const cs = chars.value
  let result = ''
  // Ensure at least one char from each selected set
  const sets = []
  if (useUpper.value) sets.push('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  if (useLower.value) sets.push('abcdefghijklmnopqrstuvwxyz')
  if (useDigits.value) sets.push('0123456789')
  if (useSymbols.value) sets.push('!@#$%^&*()_+-=[]{}|;:,.<>?')
  for (const set of sets) {
    result += randomPick(set)
  }
  // Fill the rest
  for (let i = result.length; i < length.value; i++) {
    result += randomPick(cs)
  }
  // Shuffle using Fisher-Yates
  const arr = result.split('')
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]]
  }
  password.value = arr.join('')
}

async function copyPassword() {
  if (!password.value) return
  try {
    await navigator.clipboard.writeText(password.value)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch {}
}
</script>
