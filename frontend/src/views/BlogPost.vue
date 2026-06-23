<template>
  <div>
    <section class="hero-gradient py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="mb-4">
          <router-link to="/blog" class="text-amber-400 hover:text-amber-300 text-sm flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back to Blog
          </router-link>
        </div>
        <h1 class="text-3xl sm:text-4xl font-bold text-white">{{ post.title || capitalize(slug) }}</h1>
        <a v-if="post.external_url" :href="post.external_url" target="_blank" rel="noopener"
          class="inline-flex items-center gap-1 mt-4 px-4 py-2 rounded-lg bg-white/10 text-white hover:bg-white/20 text-sm font-semibold no-underline transition-colors">
          🔗 Visit Site →
        </a>
        <div v-if="post.date" class="flex items-center gap-3 mt-3 text-sm text-gray-400">
          <span>{{ post.date }}</span>
          <span v-if="post.readTime">• {{ post.readTime }}</span>
          <span v-if="post.category" class="blog-category" :class="categoryClass(post.category)">{{ post.category }}</span>
        </div>
      </div>
    </section>

    <section class="py-16 bg-white dark:bg-slate-900">
      <div class="max-w-4xl mx-auto px-4 sm:px-6">
        <div v-if="post.content" class="blog-content max-w-none" v-html="renderedContent"></div>

        <!-- Related Posts -->
        <div v-if="relatedPosts.length" class="mt-16 pt-12 border-t border-gray-200 dark:border-slate-700">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-6">📝 Related Posts</h3>
          <div class="grid md:grid-cols-2 gap-6">
            <router-link v-for="rp in relatedPosts" :key="rp.slug" :to="'/blog/' + rp.slug"
              class="no-underline block p-5 rounded-xl border border-gray-200 dark:border-slate-700 hover:border-amber-300 dark:hover:border-amber-600 hover:shadow-md transition-all bg-gray-50 dark:bg-slate-800">
              <span class="text-xs font-semibold px-2 py-0.5 rounded-full" :class="categoryClass(rp.category)">{{ rp.category }}</span>
              <h4 class="font-semibold text-gray-900 dark:text-white mt-2 mb-1">{{ rp.title }}</h4>
              <p class="text-sm text-gray-500 dark:text-slate-400 line-clamp-2">{{ rp.excerpt }}</p>
            </router-link>
          </div>
        </div>

        <div v-else class="text-center py-12">
          <div class="text-5xl mb-4">📝</div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">{{ post.title || 'Blog Post' }}</h2>
          <p class="text-slate-600 dark:text-slate-400 mb-6">{{ post.excerpt || 'This blog post is coming soon. Stay tuned for more content about indie development, tools, and tutorials.' }}</p>

          <div v-if="!loading" class="mt-8 p-6 bg-slate-50 dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 text-left">
            <h3 class="font-semibold text-gray-900 dark:text-white mb-3">Post Preview</h3>
            <p class="text-slate-600 dark:text-slate-400 text-sm">This is a placeholder. Once the blog post content is published on the server, it will appear here. In the meantime, feel free to <router-link to="/contact" class="text-amber-600 dark:text-amber-400 hover:underline">suggest a topic</router-link> you'd like us to cover.</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style>
