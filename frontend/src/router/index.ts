import { createRouter, createWebHistory } from 'vue-router'
import PageContentVue from '@/pages/PageContent.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: PageContentVue
    }
  ]
})

export default router
