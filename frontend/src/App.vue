<template>
  <div id="app">
    <Navbar />
    <router-view v-slot="{ Component }">
      <Transition name="fade" mode="out-in" @after-enter="observeRevealElements">
        <component :is="Component" />
      </Transition>
    </router-view>
    <Footer />
    <BackToTop />
    <CookieBanner />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import BackToTop from './components/BackToTop.vue'
import CookieBanner from './components/CookieBanner.vue'
import { playClick, isSoundEnabled } from './utils/sound.js'

let revealObserver = null

const router = useRouter()
router.onError((err) => {
  console.error('[Router error]', err)
})

function observeRevealElements() {
  if (!revealObserver) return
  document.querySelectorAll('.reveal:not(.visible)').forEach(el => {
    revealObserver.observe(el)
  })
}

function handleClick(e) {
  if (!isSoundEnabled()) return
  const target = e.target.closest('a, button, .tool-card, .blog-card, .filter-btn, [role="button"]')
  if (target) playClick()
}

onMounted(() => {
  document.addEventListener('click', handleClick)
  // Scroll reveal
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); revealObserver?.unobserve(e.target) } })
    }, { threshold: 0.15 })
    observeRevealElements()
  } else {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'))
  }
})
onUnmounted(() => {
  document.removeEventListener('click', handleClick)
  if (revealObserver) revealObserver.disconnect()
})
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Smooth theme transition */
html {
  transition: background-color 0.3s ease, color 0.3s ease;
}
html *, html *::before, html *::after {
  transition: background-color 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}
@media (prefers-reduced-motion: reduce) {
  html, html *, html *::before, html *::after {
    transition: none !important;
  }
}
</style>
