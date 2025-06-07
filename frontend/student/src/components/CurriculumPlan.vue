<template>
  <div class="page-container">
    <div class="inner-container">
      <div class="header-row">
        <h1>定制培养方案</h1>
      </div>

      <div class="controls-row">
        <div class="search-container">
          <input type="text" v-model="searchCourseId" placeholder="搜索课程ID" class="search-input">
          <input type="text" v-model="searchCourseName" placeholder="搜索课程名称" class="search-input">
          <input type="text" v-model="searchCourseDept" placeholder="搜索课程学科" class="search-input">
          <button @click="searchCourses" class="search-btn">查询</button>
        </div>
        <div class="button-container">
          <button @click="showCurriculum" class="confirm-btn">我的培养方案</button>
          <button @click="toggleActionMenu" class="confirm-btn" style="margin-top: 10px;">确认</button>
        </div>
      </div>
      <div v-if="showCurriculumModal" class="modal-overlay">
        <div class="curriculum-modal">
          <h2 style="margin-top: 0;">我的培养方案</h2>
          <table class="curriculum-table">
            <thead>
            <tr>
              <th>课程ID</th>
              <th>课程名称</th>
              <th>课程学分</th>
              <th>课程学科</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="course in curriculumCourses" :key="course.courseId">
              <td>{{ course.courseId }}</td>
              <td>{{ course.title }}</td>
              <td>{{ course.credit }}</td>
              <td>{{ course.deptName }}</td>
            </tr>
            <tr v-if="curriculumCourses.length === 0">
              <td colspan="4">暂无已添加的课程</td>
            </tr>
            </tbody>
          </table>
          <button @click="closeCurriculumModal" class="confirm-btn"
                  style="margin-top: 15px; display: block; margin-left: auto;" >
            关闭
          </button>
        </div>
      </div>

      <form id="courseForm">
        <table id="courseTable">
          <thead>
          <tr>
            <th>选择</th>
            <th>课程ID</th>
            <th>课程名称</th>
            <th>课程学分</th>
            <th>课程学科</th>
            <th>状态</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="course in courses" :key="course.courseId">
            <td><input type="checkbox" v-model="selectedCourses" :value="course"></td>
            <td>{{ course.courseId }}</td>
            <td>{{ course.title }}</td>
            <td>{{ course.credit }}</td>
            <td>{{ course.deptName }}</td>
            <td>{{ course.status }}</td>
          </tr>
          </tbody>
        </table>
        <div v-if="showActionMenu" class="modal-overlay">
          <div class="action-menu">
            <p style="margin-bottom: 20px; font-size: 18px;">你希望的操作</p>
            <ul>
              <button type="button" @click="confirmSelection">添加课程</button>
              <button type="button" @click="confirmRemove">删除课程</button>
              <button type="button" @click="cancelAction">取消</button>
            </ul>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      allCourses: [],
      courses: [],
      selectedCourses: [],
      showCurriculumModal: false, // 控制培养方案模态框显示
      showActionMenu: false, // 控制菜单显示
      curriculumCourses: [],
      searchCourseId: '',
      searchCourseName: '',
      searchCourseDept: '',
      userId: this.$route.params.userId || '', // Initialize userId as null
    };
  },
  
  mounted() {
    // Assign userId from route params
    const idFromRoute = this.$route.params.userId;
    if (idFromRoute) {
      this.userId = parseInt(idFromRoute, 10); // Use parseInt to convert the string to an integer
    this.fetchCourses();
    } else {
      this.userId=1;
      this.fetchCourses();
    }
  },
  methods: {
    async fetchCourses() {
      try {
        const response = await fetch('http://localhost:8080/student/getAllCourses');
        if (!response.ok) throw new Error('网络响应失败');
        let data = await response.json();
        
        // Use Promise.all to wait for all status fetches to complete
        const coursesWithStatus = await Promise.all(data.map(async (course) => {
          const status = await this.getCourseStatus(course);
          return { ...course, status };
        }));

        this.allCourses = coursesWithStatus;
        this.courses = [...this.allCourses];

      } catch (error) {
        console.error('获取课程失败:', error);
        alert('无法加载课程，请刷新重试');
      }
    },

    async searchCourses() {
        // For simplicity, this example will filter the already fetched allCourses list.
        // You can also implement a backend search endpoint if needed.
        let filteredCourses = [...this.allCourses];

        if (this.searchCourseId.trim()) {
            filteredCourses = filteredCourses.filter(course =>
                course.courseId.toString().includes(this.searchCourseId.trim())
            );
        }
        if (this.searchCourseName.trim()) {
            filteredCourses = filteredCourses.filter(course =>
                course.title.toLowerCase().includes(this.searchCourseName.trim().toLowerCase())
            );
        }
        if (this.searchCourseDept.trim()) {
            filteredCourses = filteredCourses.filter(course =>
                course.deptName.toLowerCase().includes(this.searchCourseDept.trim().toLowerCase())
            );
        }
        this.courses = filteredCourses;
    },

    showCurriculum() {
      this.curriculumCourses = this.allCourses.filter(course => course.status === '已添加');
      this.showCurriculumModal = true;
    },
    
    closeCurriculumModal() {
      this.showCurriculumModal = false;
    },

    toggleActionMenu() {
      if (this.selectedCourses.length === 0) {
        alert('请至少选择一门课程');
        return;
      }
      this.showActionMenu = !this.showActionMenu;
    },

    cancelAction() {
      this.showActionMenu = false;
    },

    async confirmSelection() {
      try {
        const response = await fetch('http://localhost:8080/student/setPersonalCurriculum', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            userId: this.userId,
            courseIds: this.selectedCourses.map(course => course.courseId)
          })
        });
        if (!response.ok) throw new Error(await response.text());
        alert(await response.text());
        
        this.selectedCourses.forEach(selectedCourse => {
          const course = this.allCourses.find(c => c.courseId === selectedCourse.courseId);
          if (course) course.status = '已添加';
        });

        this.showActionMenu = false;
        this.selectedCourses = [];
      } catch (error) {
        console.error('提交失败:', error);
        alert(`定制失败: ${error.message}`);
      }
    },

    async confirmRemove() {
      try {
        const response = await fetch('http://localhost:8080/student/removePersonalCurriculum', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            userId: this.userId,
            courseIds: this.selectedCourses.map(course => course.courseId)
          })
        });
        if (!response.ok) throw new Error(await response.text());
        alert(await response.text());

        this.selectedCourses.forEach(selectedCourse => {
          const course = this.allCourses.find(c => c.courseId === selectedCourse.courseId);
          if (course) course.status = '待添加';
        });

        this.showActionMenu = false;
        this.selectedCourses = [];
      } catch (error) {
        console.error('删除失败:', error);
        alert(`删除失败: ${error.message}`);
      }
    },

    async getCourseStatus(course) {
      if (!this.userId) return '未知状态'; // Prevent API call if userId is not set
      try {
        const response = await fetch(`http://localhost:8080/student/getCourseStatus?userId=${this.userId}&courseId=${course.courseId}`);
        if (!response.ok) throw new Error('获取课程状态失败');
        const result = await response.json();
        return result === 1 ? '已添加' : '待添加';
      } catch (error) {
        console.error('获取课程状态失败:', error);
        return '未知状态';
      }
    },
  }
};
</script>

