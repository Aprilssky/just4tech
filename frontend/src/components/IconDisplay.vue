<template>
  <img v-if="isUrl" :src="icon" :alt="alt" :style="{ width: size, height: size }" class="rounded object-cover flex-shrink-0 inline-block align-middle" @error="onError">
  <span v-else :style="{ fontSize: size }">{{ icon || fallback }}</span>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  icon: { type: String, default: '' },
  fallback: { type: String, default: '🤖' },
  alt: { type: String, default: '' },
  size: { type: String, default: '2rem' }
})

const failed = ref(false)

const isUrl = computed(() => {
  return !failed.value && props.icon && /^https?:\/\//.test(props.icon.trim())
})

function onError() {
  failed.value = true
}
</script>
