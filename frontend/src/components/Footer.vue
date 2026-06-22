<template>
  <footer class="footer py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid md:grid-cols-4 gap-8">
        <!-- Column 1: Brand -->
        <div>
          <router-link to="/" class="flex items-center gap-2 text-white font-bold text-lg mb-4 no-underline">
            <span class="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-500 to-rose-500 flex items-center justify-center text-white text-sm font-bold">JT</span>
            Just4Tech
          </router-link>
          <p class="text-sm text-slate-400">{{ description }}</p>
        </div>

        <!-- Column 2: Tools -->
        <div>
          <h4 class="text-white font-semibold mb-3">Tools</h4>
          <ul class="space-y-2 text-sm">
            <li v-for="tool in tools" :key="tool.slug">
              <router-link :to="'/tools/' + tool.slug" class="text-slate-400 hover:text-white transition-colors no-underline">{{ tool.name }}</router-link>
            </li>
          </ul>
        </div>

        <!-- Column 3: Explore -->
        <div>
          <h4 class="text-white font-semibold mb-3">Explore</h4>
          <ul class="space-y-2 text-sm">
            <li><router-link to="/blog" class="text-slate-400 hover:text-white transition-colors no-underline">Blog</router-link></li>
            <li><router-link to="/tutorials" class="text-slate-400 hover:text-white transition-colors no-underline">Tutorials</router-link></li>
            <li><router-link to="/aitools" class="text-slate-400 hover:text-white transition-colors no-underline">AI Tools</router-link></li>
            <li><router-link to="/projects" class="text-slate-400 hover:text-white transition-colors no-underline">Projects</router-link></li>
            
          </ul>
        </div>

        <!-- Column 4: Links -->
        <div>
          <h4 class="text-white font-semibold mb-3">Links</h4>
          <ul class="space-y-2 text-sm">
            <li><router-link to="/contact" class="text-slate-400 hover:text-white transition-colors no-underline">Contact</router-link></li>
            <li><router-link to="/privacy" class="text-slate-400 hover:text-white transition-colors no-underline">Privacy Policy</router-link></li>
            <li><router-link to="/terms" class="text-slate-400 hover:text-white transition-colors no-underline">Terms of Use</router-link></li>
          </ul>
        </div>
      </div>

      <!-- Bottom bar -->
      <div class="border-t border-slate-800 dark:border-slate-700/50 mt-10 pt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
        <p class="text-sm text-slate-500">&copy; {{ new Date().getFullYear() }} Just4Tech. All rights reserved.</p>
        <div class="flex gap-6 text-sm">
          <router-link to="/privacy" class="text-slate-500 hover:text-slate-300 transition-colors no-underline">Privacy</router-link>
          <router-link to="/terms" class="text-slate-500 hover:text-slate-300 transition-colors no-underline">Terms</router-link>
          <router-link to="/contact" class="text-slate-500 hover:text-slate-300 transition-colors no-underline">Contact</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const description = 'Indie dev stories, curated tools, and developer spotlights — by a solo developer, for solo developers.'

const tools = [
  { slug: 'json', name: 'JSON Formatter' },
  { slug: 'base64', name: 'Base64 Encoder/Decoder' },
  { slug: 'uuid', name: 'UUID Generator' },
  { slug: 'password', name: 'Password Generator' },
  { slug: 'color', name: 'Color Converter' },
  { slug: 'url', name: 'URL Encoder/Decoder' },
]
</script>
