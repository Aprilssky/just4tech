<template>
  <Transition name="cookie-banner">
    <div v-if="visible" class="fixed bottom-0 left-0 right-0 z-50 bg-white/95 dark:bg-slate-900/95 backdrop-blur border-t border-gray-200 dark:border-slate-700 shadow-2xl">
      <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div class="flex-1 text-sm text-gray-700 dark:text-slate-300">
            <p>
              🍪 We use cookies to improve your experience and display relevant advertisements.
              By continuing, you agree to our use of cookies.
              <router-link to="/privacy" class="text-amber-600 dark:text-amber-400 hover:underline font-medium">Privacy Policy</router-link>
            </p>
          </div>
          <div class="flex gap-3 shrink-0">
            <button @click="decline"
              class="px-4 py-2 text-sm rounded-lg border border-gray-300 dark:border-slate-600 text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors">
              Essential Only
            </button>
            <button @click="accept"
              class="px-6 py-2 text-sm rounded-lg bg-amber-500 hover:bg-amber-600 text-white font-semibold transition-colors shadow-sm">
              Accept All
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const visible = ref(false)

onMounted(() => {
  const consent = localStorage.getItem('cookie_consent')
  if (!consent) {
    // Small delay so it doesn't flash on page load
    setTimeout(() => { visible.value = true }, 800)
  }
})

function accept() {
  localStorage.setItem('cookie_consent', 'all')
  visible.value = false
}

function decline() {
  localStorage.setItem('cookie_consent', 'essential')
  visible.value = false
}
</script>

<style scoped>
.cookie-banner-enter-active,
.cookie-banner-leave-active {
  transition: transform 0.4s ease, opacity 0.4s ease;
}
.cookie-banner-enter-from,
.cookie-banner-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
