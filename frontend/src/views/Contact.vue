<template>
  <div>
    <section class="hero-gradient py-20">
      <div class="max-w-4xl mx-auto px-4 text-center relative z-10">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 text-amber-400 text-sm font-medium mb-6 border border-white/10">
          <span class="w-2 h-2 bg-amber-400 rounded-full animate-pulse-dot"></span>
          <span>Contact</span>
        </div>
        <h1 class="text-4xl sm:text-5xl font-bold text-white mb-4">Contact Us</h1>
        <p class="text-lg text-gray-400 max-w-2xl mx-auto">Have a question, suggestion, or just want to say hi? We'd love to hear from you.</p>
      </div>
    </section>

    <section class="py-16 bg-white dark:bg-slate-900">
      <div class="max-w-4xl mx-auto px-4 sm:px-6">
        <div class="grid md:grid-cols-2 gap-12">
          <!-- Contact Form -->
          <div>
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Send Us a Message</h2>
            <form @submit.prevent="handleSubmit" class="space-y-5">
              <div>
                <label for="name" class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Name</label>
                <input v-model="form.name" type="text" id="name" required
                  class="w-full px-4 py-3 border border-gray-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-gray-900 dark:text-white dark:bg-slate-800"
                  placeholder="Your name">
              </div>
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Email</label>
                <input v-model="form.email" type="email" id="email" required
                  class="w-full px-4 py-3 border border-gray-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-gray-900 dark:text-white dark:bg-slate-800"
                  placeholder="you@example.com">
              </div>
              <div>
                <label for="subject" class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Subject</label>
                <select v-model="form.subject" id="subject"
                  class="w-full px-4 py-3 border border-gray-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-gray-900 dark:text-white dark:bg-slate-800">
                  <option value="general">General Inquiry</option>
                  <option value="tool-suggestion">Tool Suggestion</option>
                  <option value="blog-topic">Blog Topic Request</option>
                  <option value="bug">Bug Report</option>
                  <option value="feedback">Feedback</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label for="message" class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Message</label>
                <textarea v-model="form.message" id="message" rows="5" required
                  class="w-full px-4 py-3 border border-gray-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-gray-900 dark:text-white dark:bg-slate-800 resize-y"
                  placeholder="How can we help?"></textarea>
              </div>
              <button type="submit" class="btn btn-primary w-full !py-3">Send Message</button>
              <p v-if="submitted" class="text-sm text-center mt-2 text-green-600 dark:text-green-400">
                Thank you! Your message has been sent. We will get back to you soon.
              </p>
            </form>
          </div>

          <!-- Editable Content (from admin panel) -->
          <div v-if="!loading && page.content" class="blog-content" v-html="renderedContent"></div>
          <div v-else-if="loading" class="text-center py-12 text-gray-500">Loading...</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePageMeta } from '../utils/meta.js'
import { marked } from 'marked'

const form = ref({ name: '', email: '', subject: 'general', message: '' })
const submitted = ref(false)
const page = ref({ content: '' })
const loading = ref(true)

const renderedContent = computed(() => {
  try { return marked(page.value.content || '') } catch { return page.value.content || '' }
})

async function handleSubmit() {
  try {
    await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
  } catch {}
  submitted.value = true
  form.value = { name: '', email: '', subject: 'general', message: '' }
  setTimeout(() => { submitted.value = false }, 5000)
}

onMounted(async () => {
  try {
    const resp = await fetch('/api/page/contact')
    if (resp.ok) page.value = await resp.json()
  } catch {}
  loading.value = false
  usePageMeta({
    title: 'Contact — Just4Tech',
    description: 'Contact the Just4Tech team. We would love to hear from you.'
  })
})
</script>
