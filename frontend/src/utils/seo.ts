import type { RouteLocationNormalized } from 'vue-router'

const SITE_NAME = 'HockeyKE'
const SITE_URL = 'https://hockeyke.com'
const SOCIAL_IMAGE = `${SITE_URL}/images/social/hockeyke-social-share-v2.png`
const DEFAULT_DESCRIPTION =
  "Follow Kenyan field hockey fixtures, results, league tables, schedules and team statistics across men's and women's Premier, Super and National Leagues."

const humanize = (value: string | string[] | undefined) => {
  const text = Array.isArray(value) ? value[0] : value

  return (text || '')
    .replace(/-vs-/g, ' vs ')
    .replace(/-/g, ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
    .replace(/\bVs\b/g, 'vs')
}

const setMeta = (
  selector: string,
  attribute: 'name' | 'property',
  key: string,
  content: string,
) => {
  let element = document.head.querySelector<HTMLMetaElement>(selector)

  if (!element) {
    element = document.createElement('meta')
    element.setAttribute(attribute, key)
    document.head.appendChild(element)
  }

  element.content = content
}

const setCanonical = (url: string) => {
  let canonical = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]')

  if (!canonical) {
    canonical = document.createElement('link')
    canonical.rel = 'canonical'
    document.head.appendChild(canonical)
  }

  canonical.href = url
}

export const applySeo = (route: RouteLocationNormalized, title: string) => {
  let description = DEFAULT_DESCRIPTION
  let shouldIndex = true

  if (route.name === 'League') {
    const competition = humanize(route.params.competition)
    const gender = humanize(route.params.gender)
    const division = humanize(route.params.division)
    const season = typeof route.query.season === 'string' ? route.query.season : '2026'
    const league = [competition, gender, division].filter(Boolean).join(' ')

    description = `View the ${season} ${league} field hockey table, fixtures, results and team statistics in Kenya.`
  } else if (route.name === 'MatchDetail') {
    const match = humanize(route.params.slug)
    description = `View ${match} match details, recent form, head-to-head records, league table and statistics.`
  } else if (route.name === 'TeamProfile') {
    const team = humanize(route.params.teamSlug)
    description = `Follow ${team} fixtures, results, league position, recent form and field hockey statistics.`
  } else if (route.name === 'Fixtures') {
    description = 'View upcoming Kenya field hockey fixtures, match schedules, dates, times and venues.'
    shouldIndex = false
  } else if (route.name === 'About') {
    description =
      'Learn about HockeyKE, a platform for Kenyan field hockey fixtures, results, league tables and team statistics across national competitions.'
  } else if (route.name === 'Contact') {
    description =
      'Contact HockeyKE by email to report fixture or result corrections, provide feedback or ask about Kenyan field hockey information on the platform.'
  } else if (route.name === 'Privacy') {
    description =
      'Read the HockeyKE privacy policy covering Google Analytics, advertising cookies, third-party services and the choices available to website visitors.'
  } else if (route.name !== 'Home') {
    shouldIndex = false
  }

  const canonicalUrl = `${SITE_URL}${route.path === '/' ? '/' : route.path.replace(/\/+$/, '')}`
  const robots = shouldIndex ? 'index, follow' : 'noindex, nofollow'

  setCanonical(canonicalUrl)
  setMeta('meta[name="description"]', 'name', 'description', description)
  setMeta('meta[name="robots"]', 'name', 'robots', robots)
  setMeta('meta[property="og:site_name"]', 'property', 'og:site_name', SITE_NAME)
  setMeta('meta[property="og:type"]', 'property', 'og:type', 'website')
  setMeta('meta[property="og:title"]', 'property', 'og:title', title)
  setMeta('meta[property="og:description"]', 'property', 'og:description', description)
  setMeta('meta[property="og:url"]', 'property', 'og:url', canonicalUrl)
  setMeta('meta[property="og:image"]', 'property', 'og:image', SOCIAL_IMAGE)
  setMeta('meta[name="twitter:card"]', 'name', 'twitter:card', 'summary_large_image')
  setMeta('meta[name="twitter:title"]', 'name', 'twitter:title', title)
  setMeta('meta[name="twitter:description"]', 'name', 'twitter:description', description)
  setMeta('meta[name="twitter:image"]', 'name', 'twitter:image', SOCIAL_IMAGE)
}
