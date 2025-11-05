<template>
  <div class="markets-page">
    <div class="markets-container">
      <!-- 中央手机图片 -->
      <div class="phone-display">
        <img src="@/assets/phone-hand.png" alt="Mobile App" class="phone-image" />
      </div>

      <!-- 左上角卡片 -->
      <div class="stat-card top-left">
        <div class="stat-value">13.66min</div>
        <div class="stat-label">{{ t('markets.saveTime') }}</div>
      </div>

      <!-- 右上角卡片 -->
      <div class="stat-card top-right">
        <div class="stat-value">56%</div>
        <div class="stat-label">{{ t('markets.adoptionRate') }}</div>
      </div>

      <!-- 左下角卡片 -->
      <div class="stat-card bottom-left">
        <div class="stat-value">28.74%</div>
        <div class="stat-label">{{ t('markets.profitMargin') }}</div>
      </div>

      <!-- 右下角卡片 -->
      <div class="stat-card bottom-right">
        <div class="stat-value">8pt</div>
        <div class="stat-label">{{ t('markets.efficiency') }}</div>
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
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style lang="scss" scoped>
.markets-page {
  width: 100%;
  min-height: calc(100vh - 72px);
  background: linear-gradient(135deg, #f0f9f4 0%, #e8f5e9 50%, #ffffff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  position: relative;
  overflow: hidden;
  animation: fadeInPage 0.8s ease-out;
}

@keyframes fadeInPage {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.markets-container {
  position: relative;
  width: 100%;
  max-width: 1200px;
  height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

// 中央手机显示
.phone-display {
  position: relative;
  z-index: 10;
  animation: float 3s ease-in-out infinite;
  
  .phone-image {
    width: 350px;
    height: auto;
    filter: drop-shadow(0 20px 40px rgba(76, 175, 80, 0.3));
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

// 统计卡片通用样式
.stat-card {
  position: absolute;
  background: white;
  border-radius: 16px;
  padding: 24px 32px;
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.15);
  border: 2px solid rgba(76, 175, 80, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 32px rgba(76, 175, 80, 0.25);
    border-color: rgba(76, 175, 80, 0.3);
  }
  
  .stat-value {
    font-size: 36px;
    font-weight: 700;
    color: #4CAF50;
    margin-bottom: 8px;
    background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .stat-label {
    font-size: 14px;
    color: #666;
    font-weight: 500;
  }
}

// 卡片位置
.top-left {
  top: 60px;
  left: 80px;
  animation: slideInLeft 1s ease-out;
}

.top-right {
  top: 60px;
  right: 80px;
  animation: slideInRight 1s ease-out;
}

.bottom-left {
  bottom: 60px;
  left: 80px;
  animation: slideInLeft 1.2s ease-out;
}

.bottom-right {
  bottom: 60px;
  right: 80px;
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
  .markets-container {
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
