<template>
  <div class="sidebar">
    <nav class="nav-menu">
      <router-link 
        v-for="item in menuItems" 
        :key="item.path" 
        :to="item.path"
        class="nav-item"
        :class="{ 'active': isActive(item.path) }"
      >
        <component :is="item.icon" :size="20" stroke-width="2" class="nav-icon" />
        <span class="nav-text">{{ t(item.nameKey) }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <router-link to="/help" class="nav-item">
        <HelpCircle :size="20" stroke-width="2" class="nav-icon" />
        <span class="nav-text">{{ t('sidebar.helpCenter') }}</span>
      </router-link>
      <router-link to="/settings" class="nav-item">
        <Settings :size="20" stroke-width="2" class="nav-icon" />
        <span class="nav-text">{{ t('sidebar.settings') }}</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { 
  LayoutGrid, 
  TrendingUp, 
  BarChart2, 
  Activity, 
  Droplets,
  HelpCircle,
  Settings,
  Hexagon
} from 'lucide-vue-next'

const route = useRoute()
const { t } = useI18n()

const menuItems = [
  { nameKey: 'sidebar.dashboard', path: '/dashboard', icon: LayoutGrid },
  { nameKey: 'sidebar.priceComparison.title', path: '/price-comparison', icon: TrendingUp },
  { nameKey: 'sidebar.arbitrage.title', path: '/arbitrage-analysis', icon: BarChart2 },
  { nameKey: 'sidebar.volumeComparison', path: '/volume-comparison', icon: Activity },
  { nameKey: 'sidebar.liquidityAnalysis', path: '/liquidity-analysis', icon: Droplets },
]

const isActive = (path) => {
  return route.path === path
}
</script>

<style lang="scss" scoped>
.sidebar {
  width: 100%;
  height: 100%;
  background-color: var(--color-bg-secondary);
  display: flex;
  flex-direction: column;
  padding: var(--spacing-lg) var(--spacing-md);
  border-right: 1px solid var(--color-border);
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 12px 32px 12px;
  color: var(--color-text-primary);
  
  .logo-icon {
    color: var(--color-accent);
  }
  
  .logo-text {
    font-size: 20px;
    font-weight: 700;
    letter-spacing: -0.5px;
  }
}

.nav-menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
  
  .nav-text {
    font-size: 14px;
    font-weight: 500;
  }
  
  &:hover {
    background-color: var(--color-bg-primary);
    color: var(--color-text-primary);
  }
  
  &.active {
    background-color: var(--color-bg-primary);
    color: var(--color-text-primary);
    
    .nav-icon {
      color: var(--color-accent);
    }
  }
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-border);
  margin-top: auto;
}
</style>
