import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { left: 0, top: 0 }
  },
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('../views/HomeView.vue'),
      meta: {
        title: 'Kenya Hockey Fixtures, Results & Standings',
      },
    },

    {
      path: "/league/:gender/:competition/:division?",
      name: "League",
      component: () => import("../views/Pages/LeagueView.vue"),
      meta: {
        title: 'League Table, Fixtures & Results',
      },
    },

    {
      path: '/fixtures',
      name: 'Fixtures',
      component: () => import('../views/Pages/FixturesPage.vue'),
      meta: {
        title: 'Kenya Hockey Fixtures',
      },
    },

    {
      path: "/match/:id/:slug",
      name: "MatchDetail",
      component: () => import("../views/Pages/MatchDetailView.vue"),
      meta: {
        title: 'Hockey Match Details',
      },
    },

    {
      path: "/teams/:teamId/:teamSlug/:tab?",
      name: "TeamProfile",
      component: () => import("@/views/Pages/TeamProfile.vue"),
      meta: {
        title: 'Hockey Team Profile',
      },
    },


    {
      path: '/calendar',
      name: 'Calendar',
      component: () => import('../views/Others/Calendar.vue'),
      meta: {
        title: 'Hockey Calendar',
      },
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('../views/Others/UserProfile.vue'),
      meta: {
        title: 'User Profile',
      },
    },
    {
      path: '/form-elements',
      name: 'Form Elements',
      component: () => import('../views/Forms/FormElements.vue'),
      meta: {
        title: 'Form Elements',
      },
    },
    {
      path: '/basic-tables',
      name: 'Basic Tables',
      component: () => import('../views/Tables/BasicTables.vue'),
      meta: {
        title: 'League Tables',
      },
    },
    {
      path: '/line-chart',
      name: 'Line Chart',
      component: () => import('../views/Chart/LineChart/LineChart.vue'),
      meta: {
        title: 'Hockey Statistics Line Charts',
      },
    },
    {
      path: '/bar-chart',
      name: 'Bar Chart',
      component: () => import('../views/Chart/BarChart/BarChart.vue'),
      meta: {
        title: 'Hockey Statistics Bar Charts',
      },
    },
    {
      path: '/alerts',
      name: 'Alerts',
      component: () => import('../views/UiElements/Alerts.vue'),
      meta: {
        title: 'Alerts',
      },
    },
    {
      path: '/avatars',
      name: 'Avatars',
      component: () => import('../views/UiElements/Avatars.vue'),
      meta: {
        title: 'Avatars',
      },
    },
    {
      path: '/badge',
      name: 'Badge',
      component: () => import('../views/UiElements/Badges.vue'),
      meta: {
        title: 'Badges',
      },
    },

    {
      path: '/buttons',
      name: 'Buttons',
      component: () => import('../views/UiElements/Buttons.vue'),
      meta: {
        title: 'Buttons',
      },
    },

    {
      path: '/images',
      name: 'Images',
      component: () => import('../views/UiElements/Images.vue'),
      meta: {
        title: 'Hockey Images',
      },
    },
    {
      path: '/videos',
      name: 'Videos',
      component: () => import('../views/UiElements/Videos.vue'),
      meta: {
        title: 'Hockey Videos',
      },
    },
    {
      path: '/blank',
      name: 'Blank',
      component: () => import('../views/Pages/BlankPage.vue'),
      meta: {
        title: 'HockeyKE',
      },
    },

    {
      path: '/error-404',
      name: '404 Error',
      component: () => import('../views/Errors/FourZeroFour.vue'),
      meta: {
        title: 'Page Not Found',
      },
    },

    {
      path: '/signin',
      name: 'Signin',
      component: () => import('../views/Auth/Signin.vue'),
      meta: {
        title: 'Sign In',
      },
    },
    {
      path: '/signup',
      name: 'Signup',
      component: () => import('../views/Auth/Signup.vue'),
      meta: {
        title: 'Create an Account',
      },
    },
  ],
})

export default router

const humanize = (value: string | string[] | undefined) => {
  const text = Array.isArray(value) ? value[0] : value

  return (text || '')
    .replace(/-vs-/g, ' vs ')
    .replace(/-/g, ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
    .replace(/\bVs\b/g, 'vs')
}

router.afterEach((to) => {
  let pageTitle = typeof to.meta.title === 'string' ? to.meta.title : 'HockeyKE'

  if (to.name === 'League') {
    const competition = humanize(to.params.competition)
    const gender = humanize(to.params.gender)
    const division = humanize(to.params.division)
    const season = typeof to.query.season === 'string' ? to.query.season : '2026'
    const league = [competition, gender, division, season].filter(Boolean).join(' ')

    pageTitle = `${league} Table, Fixtures & Results`
  } else if (to.name === 'MatchDetail') {
    pageTitle = `${humanize(to.params.slug)} – Match Details`
  } else if (to.name === 'TeamProfile') {
    pageTitle = `${humanize(to.params.teamSlug)} – Fixtures, Results & Statistics`
  }

  document.title = pageTitle === 'HockeyKE' ? pageTitle : `${pageTitle} | HockeyKE`
})
