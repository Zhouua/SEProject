<template>
  <div class="header">
    <div class="header-left">
      <el-icon class="back-icon" v-if="showBackButton" @click="goBack">
        <ArrowLeft />
      </el-icon>
      <h1 class="page-title">{{ pageTitle }}</h1>
    </div>

    <div class="header-center">
      <div class="search-bar">
        <el-icon class="search-icon"><Search /></el-icon>
        <input 
          type="text" 
          placeholder="Search coins, markets, or portfolio..." 
          v-model="searchQuery"
        />
      </div>
    </div>

    <div class="header-right">
      <div class="header-icon" @click="toggleNotifications">
        <el-icon><ChatDotRound /></el-icon>
      </div>
      <div class="header-icon" @click="toggleNotifications">
        <el-icon><Bell /></el-icon>
        <span class="notification-badge" v-if="hasNotifications"></span>
      </div>
      <div class="user-avatar">
        <img src="https://i.pravatar.cc/150?img=12" alt="User Avatar" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Search, ChatDotRound, Bell } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const searchQuery = ref('')
const hasNotifications = ref(true)

const pageTitle = computed(() => {
  const titles = {
    '/dashboard': 'Welcome back, Michael!',
    '/trade': 'Trade',
    '/wallet': 'Wallet',
    '/markets': 'Markets',
    '/transactions': 'Transactions',
    '/buy-crypto': 'Buy Crypto',
    '/sell-crypto': 'Sell Crypto',
    '/convert': 'Convert',
    '/referral': 'Referral',
    '/assets': 'Assets',
  }
  
  if (route.path.startsWith('/crypto/')) {
    return 'Crypto details'
  }
  
  return titles[route.path] || 'TradoX'
})

const showBackButton = computed(() => {
  return route.path.startsWith('/crypto/') || route.path === '/assets'
})

const goBack = () => {
  router.back()
}

const toggleNotifications = () => {
  // 实现通知功能
}
</script>

<style lang="scss" scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
  padding: 0 32px;
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
  
  .back-icon {
    font-size: 24px;
    color: #666;
    cursor: pointer;
    
    &:hover {
      color: #1a1a1a;
    }
  }
  
  .page-title {
    font-size: 20px;
    font-weight: 600;
    color: #1a1a1a;
    margin: 0;
  }
}

.header-center {
  flex: 1;
  max-width: 600px;
  margin: 0 32px;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background-color: #f5f5f5;
  border-radius: 24px;
  
  .search-icon {
    font-size: 20px;
    color: #999;
  }
  
  input {
    flex: 1;
    border: none;
    background: transparent;
    outline: none;
    font-size: 14px;
    color: #1a1a1a;
    
    &::placeholder {
      color: #999;
    }
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  position: relative;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2C2C2C;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s;
  
  .el-icon {
    font-size: 20px;
    color: #ffffff;
  }
  
  &:hover {
    background-color: #3C3C3C;
  }
  
  .notification-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 8px;
    height: 8px;
    background-color: #F44336;
    border-radius: 50%;
  }
}

.user-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}
</style>
