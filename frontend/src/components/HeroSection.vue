<template>
  <section :class="['hero-gradient min-h-[80vh] flex items-center', { 'bg-gray-900': !gradient }]">
    <div class="hero-deco" aria-hidden="true">
      <span style="top:15%;left:8%;width:8px;height:8px"></span>
      <span style="top:25%;right:15%"></span>
      <span style="top:60%;left:5%;width:10px;height:10px;opacity:0.08"></span>
      <span style="bottom:20%;right:8%"></span>
      <span style="top:40%;left:50%;width:4px;height:4px;opacity:0.06"></span>
    </div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10">
      <div class="max-w-3xl">
        <div v-if="badge" class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 text-amber-400 text-sm font-medium mb-6 border border-white/10">
          <span class="w-2 h-2 bg-amber-400 rounded-full animate-pulse"></span>
          {{ badge }}
        </div>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white leading-tight mb-6" v-html="title"></h1>
        <p v-if="subtitle" class="text-lg sm:text-xl text-gray-400 mb-8 max-w-2xl leading-relaxed" v-html="subtitle"></p>
        <div class="flex flex-wrap gap-4">
          <slot name="actions"></slot>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  badge: { type: String, default: '' },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  gradient: { type: Boolean, default: true }
})
</script>
