<template>
  <div class="layout">
    <aside class="sidebar">
      <h2>学生信息系统</h2>
      <nav>
        <!--// lmt 查看选课结果（需传递 userId） -->
        <router-link
            :to="{
          name: 'CourseResultS',
          params: { userId: currentUserId }
        }"
            :class="{ active: $route.name === 'CourseResultS' }"
        >查看选课结果
        </router-link>
        <!--// lmt 查看课表（需传递 userId） -->
        <router-link
            :to="{
          name: 'CourseTableS',
          params: { userId: currentUserId }
        }"
            :class="{ active: $route.name === 'CourseTableS' }"
        >查看课表
        </router-link>
        <router-link :to="{ name: 'CurriculumPlan' }" :class="{ active: $route.name === 'CurriculumPlan' }">定制培养方案</router-link>
        <router-link :to="{ name: 'CourseInfoS' }" :class="{ active: $route.name === 'CourseInfoS' }">查询课程信息</router-link>
        <router-link :to="{ name: 'CourseSelectS' }" :class="{ active: $route.name === 'CourseSelectS' }">选择课程</router-link>
      </nav>
    </aside>
    <main class="content">
      <div class="top-bar">
        <div class="user-area" @click="toggleDropdown">
          <!-- <img src="https://i.pravatar.cc/40" alt="头像" class="avatar" /> -->
          <span class="username">学生姓名</span>
          <svg class="arrow" viewBox="0 0 1024 1024" width="12" height="12">
            <path d="M512 672L192 352h640z" fill="#333" />
          </svg>
        </div>
        <div :class="{ 'dropdown-menu': true, show: isDropdownVisible }" @click.outside="closeDropdown">
          <div class="dropdown-item" @click="logout">退出登录</div>
        </div>
      </div>
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
// lmt
import { ref, computed,onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// lmt
// 初始值设为路由参数或空字符串（避免 undefined）
const currentUserId = computed(() => {
  return route.params.userId || localStorage.getItem('studentId') || 'default-user-id';
});

// 使用 computed 声明（适用于依赖其他响应式数据）
const userId = computed(() => {
  return route.params.userId || localStorage.getItem('studentId') || 'default';
});
// lmt
// 可选：在组件挂载后验证 userId
onMounted(() => {
  if (!userId.value) {
    console.warn('未获取到有效的 userId，可能导致导航错误');
    // 可选择跳转到登录页或其他处理
  }
});

const isDropdownVisible = ref(false);

const toggleDropdown = () => {
  isDropdownVisible.value = !isDropdownVisible.value;
};

const closeDropdown = () => {
  isDropdownVisible.value = false;
};

const logout = () => {
  alert('退出登录');
  // 这里可以添加真正的退出逻辑，比如跳转到登录页
  router.push('/login');
};
</script>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
}
/* 整个布局占满浏览器 */
.layout {
  display: flex;
  flex-direction: row;
  height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 侧边栏固定宽度 */
.sidebar {
  width: 240px;
  background: linear-gradient(180deg, #0d47a1, #1565c0);
  color: white;
  padding: 20px;
  box-sizing: border-box;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
}

.sidebar h2 {
  margin-bottom: 30px;
  font-size: 20px;
  font-weight: bold;
  letter-spacing: 1px;
}

.sidebar nav a {
  display: block;
  color: white;
  text-decoration: none;
  margin-bottom: 15px;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.sidebar nav a:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.sidebar nav a.active {
  font-weight: bold;
  border-left: 4px solid white;
  padding-left: 8px;
}

/* 内容区域 */
.content {
  flex: 1;
  height: 100vh;
  overflow-y: auto;
  background-color: #f5f5f5;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

/* 顶部栏 */
.top-bar {
  width: 100%;
  height: 60px;
  background-color: #ffffff;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0 30px;
  box-sizing: border-box;
  border-bottom: 1px solid #ddd;
  position: relative;
}

/* 用户信息区域 */
.user-area {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  font-size: 15px;
  color: #333;
  margin-right: 5px;
}

.arrow {
  transform: rotate(0deg);
  transition: transform 0.2s;
}

.user-area:hover .arrow {
  transform: rotate(180deg);
}

/* 下拉菜单 */
.dropdown-menu {
  position: absolute;
  top: 60px;
  right: 30px;
  background: white;
  border: 1px solid #ddd;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  overflow: hidden;
  z-index: 100;
  display: none;
}

.dropdown-menu.show {
  display: block;
}

.dropdown-item {
  padding: 10px 20px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: background-color 0.3s;
}

.dropdown-item:hover {
  background-color: #f0f0f0;
}
</style>