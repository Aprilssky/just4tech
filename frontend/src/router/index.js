import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Software from '../views/Software.vue'
import SoftwareDetail from '../views/SoftwareDetail.vue'
import Projects from '../views/Projects.vue'
import IndieDevs from '../views/IndieDevs.vue'
import Blog from '../views/Blog.vue'
import BlogPost from '../views/BlogPost.vue'
import About from '../views/About.vue'
import Contact from '../views/Contact.vue'
import Privacy from '../views/Privacy.vue'
import Terms from '../views/Terms.vue'
import NotFound from '../views/NotFound.vue'
import Sites from '../views/Sites.vue'
import Tutorials from '../views/Tutorials.vue'
import AdminLayout from '../views/admin/AdminLayout.vue'
import AdminLogin from '../views/admin/AdminLogin.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminPosts from '../views/admin/AdminPosts.vue'
import AdminPostEdit from '../views/admin/AdminPostEdit.vue'
import AdminPages from '../views/admin/AdminPages.vue'
import AdminPageEdit from '../views/admin/AdminPageEdit.vue'
import AdminMessages from '../views/admin/AdminMessages.vue'
import AdminSettings from '../views/admin/AdminSettings.vue'
import AdminMedia from '../views/admin/AdminMedia.vue'

const routes = [
  { path: '/', name: 'Home', component: Home, meta: { title: 'Just4Tech — Indie Dev Stories, Tools & Spotlights' } },
  { path: '/tools', redirect: '/aitools' }, { path: '/software', redirect: '/aitools' }, { path: '/software/:slug', redirect: '/aitools/:slug' },
  { path: '/tools/:slug', redirect: '/aitools' },
  { path: '/aitools', name: 'AITools', component: Software, meta: { title: 'AI Tool Picks — Just4Tech' } },
  { path: '/aitools/:slug', name: 'AIToolDetail', component: SoftwareDetail, meta: { title: 'AI Tool — Just4Tech' } },
  { path: '/projects', name: 'Projects', component: Projects, meta: { title: 'Projects — Just4Tech' } },
  { path: '/indie-devs', name: 'IndieDevs', component: IndieDevs, meta: { title: 'Indie Dev Spotlight — Just4Tech' } },
  { path: '/blog', name: 'Blog', component: Blog, meta: { title: 'Blog — Indie Dev Experiences — Just4Tech' } },
  { path: '/blog/:slug', name: 'BlogPost', component: BlogPost, meta: { title: 'Blog Post — Just4Tech' } },
  { path: '/about', name: 'About', component: About, meta: { title: 'About — Just4Tech' } },
  { path: '/contact', name: 'Contact', component: Contact, meta: { title: 'Contact — Just4Tech' } },
  { path: '/privacy', name: 'Privacy', component: Privacy, meta: { title: 'Privacy Policy — Just4Tech' } },
  { path: '/terms', name: 'Terms', component: Terms, meta: { title: 'Terms of Use — Just4Tech' } },

  // Admin routes
  { path: '/admin/login', name: 'AdminLogin', component: AdminLogin, meta: { title: 'Admin Login — Just4Tech' } },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard', name: 'AdminDashboard', component: AdminDashboard, meta: { title: 'Dashboard — Just4Tech Admin' } },
      { path: 'posts', name: 'AdminPosts', component: AdminPosts, meta: { title: 'Posts — Just4Tech Admin' } },
      { path: 'posts/edit/:id', name: 'AdminPostEdit', component: AdminPostEdit, meta: { title: 'Edit Post — Just4Tech Admin' } },
      { path: 'pages', name: 'AdminPages', component: AdminPages, meta: { title: 'Pages — Just4Tech Admin' } },
      { path: 'pages/edit/:id', name: 'AdminPageEdit', component: AdminPageEdit, meta: { title: 'Edit Page — Just4Tech Admin' } },
      { path: 'messages', name: 'AdminMessages', component: AdminMessages, meta: { title: 'Messages — Just4Tech Admin' } },
      { path: 'media', name: 'AdminMedia', component: AdminMedia, meta: { title: 'Media — Just4Tech Admin' } },
      { path: 'settings', name: 'AdminSettings', component: AdminSettings, meta: { title: 'Settings — Just4Tech Admin' } },
    ]
  },

  { path: '/tutorials', name: 'Tutorials', component: Tutorials, meta: { title: 'Tutorials — Just4Tech' } },
  { path: '/sites', name: 'Sites', component: Sites, meta: { title: 'Personal Sites — Just4Tech' } },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Just4Tech'
  next()
})

export default router
