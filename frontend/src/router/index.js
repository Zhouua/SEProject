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
      },
      {
        path: 'liquidity-analysis',
        name: 'LiquidityAnalysis',
        component: () => import('@/views/LiquidityAnalysis.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
