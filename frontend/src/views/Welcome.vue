<template>
  <div class="welcome-wrapper">
    <!-- Header -->
    <div class="welcome-header">
      <div class="header-left">
        <div class="logo-section">
          <div class="logo-icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <rect width="32" height="32" rx="8" fill="#4CAF50"/>
              <path d="M16 8L22 16L16 24L10 16L16 8Z" fill="white"/>
            </svg>
          </div>
          <div>
            <h1 class="page-title">Trade0</h1>
            <p class="page-subtitle">Uniswap V3 vs Binance</p>
          </div>
        </div>
      </div>
      
      <div class="header-right">
        <div class="header-icon lang-switch" @click="toggleLanguage">
          <span class="lang-text">{{ locale === 'zh' ? '中' : 'EN' }}</span>
        </div>
      </div>
    </div>
    
    <!-- 欢迎页面内容 -->
    <div class="welcome-page" @wheel="handleScroll" @click="handleClick">
      <div class="welcome-container">
      <!-- 四个KPI指标卡片 -->
      <!-- 左上角卡片 - 数据准确性 -->
      <div class="stat-card top-left">
        <div class="stat-value">99.9%</div>
        <div class="stat-label">{{ t('welcome.dataAccuracy') }}</div>
      </div>

      <!-- 右上角卡片 - 时间覆盖率 -->
      <div class="stat-card top-right">
        <div class="stat-value">99.5%</div>
        <div class="stat-label">{{ t('welcome.timeCoverage') }}</div>
      </div>

      <!-- 左下角卡片 - 端到端延迟 -->
      <div class="stat-card bottom-left">
        <div class="stat-value">&lt;1s</div>
        <div class="stat-label">{{ t('welcome.endToEndLatency') }}</div>
      </div>

      <!-- 右下角卡片 - API响应时间 -->
      <div class="stat-card bottom-right">
        <div class="stat-value">&lt;500ms</div>
        <div class="stat-label">{{ t('welcome.apiResponseTime') }}</div>
      </div>

      <!-- 装饰性元素 -->
      <div class="decoration-dots">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
      
      <!-- 向下箭头提示 -->
      <div class="scroll-indicator">
        <div class="scroll-text">{{ t('welcome.scrollDown') }}</div>
        <div class="arrow-down">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const { t, locale } = useI18n()
const router = useRouter()

let isNavigating = ref(false)

// 切换语言
const toggleLanguage = () => {
  locale.value = locale.value === 'zh' ? 'en' : 'zh'
}

// 处理滚轮事件
const handleScroll = (event) => {
  if (isNavigating.value) return
  
  // 向下滚动
  if (event.deltaY > 0) {
    navigateToDashboard()
  }
}

// 处理点击事件
const handleClick = () => {
  if (isNavigating.value) return
  navigateToDashboard()
}

// 平滑跳转到 Dashboard
const navigateToDashboard = () => {
  isNavigating.value = true
  
  // 添加淡出动画
  const welcomePage = document.querySelector('.welcome-page')
  if (welcomePage) {
    welcomePage.style.transition = 'opacity 0.6s ease-out'
    welcomePage.style.opacity = '0'
  }
  
  // 延迟跳转，让淡出动画完成
  setTimeout(() => {
    router.push('/dashboard')
  }, 600)
}
</script>

