<template>
  <div class="sidebar">
    <div class="logo">
      <div class="logo-icon">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <rect width="32" height="32" rx="8" fill="#4CAF50"/>
          <path d="M16 8L22 16L16 24L10 16L16 8Z" fill="white"/>
        </svg>
      </div>
      <span class="logo-text">Trade0</span>
    </div>

    <nav class="nav-menu">
      <router-link 
        v-for="item in menuItems" 
        :key="item.path" 
        :to="item.path"
        class="nav-item"
        :class="{ 'active': isActive(item.path) }"
      >
        <el-icon :size="16" class="nav-icon">
          <component :is="item.icon" />
        </el-icon>
        <span class="nav-text">{{ t(item.nameKey) }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <router-link to="/help" class="nav-item">
        <el-icon :size="16" class="nav-icon"><QuestionFilled /></el-icon>
        <span class="nav-text">{{ t('sidebar.helpCenter') }}</span>
      </router-link>
      <router-link to="/settings" class="nav-item">
        <el-icon :size="16" class="nav-icon"><Setting /></el-icon>
        <span class="nav-text">{{ t('sidebar.settings') }}</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { 
  Grid, 
  TrendCharts, 
  Wallet, 
  DataAnalysis,
  Tickets,
  CirclePlus,
  Remove,
  RefreshRight,
  Present,
  QuestionFilled,
  Setting
} from '@element-plus/icons-vue'

const route = useRoute()
const { t } = useI18n()

const menuItems = [
  { nameKey: 'sidebar.dashboard', path: '/dashboard', icon: Grid },
  { nameKey: 'sidebar.trade', path: '/trade', icon: TrendCharts },
  { nameKey: 'sidebar.wallet', path: '/wallet', icon: Wallet },
  { nameKey: 'sidebar.markets', path: '/markets', icon: DataAnalysis },
  { nameKey: 'sidebar.transactions', path: '/transactions', icon: Tickets },
  { nameKey: 'sidebar.buyCrypto', path: '/buy-crypto', icon: CirclePlus },
  { nameKey: 'sidebar.sellCrypto', path: '/sell-crypto', icon: Remove },
  { nameKey: 'sidebar.convert', path: '/convert', icon: RefreshRight },
  { nameKey: 'sidebar.referral', path: '/referral', icon: Present },
]

const isActive = (path) => {
  return route.path === path
}
</script>

<style lang="scss" scoped>
.sidebar {
  width: 240px;
  background-color: #ffffff;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  padding: 24px 0;
}

.logo {
  display: flex;
  align-items: center;
  padding: 0 24px 32px;
  gap: 12px;
  
  .logo-icon {
    width: 32px;
    height: 32px;
  }
  
  .logo-text {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a1a;
  }
}

.nav-menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  color: #666666;
  text-decoration: none;
  transition: all 0.3s;
  cursor: pointer;
  
  .nav-icon {
    flex-shrink: 0;
  }
  
  .nav-text {
    font-size: 14px;
    font-weight: 500;
  }
  
  &:hover {
    background-color: #f5f5f5;
    color: #1a1a1a;
  }
  
  &.active {
    background-color: #E8F5E9;
    color: #4CAF50;
    font-weight: 600;
  }
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px 12px 0;
  border-top: 1px solid #e0e0e0;
}
</style>
