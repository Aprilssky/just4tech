// Simple page meta tags manager (no external dependency)
const SITE = 'Just4Tech'
const DEFAULT_DESC = 'Indie dev stories, curated tools, and developer spotlights — by a solo developer, for solo developers.'
const DEFAULT_IMAGE = 'https://just4.tech/images/fastapi-cover.webp'

export function usePageMeta({ title, description, image, type }) {
  const fullTitle = title ? `${title} - ${SITE}` : `${SITE} - Build Better. Ship Faster.`
  const desc = description || DEFAULT_DESC
  const img = image || DEFAULT_IMAGE

  setMeta('title', fullTitle)
  document.title = fullTitle

  setMeta('description', desc)
  setMeta('og:title', fullTitle)
  setMeta('og:description', desc)
  setMeta('og:image', img)
  setMeta('og:type', type || 'website')
  setMeta('og:url', window.location.href)
  setMeta('twitter:card', 'summary_large_image')
  setMeta('twitter:title', fullTitle)
  setMeta('twitter:description', desc)
  setMeta('twitter:image', img)
}

function setMeta(property, content) {
  if (!content) return
  // Try og: and twitter: as property, standard as name
  const attr = property.startsWith('og:') || property.startsWith('twitter:') ? 'property' : 'name'
  let el = document.querySelector(`meta[${attr}="${property}"]`)
  if (!el) {
    el = document.createElement('meta')
    el.setAttribute(attr, property)
    document.head.appendChild(el)
  }
  el.setAttribute('content', content)
}
