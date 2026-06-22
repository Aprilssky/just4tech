<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Color Converter</h2>
      <p class="text-slate-600 dark:text-slate-400 mt-1">Convert colors between HEX, RGB, and HSL formats with a live preview.</p>
    </div>

    <div class="space-y-4">
      <!-- Preview -->
      <div class="h-32 rounded-xl border-2 border-slate-200 dark:border-slate-700 transition-all duration-300" :style="{ backgroundColor: previewColor }"></div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <!-- HEX -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">HEX</label>
          <input v-model="hex" @input="fromHex" class="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none font-mono" placeholder="#6366F1">
        </div>

        <!-- RGB -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">RGB</label>
          <div class="flex gap-1">
            <input type="number" v-model.number="r" @input="fromRgb" min="0" max="255" class="w-full px-2 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-center font-mono" placeholder="R">
            <input type="number" v-model.number="g" @input="fromRgb" min="0" max="255" class="w-full px-2 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-center font-mono" placeholder="G">
            <input type="number" v-model.number="b" @input="fromRgb" min="0" max="255" class="w-full px-2 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-center font-mono" placeholder="B">
          </div>
        </div>

        <!-- HSL -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">HSL</label>
          <div class="flex gap-1">
            <input type="number" v-model.number="h" @input="fromHsl" min="0" max="360" class="w-full px-2 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-center font-mono" placeholder="H">
            <input type="number" v-model.number="s" @input="fromHsl" min="0" max="100" class="w-full px-2 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-center font-mono" placeholder="S">
            <input type="number" v-model.number="l" @input="fromHsl" min="0" max="100" class="w-full px-2 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-center font-mono" placeholder="L">
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">HEX</div>
          <div class="font-mono text-sm text-slate-900 dark:text-white break-all">{{ hexDisplay }}</div>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">RGB</div>
          <div class="font-mono text-sm text-slate-900 dark:text-white">{{ rgbDisplay }}</div>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800">
          <div class="text-xs text-slate-500 dark:text-slate-400 mb-1">HSL</div>
          <div class="font-mono text-sm text-slate-900 dark:text-white">{{ hslDisplay }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const hex = ref('#6366F1')
const r = ref(99)
const g = ref(102)
const b = ref(241)
const h = ref(239)
const s = ref(84)
const l = ref(67)

let updating = false

const previewColor = computed(() => {
  return `rgb(${r.value}, ${g.value}, ${b.value})`
})

const hexDisplay = computed(() => {
  return '#' + [r.value, g.value, b.value].map(v => {
    const hx = Math.round(v).toString(16).toUpperCase()
    return hx.length === 1 ? '0' + hx : hx
  }).join('')
})

const rgbDisplay = computed(() => `rgb(${Math.round(r.value)}, ${Math.round(g.value)}, ${Math.round(b.value)})`)

const hslDisplay = computed(() => `hsl(${Math.round(h.value)}, ${Math.round(s.value)}%, ${Math.round(l.value)}%)`)

function fromHex() {
  if (updating) return
  updating = true
  const val = hex.value.replace('#', '')
  if (val.length === 3) {
    r.value = parseInt(val[0] + val[0], 16)
    g.value = parseInt(val[1] + val[1], 16)
    b.value = parseInt(val[2] + val[2], 16)
  } else if (val.length === 6) {
    r.value = parseInt(val.slice(0, 2), 16)
    g.value = parseInt(val.slice(2, 4), 16)
    b.value = parseInt(val.slice(4, 6), 16)
  }
  if (!isNaN(r.value) && !isNaN(g.value) && !isNaN(b.value)) {
    updateHsl()
  }
  updating = false
}

function fromRgb() {
  if (updating) return
  updating = true
  clampRgb()
  hex.value = hexDisplay.value
  updateHsl()
  updating = false
}

function fromHsl() {
  if (updating) return
  updating = true
  clampHsl()
  const { r: nr, g: ng, b: nb } = hslToRgb(h.value, s.value / 100, l.value / 100)
  r.value = Math.round(nr * 255)
  g.value = Math.round(ng * 255)
  b.value = Math.round(nb * 255)
  hex.value = hexDisplay.value
  updating = false
}

function clampRgb() {
  r.value = Math.max(0, Math.min(255, r.value || 0))
  g.value = Math.max(0, Math.min(255, g.value || 0))
  b.value = Math.max(0, Math.min(255, b.value || 0))
}

function clampHsl() {
  h.value = Math.max(0, Math.min(360, h.value || 0))
  s.value = Math.max(0, Math.min(100, s.value || 0))
  l.value = Math.max(0, Math.min(100, l.value || 0))
}

function updateHsl() {
  const nr = r.value / 255, ng = g.value / 255, nb = b.value / 255
  const max = Math.max(nr, ng, nb), min = Math.min(nr, ng, nb)
  let hh = 0, ss = 0, ll = (max + min) / 2

  if (max !== min) {
    const d = max - min
    ss = ll > 0.5 ? d / (2 - max - min) : d / (max + min)
    switch (max) {
      case nr: hh = ((ng - nb) / d + (ng < nb ? 6 : 0)) / 6; break
      case ng: hh = ((nb - nr) / d + 2) / 6; break
      case nb: hh = ((nr - ng) / d + 4) / 6; break
    }
  }

  h.value = Math.round(hh * 360)
  s.value = Math.round(ss * 100)
  l.value = Math.round(ll * 100)
}

function hslToRgb(hh, ss, ll) {
  const c = (1 - Math.abs(2 * ll - 1)) * ss
  const x = c * (1 - Math.abs((hh / 60) % 2 - 1))
  const m = ll - c / 2
  let nr, ng, nb

  if (hh < 60) { nr = c; ng = x; nb = 0 }
  else if (hh < 120) { nr = x; ng = c; nb = 0 }
  else if (hh < 180) { nr = 0; ng = c; nb = x }
  else if (hh < 240) { nr = 0; ng = x; nb = c }
  else if (hh < 300) { nr = x; ng = 0; nb = c }
  else { nr = c; ng = 0; nb = x }

  return { r: nr + m, g: ng + m, b: nb + m }
}
</script>
