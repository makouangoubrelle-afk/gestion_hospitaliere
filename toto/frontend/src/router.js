import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from './views/DashboardView.vue'
import PatientsView from './views/PatientsView.vue'

const DJANGO_LOGIN = 'http://127.0.0.1:8000/login/'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/dashboard' },
    {
      path: '/login',
      beforeEnter() {
        window.location.href = DJANGO_LOGIN
      },
    },
    { path: '/dashboard', component: DashboardView, meta: { requiresAuth: true } },
    { path: '/patients', component: PatientsView, meta: { requiresAuth: true } },
  ],
})

router.beforeEach((to, _from, next) => {
  if (to.meta.requiresAuth && !localStorage.getItem('access_token')) {
    window.location.href = DJANGO_LOGIN
    return
  }
  next()
})

export default router