<style scoped>
.page-container {
  width: 100%;
  flex-grow: 1;
  padding: 20px;
  box-sizing: border-box;
}

.inner-container {
  background-color: #f8f9fa;
  padding: 30px 40px 40px;
  border-radius: 8px;
}

.inner-container h1 {
  font-size: 30px;
  font-weight: 600;
  color: #0d47a1;
  margin: 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  background-color: white;
}

.header-row {
  margin-bottom: 20px;
}

.controls-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.search-container {
  margin-top: 50px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-input {
  padding: 8px;
  width: 300px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-btn {
  padding: 8px 15px;
  background-color: #0d47a1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-btn:hover {
  background-color: #1565c0;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.confirm-btn {
  padding: 10px 20px;
  background-color: #0d47a1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap;
}

.confirm-btn:hover {
  background-color: #1565c0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.curriculum-modal {
  background-color: #ffffff;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  z-index: 10000;
}

.curriculum-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.curriculum-table th,
.curriculum-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

.curriculum-table th {
  background-color: #0d47a1;
  color: white;
}

th,
td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

th {
  background-color: #0d47a1;
  color: white;
  font-weight: bold;
}

.action-menu {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  text-align: center;
  z-index: 10000;
}

.action-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.action-menu button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  color: white;
  min-width: 100px;
}

.action-menu button:hover {
  opacity: 0.9;
}

.action-menu button:nth-child(1) {
  background-color: #4caf50;
}

.action-menu button:nth-child(2) {
  background-color: #f44336;
}

.action-menu button:nth-child(3) {
  background-color: #9e9e9e;
}
</style>