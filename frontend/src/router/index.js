import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/layout/Layout.vue'

const routes = [
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
        path: 'trade',
        name: 'Trade',
        component: () => import('@/views/Trade.vue')
      },
      {
        path: 'wallet',
        name: 'Wallet',
        component: () => import('@/views/Wallet.vue')
      },
      {
        path: 'markets',
        name: 'Markets',
        component: () => import('@/views/Markets.vue')
      },
      {
        path: 'transactions',
        name: 'Transactions',
        component: () => import('@/views/Transactions.vue')
      },
      {
        path: 'buy-crypto',
        name: 'BuyCrypto',
        component: () => import('@/views/BuyCrypto.vue')
      },
      {
        path: 'sell-crypto',
        name: 'SellCrypto',
        component: () => import('@/views/SellCrypto.vue')
      },
      {
        path: 'convert',
        name: 'Convert',
        component: () => import('@/views/Convert.vue')
      },
      {
        path: 'referral',
        name: 'Referral',
        component: () => import('@/views/Referral.vue')
      },
      {
        path: 'crypto/:symbol',
        name: 'CryptoDetails',
        component: () => import('@/views/CryptoDetails.vue')
      },
      {
        path: 'assets',
        name: 'Assets',
        component: () => import('@/views/Assets.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
