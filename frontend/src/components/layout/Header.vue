<template>
  <div class="header">
    <div class="header-left">
      <!-- 侧边栏切换按钮 -->
      <div class="menu-toggle" @click="toggleSidebar">
        <div class="hamburger" :class="{ active: sidebarOpen }">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
      
      <el-icon class="back-icon" v-if="showBackButton" @click="goBack">
        <ArrowLeft />
      </el-icon>
      
      <router-link to="/welcome" class="logo-section">
        <div class="logo-icon">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="8" fill="#4CAF50"/>
            <path d="M16 8L22 16L16 24L10 16L16 8Z" fill="white"/>
          </svg>
        </div>
        <div class="page-title-section">
          <h1 class="page-title">Trade0</h1>
          <p class="page-subtitle">Uniswap V3 vs Binance</p>
        </div>
      </router-link>
    </div>

    <div class="header-center">
      <div class="search-bar">
        <el-icon class="search-icon"><Search /></el-icon>
        <input 
          type="text" 
          :placeholder="t('header.search')" 
          v-model="searchQuery"
        />
      </div>
    </div>

    <div class="header-right">
      <div class="header-icon lang-switch" @click="toggleLanguage">
        <span class="lang-text">{{ locale === 'zh' ? '中' : 'EN' }}</span>
      </div>
      <div class="header-icon" @click="showNotificationDialog = true">
        <el-icon><Bell /></el-icon>
        <span class="notification-badge" v-if="hasNotifications"></span>
      </div>
      <div class="user-avatar">
        <img src="@/assets/avatar.png" alt="User Avatar" />
      </div>
    </div>
  </div>

  <!-- 通知模态框 -->
  <el-dialog
    v-model="showNotificationDialog"
    :title="t('notification.title')"
    width="500px"
    class="notification-dialog"
  >
    <div class="notification-header">
      <el-button text @click="markAllAsRead">{{ t('notification.markAllRead') }}</el-button>
    </div>
    <div class="notification-list">
      <div 
        v-if="notifications.length === 0" 
        class="no-notifications"
      >
        {{ t('notification.noNotifications') }}
      </div>
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        class="notification-item"
        :class="{ unread: !notification.read }"
        @click="markAsRead(notification.id)"
      >
        <div class="notification-icon" :class="notification.type">
          <el-icon v-if="notification.type === 'success'"><SuccessFilled /></el-icon>
          <el-icon v-else-if="notification.type === 'warning'"><WarningFilled /></el-icon>
          <el-icon v-else-if="notification.type === 'info'"><InfoFilled /></el-icon>
          <el-icon v-else><Bell /></el-icon>
        </div>
        <div class="notification-content">
          <div class="notification-title">
            {{ notification.title }}
            <span v-if="!notification.read" class="new-badge">{{ t('notification.new') }}</span>
          </div>
          <div class="notification-message">{{ notification.message }}</div>
          <div class="notification-time">{{ formatTime(notification.time) }}</div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ArrowLeft, Search, Bell, SuccessFilled, WarningFilled, InfoFilled, DArrowLeft, DArrowRight } from '@element-plus/icons-vue'
import { api } from '@/api'

// 定义 props
const props = defineProps({
  sidebarOpen: {
    type: Boolean,
    default: true
  }
})

// 定义 emit
const emit = defineEmits(['toggle-sidebar'])

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()

const searchQuery = ref('')
const hasNotifications = ref(true)
const showNotificationDialog = ref(false)
const loading = ref(false)

// 切换侧边栏
const toggleSidebar = () => {
  emit('toggle-sidebar')
}

// Git Commit 通知数据 - 从 API 动态获取
const notifications = ref([])

// 加载 Git Commit 通知
const loadCommits = async () => {
  loading.value = true
  try {
    const response = await api.getCommits(10)
    if (response.success && response.data) {
      notifications.value = response.data.map(commit => ({
        id: commit.id,
        type: commit.type,
        title: commit.title,
        message: locale.value === 'zh' 
          ? `提交者: ${commit.author} | 提交哈希: ${commit.hash}` 
          : `Author: ${commit.author} | Commit: ${commit.hash}`,
        time: new Date(commit.timestamp),
        timeAgo: commit.time_ago,
        read: commit.read
      }))
      updateHasNotifications()
    }
  } catch (error) {
    console.error('加载提交记录失败:', error)
  } finally {
    loading.value = false
  }
}

// 组件挂载时加载通知
onMounted(() => {
  loadCommits()
})

const showBackButton = computed(() => {
  return route.path.startsWith('/crypto/') || route.path === '/assets'
})

const goBack = () => {
  router.back()
}

const toggleLanguage = () => {
  locale.value = locale.value === 'zh' ? 'en' : 'zh'
  // 更新通知内容语言
  updateNotificationLanguage()
}

