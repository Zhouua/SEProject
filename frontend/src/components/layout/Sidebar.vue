<template>
  <div class="sidebar">
    <div class="logo">
      <div class="logo-icon">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <rect width="32" height="32" rx="8" fill="#4CAF50"/>
          <path d="M16 8L22 16L16 24L10 16L16 8Z" fill="white"/>
        </svg>
      </div>
      <span class="logo-text">TradoX</span>
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
        <span class="nav-text">{{ item.name }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <router-link to="/help" class="nav-item">
        <el-icon :size="16" class="nav-icon"><QuestionFilled /></el-icon>
        <span class="nav-text">Help Center</span>
      </router-link>
      <router-link to="/settings" class="nav-item">
        <el-icon :size="16" class="nav-icon"><Setting /></el-icon>
        <span class="nav-text">Settings</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
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

const menuItems = [
  { name: 'Dashboard', path: '/dashboard', icon: Grid },
  { name: 'Trade', path: '/trade', icon: TrendCharts },
  { name: 'Wallet', path: '/wallet', icon: Wallet },
  { name: 'Markets', path: '/markets', icon: DataAnalysis },
  { name: 'Transactions', path: '/transactions', icon: Tickets },
  { name: 'Buy Crypto', path: '/buy-crypto', icon: CirclePlus },
  { name: 'Sell Crypto', path: '/sell-crypto', icon: Remove },
  { name: 'Convert', path: '/convert', icon: RefreshRight },
  { name: 'Referral', path: '/referral', icon: Present },
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
