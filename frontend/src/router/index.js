import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layout/MainLayout.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../views/Home.vue')
      },
      {
        path: 'cube',
        name: 'CubeFree',
        component: () => import('../views/CubeFree.vue')
      },
      {
        path: 'solver',
        name: 'Solver',
        component: () => import('../views/Solver.vue')
      },
      {
        path: 'learning',
        name: 'Learning',
        component: () => import('../views/Learning.vue')
      },
      {
        path: 'about',
        name: 'About',
        component: () => import('../views/About.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router