<template>
  <div class="home-page" @scroll="handleScroll" ref="scrollContainer">
    <div class="scroll-content">
      <!-- 手的图片 -->
      <div 
        class="hand-image" 
        :style="{
          transform: `translateY(${handTransform}px)`,
          opacity: handOpacity
        }"
      >
        <img src="/手.png" alt="手" />
      </div>
      
      <!-- 硬币图片 -->
      <div 
        class="coin-image"
        :style="{
          transform: `translate(-50%, -50%) rotate(${coinRotation}deg) scale(${coinScale})`,
        }"
      >
        <img src="/硬币.png" alt="硬币" />
      </div>

      <!-- 初始状态：手拿硬币 -->
      <div 
        class="hand-coin-image"
        :style="{
          opacity: initialOpacity
        }"
      >
        <img src="/手拿硬币.png" alt="手拿硬币" />
      </div>

      <!-- 占位内容，用于产生滚动空间 -->
      <div class="spacer"></div>
      
      <!-- 后续内容区域 -->
      <div class="content-section" :style="{ opacity: contentOpacity }">
        <h1>区块链非原子套利交易识别</h1>
        <p>Uniswap V3 与 Binance 套利分析系统</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const scrollContainer = ref<HTMLElement | null>(null)
const scrollProgress = ref(0)

// 初始组合图片的透明度
const initialOpacity = ref(1)

// 手的变换
const handTransform = ref(0)
const handOpacity = ref(0)

// 硬币的变换
const coinRotation = ref(0)
const coinScale = ref(1)

// 内容区域透明度
const contentOpacity = ref(0)

const handleScroll = (event: Event) => {
  const target = event.target as HTMLElement
  const scrollTop = target.scrollTop
  const maxScroll = 1500 // 定义动画完成的滚动距离
  
  // 计算滚动进度 (0-1)
  scrollProgress.value = Math.min(scrollTop / maxScroll, 1)
  
  // 第一阶段：初始图片淡出，分离的手和硬币淡入 (0-0.3)
  if (scrollProgress.value <= 0.3) {
    const phase1Progress = scrollProgress.value / 0.3
    initialOpacity.value = 1 - phase1Progress
    handOpacity.value = phase1Progress
  } else {
    initialOpacity.value = 0
    handOpacity.value = 1
  }
  
  // 第二阶段：手向上移动脱离页面 (0.3-0.7)
  if (scrollProgress.value > 0.3 && scrollProgress.value <= 0.7) {
    const phase2Progress = (scrollProgress.value - 0.3) / 0.4
    handTransform.value = -phase2Progress * 600 // 向上移动600px
  } else if (scrollProgress.value > 0.7) {
    handTransform.value = -600
    handOpacity.value = Math.max(0, 1 - (scrollProgress.value - 0.7) / 0.1)
  }
  
  // 硬币旋转和放大 (0.3-1.0)
  if (scrollProgress.value > 0.3) {
    const coinProgress = (scrollProgress.value - 0.3) / 0.7
    coinRotation.value = coinProgress * 720 // 旋转两圈
    coinScale.value = 1 + coinProgress * 2 // 放大到3倍
  }
  
  // 内容区域淡入 (0.8-1.0)
  if (scrollProgress.value > 0.8) {
    contentOpacity.value = (scrollProgress.value - 0.8) / 0.2
  }
}

onMounted(() => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollTop = 0
  }
})
</script>

<style scoped>
.home-page {
  width: 100vw;
  height: 100vh;
  overflow-y: scroll;
  overflow-x: hidden;
  scroll-behavior: smooth;
}

.scroll-content {
  position: relative;
  width: 100%;
  min-height: 300vh;
}

.hand-coin-image {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  transition: opacity 0.3s ease-out;
}

.hand-coin-image img {
  width: auto;
  height: 60vh;
  max-width: 90vw;
  object-fit: contain;
}

.hand-image {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
  transition: transform 0.3s ease-out, opacity 0.3s ease-out;
}

.hand-image img {
  width: auto;
  height: 60vh;
  max-width: 90vw;
  object-fit: contain;
}

.coin-image {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 3;
  transition: transform 0.3s ease-out;
}

.coin-image img {
  width: auto;
  height: 30vh;
  max-width: 90vw;
  object-fit: contain;
}

.spacer {
  height: 200vh;
}

.content-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transition: opacity 0.5s ease-out;
}

.content-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  text-align: center;
}

.content-section p {
  font-size: 1.5rem;
  text-align: center;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .content-section h1 {
    font-size: 2rem;
  }
  
  .content-section p {
    font-size: 1.2rem;
  }
}
</style>
