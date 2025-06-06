import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: { // <--- 添加 server 配置
    proxy: {
      // 将所有以 /api 开头的请求代理到后端服务
      '/api': {
        target: 'http://localhost:8080', // 您的后端Spring Boot服务地址和端口
        changeOrigin: true, // 必须设置为 true，表示服务器源改变
        // 如果您的后端API路径本身不包含 /api 前缀 (例如后端是 /teacher/... 而不是 /api/teacher/...)
        // 您可能需要添加路径重写规则，像下面这样:
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})