<style lang="scss" scoped>
// 整体容器
.welcome-wrapper {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

// Header 样式
.welcome-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100px;
  padding: 0 32px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(224, 224, 224, 0.5);
  z-index: 100;
  
  .header-left {
    .logo-section {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .logo-icon {
        width: 32px;
        height: 32px;
      }
      
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
  
  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  
  .header-icon {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #4CAF50;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      background-color: #66BB6A;
      transform: scale(1.05);
    }
    
    &.lang-switch {
      .lang-text {
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
      }
    }
  }
}

.welcome-page {
  flex: 1;
  width: 100%;
  background-image: url('@/assets/phone-hand.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  opacity: 1;
  animation: fadeIn 0.8s ease-out;
}

.welcome-container {
  position: relative;
  width: 100%;
  max-width: 1200px;
  height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}


// 统计卡片通用样式
.stat-card {
  position: absolute;
  width: 300px;
  height: 120px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  
  &:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 16px 48px rgba(76, 175, 80, 0.25);
    background: rgba(255, 255, 255, 1);
    border-color: rgba(76, 175, 80, 0.3);
  }
  
  .stat-value {
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 8px;
    background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 50%, #66BB6A 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
  }
  
  .stat-label {
    font-size: 13px;
    color: #424242;
    font-weight: 600;
    line-height: 1.4;
  }
}

// 卡片位置
.top-left {
  top: 0px;
  left: 0px;
  animation: slideInLeft 1s ease-out;
}

.top-right {
  top: 0px;
  right: 0px;
  animation: slideInRight 1s ease-out;
}

.bottom-left {
  bottom: 0px;
  left: 0px;
  animation: slideInLeft 1.2s ease-out;
}

.bottom-right {
  bottom: 0px;
  right: 0px;
  animation: slideInRight 1.2s ease-out;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

// 装饰性点点
.decoration-dots {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  
  .dot {
    position: absolute;
    width: 8px;
    height: 8px;
    background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
    border-radius: 50%;
    opacity: 0.3;
    animation: twinkle 3s ease-in-out infinite;
    
    &:nth-child(1) {
      top: 20%;
      left: 15%;
      animation-delay: 0s;
    }
    
    &:nth-child(2) {
      top: 30%;
      right: 20%;
      animation-delay: 0.5s;
    }
    
    &:nth-child(3) {
      bottom: 25%;
      left: 25%;
      animation-delay: 1s;
    }
    
    &:nth-child(4) {
      bottom: 35%;
      right: 15%;
      animation-delay: 1.5s;
    }
    
    &:nth-child(5) {
      top: 50%;
      left: 10%;
      animation-delay: 2s;
    }
    
    &:nth-child(6) {
      top: 60%;
      right: 10%;
      animation-delay: 2.5s;
    }
  }
}

@keyframes twinkle {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.5);
  }
}

// 向下滚动提示
.scroll-indicator {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  z-index: 100;
  animation: bounce 2s ease-in-out infinite;
  cursor: pointer;
  
  .scroll-text {
    font-size: 14px;
    color: #2E7D32;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    text-shadow: 0 2px 4px rgba(255, 255, 255, 0.8);
  }
  
  .arrow-down {
    width: 30px;
    height: 30px;
    position: relative;
    
    span {
      position: absolute;
      top: 0;
      left: 50%;
      width: 12px;
      height: 12px;
      margin-left: -6px;
      border-left: 2px solid #4CAF50;
      border-bottom: 2px solid #4CAF50;
      transform: rotate(-45deg);
      animation: arrowSlide 2s ease-in-out infinite;
      
      &:nth-child(1) {
        animation-delay: 0s;
        opacity: 0.3;
      }
      
      &:nth-child(2) {
        top: 8px;
        animation-delay: 0.15s;
        opacity: 0.6;
      }
      
      &:nth-child(3) {
        top: 16px;
        animation-delay: 0.3s;
        opacity: 1;
      }
    }
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateX(-50%) translateY(0);
  }
  50% {
    transform: translateX(-50%) translateY(-10px);
  }
}

@keyframes arrowSlide {
  0% {
    opacity: 0;
    transform: rotate(-45deg) translate(-10px, -10px);
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: rotate(-45deg) translate(10px, 10px);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

// 响应式设计
@media (max-width: 1024px) {
  .phone-display .phone-image {
    width: 280px;
  }
  
  .stat-card {
    padding: 20px 24px;
    
    .stat-value {
      font-size: 28px;
    }
    
    .stat-label {
      font-size: 12px;
    }
  }
  
  .top-left, .bottom-left {
    left: 40px;
  }
  
  .top-right, .bottom-right {
    right: 40px;
  }
}

@media (max-width: 768px) {
  .welcome-container {
    height: 500px;
  }
  
  .phone-display .phone-image {
    width: 220px;
  }
  
  .stat-card {
    padding: 16px 20px;
    
    .stat-value {
      font-size: 24px;
    }
    
    .stat-label {
      font-size: 11px;
    }
  }
  
  .top-left, .bottom-left {
    left: 20px;
  }
  
  .top-right, .bottom-right {
    right: 20px;
  }
}
</style>
