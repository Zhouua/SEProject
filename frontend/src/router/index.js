import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/layout/Layout.vue'

const routes = [
  {
    path: '/',
    redirect: '/welcome'
  },
  {
    path: '/welcome',
    name: 'Welcome',
    component: () => import('@/views/Welcome.vue')
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue')
      },
      {
        path: 'price-comparison',
        name: 'PriceComparison',
        component: () => import('@/views/PriceComparison.vue')
      },
      {
        path: 'arbitrage-analysis',
        name: 'ArbitrageAnalysis',
        component: () => import('@/views/ArbitrageAnalysis.vue')
      },
      {
        path: 'volume-comparison',
        name: 'VolumeComparison',
        component: () => import('@/views/VolumeComparison.vue')
      }
    ]
  },
  {
    path: '/help',
    name: 'Help',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('@/views/HelpCenter.vue')
      }
    ]
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('@/views/Welcome.vue') // 使用 Welcome 页面作为占位符
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
