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
        redirect: '/learning/basics'
      },
      {
        path: 'learning/:courseId',
        name: 'Learning',
        component: () => import('../views/Learning.vue'),
        // 路由守卫：校验参数是否合法，不合法重定向到默认课程
        beforeEnter: (to, from, next) => {
          const validIds = ['basics', 'lbl', 'cfop'];
          if (validIds.includes(to.params.courseId)) {
            next();
          } else {
            // 如果乱输 URL (如 /learning/abc)，重定向到基础篇
            next('/learning/basics');
          }
        }
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