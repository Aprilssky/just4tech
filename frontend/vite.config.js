import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import prerender from 'vite-plugin-prerender'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    prerender({
      routes: [
        '/',
        '/blog',
        '/aitools',
        '/projects',
        '/indie-devs',
        '/tutorials',
        '/sites',
        '/about',
        '/contact',
        '/privacy',
        '/terms',
      ],
      puppeteerOptions: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
      },
    }),
  ],
  base: '/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('highlight.js')) return 'highlight'
          if (id.includes('node_modules/vue')) return 'vendor'
        }
      }
    }
  }
})
