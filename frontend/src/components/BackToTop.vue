<template>
  <Transition name="slide-up">
    <button
      v-if="visible"
      @click="scrollToTop"
      class="back-to-top"
      aria-label="Back to top"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
      </svg>
      <span class="back-to-top-label">Top</span>
    </button>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const visible = ref(false)
let timer = null

function onScroll() {
  if (timer) return
  timer = setTimeout(() => {
    visible.value = window.scrollY > 400
    timer = null
  }, 100)
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  if (timer) clearTimeout(timer)
})
</script>

<style scoped>
.back-to-top {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 50;
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 9999px;
  background: var(--color-brand);
  color: white;
  box-shadow: 0 4px 12px oklch(0 0 0 / 0.2);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  transition: all 0.25s var(--ease-out);
  overflow: hidden;
}
.back-to-top:hover {
  width: auto;
  padding: 0 1.25rem 0 0.75rem;
  gap: 0.4rem;
  background: var(--color-brand-dark);
  box-shadow: 0 4px 16px oklch(0.55 0.18 30 / 0.35);
}
.back-to-top-label {
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
  max-width: 0;
  overflow: hidden;
  opacity: 0;
  transition: max-width 0.25s var(--ease-out), opacity 0.2s var(--ease-out);
}
.back-to-top:hover .back-to-top-label {
  max-width: 50px;
  opacity: 1;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.25s var(--ease-out);
}
.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(12px);
}
</style>