/* Blog content markdown styling */
.blog-content {
  color: #374151;
  line-height: 1.75;
}
.blog-content h1 { font-size: 1.875rem; font-weight: 700; margin-top: 2.5rem; margin-bottom: 1.25rem; color: #111827; }
.blog-content h2 { font-size: 1.5rem; font-weight: 700; margin-top: 2rem; margin-bottom: 1rem; color: #111827; }
.blog-content h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem; color: #111827; }
.blog-content h4 { font-size: 1.125rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem; color: #111827; }
.blog-content p { margin-bottom: 1rem; line-height: 1.75; }
.blog-content ul { list-style-type: disc; padding-left: 1.5rem; margin-bottom: 1rem; }
.blog-content ol { list-style-type: decimal; padding-left: 1.5rem; margin-bottom: 1rem; }
.blog-content li { line-height: 1.75; margin-bottom: 0.25rem; }
.blog-content a { color: #4f46e5; text-decoration: underline; }
.blog-content a:hover { color: #3730a3; }
.blog-content blockquote {
  border-left: 4px solid #818cf8;
  padding-left: 1rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  background-color: #eef2ff;
  font-style: italic;
  color: #4b5563;
}
.blog-content code {
  background-color: #f3f4f6;
  color: #d9464b;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-family: ui-monospace, SFMono-Regular, monospace;
}
.blog-content pre { margin-bottom: 1.5rem; border-radius: 0.75rem; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.blog-content pre code {
  display: block;
  padding: 1.25rem 1.5rem;
  font-size: 0.875rem;
  line-height: 1.5;
  background-color: #111827;
  color: #f3f4f6;
  overflow-x: auto;
  border-radius: 0;
}
.blog-content img { border-radius: 0.75rem; margin: 1.5rem 0; max-width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.blog-content .blog-img-link { display: inline-block; cursor: zoom-in; position: relative; }
.blog-content .blog-img-link:hover img { opacity: 0.9; box-shadow: 0 8px 16px rgba(0,0,0,0.2); transition: opacity 0.2s, box-shadow 0.2s; }
.blog-content .blog-img-link::after {
  content: '🔍';
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0,0,0,0.6);
  color: white;
  font-size: 14px;
  padding: 4px 8px;
  border-radius: 6px;
  opacity: 0;
  transition: opacity 0.2s;
}
.blog-content .blog-img-link:hover::after { opacity: 1; }
.blog-content hr { margin: 2rem 0; border: none; border-top: 1px solid #e5e7eb; }
.blog-content table { width: 100%; margin-bottom: 1.5rem; border-collapse: collapse; }
.blog-content th { background-color: #f3f4f6; text-align: left; padding: 0.5rem 1rem; font-weight: 600; border: 1px solid #e5e7eb; }
.blog-content td { padding: 0.5rem 1rem; border: 1px solid #e5e7eb; }
.blog-content strong { font-weight: 600; color: #111827; }
.blog-content em { font-style: italic; }

/* Dark mode */
[data-theme="dark"] .blog-content { color: #d1d5db; }
[data-theme="dark"] .blog-content h1,
[data-theme="dark"] .blog-content h2,
[data-theme="dark"] .blog-content h3,
[data-theme="dark"] .blog-content h4 { color: #ffffff; }
[data-theme="dark"] .blog-content strong { color: #f3f4f6; }
[data-theme="dark"] .blog-content a { color: #818cf8; }
[data-theme="dark"] .blog-content a:hover { color: #a5b4fc; }
[data-theme="dark"] .blog-content blockquote { background-color: #1f2937; border-color: #6366f1; color: #9ca3af; }
[data-theme="dark"] .blog-content code { background-color: #1f2937; color: #f472b6; }
[data-theme="dark"] .blog-content th { background-color: #1f2937; border-color: #374151; color: #e5e7eb; }
[data-theme="dark"] .blog-content td { border-color: #374151; }
[data-theme="dark"] .blog-content hr { border-color: #374151; }
</style>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { usePageMeta } from '../utils/meta.js'
import { useRoute } from 'vue-router'

let markedModule = null
let hljsReady = false

async function getMarked() {
  if (!markedModule) {
    markedModule = await import('marked')
  }
  return markedModule.marked
}

async function ensureHljs() {
  if (hljsReady) return
  const hljs = await import('highlight.js')
  await import('highlight.js/styles/github-dark.css')
  const marked = await getMarked()
  marked.setOptions({
    breaks: true,
    gfm: true,
    highlight: function(code, lang) {
      if (lang && hljs.default.getLanguage(lang)) {
        try {
          return hljs.default.highlight(code, { language: lang }).value
        } catch {}
      }
      return hljs.default.highlightAuto(code).value
    }
  })
  hljsReady = true
}

const route = useRoute()
const slug = route.params.slug
const post = ref({})
const loading = ref(true)
const relatedPosts = ref([])
const renderedContent = ref('')

async function renderContent() {
  if (!post.value.content) {
    renderedContent.value = ''
    return
  }
  const marked = await getMarked()
  let html = marked.parse(post.value.content)
  // Wrap images in clickable links to open full-size in new tab
  html = html.replace(/<img\s+src="([^"]+)"([^>]*)>/g, (match, src, rest) => {
    return `<a href="${src}" target="_blank" class="blog-img-link"><img src="${src}"${rest}></a>`
  })
  renderedContent.value = html
}

onMounted(async () => {
  try {
    const res = await fetch(`/api/posts/slug/${slug}`)
    if (res.ok) {
      const data = await res.json()
      post.value = data
      usePageMeta({title: data.title, description: data.excerpt, image: data.cover_image})
    }
  } catch { /* fallback */ }
  if (!post.value.title) {
    post.value.title = capitalize(slug.replace(/-/g, ' '))
  }
  // Fetch related posts (same category, exclude current)
  try {
    const all = await (await fetch('/api/posts')).json()
    relatedPosts.value = all
      .filter(p => p.slug !== slug && (p.category === post.value.category))
      .slice(0, 4)
    if (relatedPosts.value.length < 2) {
      relatedPosts.value = all.filter(p => p.slug !== slug).slice(0, 4)
    }
  } catch {}
  await renderContent()
  loading.value = false
  await nextTick()
  // Lazy-load highlight.js for code blocks
  ensureHljs().then(() => {
    document.querySelectorAll('.blog-content pre code').forEach(el => {
      // hljs is now available via globalThis after dynamic import
      import('highlight.js').then(mod => mod.default.highlightElement(el))
    })
  })
})

function capitalize(str) {
  return str.replace(/\b\w/g, c => c.toUpperCase())
}

function categoryClass(cat) {
  const map = {
    'Tutorial': 'bg-amber-100 text-amber-800',
    'Vibe Coding': 'bg-rose-100 text-rose-800',
    'Indie Diary': 'bg-orange-100 text-orange-800',
    'Dev Tools': 'bg-sky-100 text-sky-800',
  }
  return map[cat] || 'bg-gray-100 text-gray-800'
}
</script>
