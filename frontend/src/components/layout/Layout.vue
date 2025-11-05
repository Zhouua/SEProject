<template>
  <div class="layout">
    <!-- Header 在最顶部 -->
    <Header :sidebar-open="isSidebarOpen" @toggle-sidebar="toggleSidebar" />
    
    <div class="layout-body">
      <!-- 侧边栏 -->
      <div class="sidebar-container" :class="{ collapsed: !isSidebarOpen }">
        <Sidebar />
      </div>
      
      <!-- 主内容区域 -->
      <div class="content-container">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import Sidebar from './Sidebar.vue'
import Header from './Header.vue'

const isSidebarOpen = ref(true)

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
  
  // 延迟触发 resize 事件，让动画完成后图表重绘
  nextTick(() => {
    setTimeout(() => {
      window.dispatchEvent(new Event('resize'))
    }, 300)
  })
}
</script>

<style lang="scss" scoped>
.layout {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  background-color: #f5f5f5;
  overflow: hidden;
}

.layout-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar-container {
  width: 240px;
  background-color: #ffffff;
  border-right: 1px solid #e0e0e0;
  overflow-y: auto;
  transition: all 0.3s ease;
  flex-shrink: 0;
  
  &.collapsed {
    width: 0;
    border-right: none;
    overflow: hidden;
  }
}

.content-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}
</style>