const updateNotificationLanguage = () => {
  // 重新加载通知以更新语言
  notifications.value = notifications.value.map(n => ({
    ...n,
    message: locale.value === 'zh' 
      ? `提交者: ${n.message.split('|')[0].split(':')[1].trim().split('Author')[0].trim()} | 提交哈希: ${n.message.split(':').pop().trim()}`
      : `Author: ${n.message.split('|')[0].split(':')[1].trim().split('提交者')[0].trim()} | Commit: ${n.message.split(':').pop().trim()}`
  }))
}

const markAsRead = (id) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification) {
    notification.read = true
  }
  updateHasNotifications()
}

const markAllAsRead = () => {
  notifications.value.forEach(n => n.read = true)
  updateHasNotifications()
}

const updateHasNotifications = () => {
  hasNotifications.value = notifications.value.some(n => !n.read)
}

const formatTime = (time) => {
  const now = new Date()
  const diff = now - time
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return t('notification.timeAgo.justNow')
  if (minutes < 60) return t('notification.timeAgo.minutesAgo', { n: minutes })
  if (hours < 24) return t('notification.timeAgo.hoursAgo', { n: hours })
  return t('notification.timeAgo.daysAgo', { n: days })
}
</script>

<style lang="scss" scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100px;
  padding: 0 32px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(224, 224, 224, 0.5);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
  
  .menu-toggle {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding: 8px;
    
    .hamburger {
      width: 24px;
      height: 18px;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      
      span {
        display: block;
        height: 2px;
        width: 100%;
        background-color: #4CAF50;
        border-radius: 2px;
        transition: all 0.3s ease;
        
        &:nth-child(1) {
          transform-origin: left center;
        }
        
        &:nth-child(2) {
          transform-origin: center center;
        }
        
        &:nth-child(3) {
          transform-origin: left center;
        }
      }
      
      &.active {
        span {
          &:nth-child(1) {
            transform: rotate(45deg) translateY(-1px);
          }
          
          &:nth-child(2) {
            opacity: 0;
            transform: scaleX(0);
          }
          
          &:nth-child(3) {
            transform: rotate(-45deg) translateY(1px);
          }
        }
      }
    }
    
    &:hover {
      .hamburger span {
        background-color: #66BB6A;
      }
    }
  }
  
  .back-icon {
    font-size: 24px;
    color: #666;
    cursor: pointer;
    
    &:hover {
      color: #1a1a1a;
    }
  }
  
  .logo-section {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    cursor: pointer;
    transition: opacity 0.3s;
    
    &:hover {
      opacity: 0.8;
    }
    
    .logo-icon {
      width: 32px;
      height: 32px;
    }
    
    .page-title-section {
      .page-title {
        font-size: 20px;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0;
        line-height: 1.2;
      }
      
      .page-subtitle {
        font-size: 12px;
        color: #4CAF50;
        margin: 4px 0 0 0;
        font-weight: 600;
      }
    }
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
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #4a4a4a;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
  
  .el-icon {
    font-size: 18px;
    color: #ffffff;
  }
  
  &:hover {
    background-color: #5a5a5a;
    transform: scale(1.05);
  }
  
  .notification-badge {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 8px;
    height: 8px;
    background-color: #F44336;
    border-radius: 50%;
  }
  
  &.lang-switch {
    .lang-text {
      font-size: 13px;
      font-weight: 600;
      color: #ffffff;
    }
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

<style lang="scss">
.notification-dialog {
  .el-dialog__header {
    border-bottom: 1px solid #e0e0e0;
    padding: 20px;
  }
  
  .el-dialog__body {
    padding: 0;
    max-height: 500px;
    overflow-y: auto;
  }
}

.notification-header {
  padding: 12px 20px;
  border-bottom: 1px solid #f5f5f5;
  text-align: right;
}

.notification-list {
  .no-notifications {
    padding: 60px 20px;
    text-align: center;
    color: #999;
    font-size: 14px;
  }
}

.notification-item {
  display: flex;
  gap: 16px;
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: #fafafa;
  }
  
  &.unread {
    background-color: #f0f9ff;
    
    &:hover {
      background-color: #e0f2fe;
    }
  }
  
  .notification-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    
    .el-icon {
      font-size: 20px;
    }
    
    &.success {
      background-color: #E8F5E9;
      color: #4CAF50;
    }
    
    &.warning {
      background-color: #FFF3E0;
      color: #FF9800;
    }
    
    &.info {
      background-color: #E3F2FD;
      color: #2196F3;
    }
  }
  
  .notification-content {
    flex: 1;
    min-width: 0;
  }
  
  .notification-title {
    font-size: 14px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
    
    .new-badge {
      display: inline-block;
      padding: 2px 6px;
      background-color: #F44336;
      color: #ffffff;
      font-size: 10px;
      font-weight: 700;
      border-radius: 4px;
    }
  }
  
  .notification-message {
    font-size: 13px;
    color: #666;
    margin-bottom: 4px;
    line-height: 1.5;
  }
  
  .notification-time {
    font-size: 12px;
    color: #999;
  }
}
</style>
