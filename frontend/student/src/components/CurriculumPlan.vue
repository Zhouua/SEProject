<!-- zza -->
<template>
  <div class="page-container">
    <div class="inner-container">
      <div class="header-row">
        <h1>定制培养方案</h1>
        <div class="button-container">
          <button @click="showCurriculum" class="confirm-btn">我的培养方案</button>
          <button @click="toggleActionMenu" class="confirm-btn" style="margin-top: 10px;">确认操作</button>
        </div>
      </div>
      <!-- 展示培养方案的模态框 -->
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
          <tr v-for="course in courses" :key="course.title">
            <td><input type="checkbox" v-model="selectedCourses" :value="course"></td>
            <td>{{ course.courseId }}</td>
            <td>{{ course.title }}</td>
            <td>{{ course.credit }}</td>
            <td>{{ course.deptName }}</td>
            <td>{{ course.status }}</td>
          </tr>
          </tbody>
        </table>
        <!--  浮动菜单 -->
        <div v-if="showActionMenu" class="modal-overlay">
          <div class="action-menu">
            <p style="margin-bottom: 20px; font-size: 18px;">你希望的操作</p>
            <ul>
              <button type="button" @click="confirmSelection">培养方案添加课程</button>
              <button type="button" @click="confirmRemove">培养方案移除课程</button>
              <button type="button" @click="cancelAction">取消我的操作</button>
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
      courses: [
        { courseId: '001', title: '人工智能导论', credit: 3, deptName: '人工智能', status: '待添加' },
        { courseId: '002', title: '数据挖掘基础', credit: 3, deptName: '软件工程', status: '已添加' },
        { courseId: '003', title: '机器学习算法', credit: 4, deptName: '计算机', status: '待添加' }
      ],
      selectedCourses: [],
      showCurriculumModal: false, // 控制培养方案模态框显示
      showActionMenu: false, // 控制菜单显示
    };
  },
  mounted() {
    this.fetchCourses();
  },
  methods: {
    fetchCourses() {
      const userId = 1; // 默认userId为1，需要更改！
      // 获取课程数据
      fetch('http://localhost:8080/student/getAllCourses')
        .then(response => {
          if (!response.ok) {
            throw new Error('网络响应失败');
          }
          return response.json();
        })
        .then(data => {
          this.courses = data;  // 将返回的课程数据赋值给 courses
          console.log('Courses:', this.courses);
          // 获取每门课程的状态
          this.courses.forEach(course => {
            this.getCourseStatus(course).then(status => {
              course.status = status; // 更新课程状态
            });
          });
        })
        .catch(error => {
          console.error('获取课程失败:', error);
          alert('无法加载课程，请刷新重试');
        });
    },
    showCurriculum() {
      this.curriculumCourses = this.courses.filter(course => course.status === '已添加');
      this.showCurriculumModal = true;
    },
    // 关闭“我的培养方案”模态框
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
      this.showActionMenu = false; // 取消操作，隐藏菜单
    },
    async confirmSelection() {
      try {
        const courseIds = this.selectedCourses.map(course => course.courseId);
        console.log('Selected courses:', courseIds);
        const response = await fetch('http://localhost:8080/student/setPersonalCurriculum', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          },
          //  注意，这里的studentId 是从登录页面获取的，请根据实际情况修改
          body: JSON.stringify({
            userId: 1,
            courseIds: this.selectedCourses.map(course => course.courseId) // 提取所有 courseId
          })
        });

        if (!response.ok) {
          const errorMessage = await response.text(); // 获取错误信息
          alert(errorMessage); // 显示给用户
          return;
        }

        const successMessage = await response.text();
      alert(successMessage); // 比如 “添加课程进入培养方案成功”
        this.selectedCourses.forEach(selectedCourse => {
          const course = this.courses.find(c => c.courseId === selectedCourse.courseId);
          if (course) {
            course.status = '已添加';
          }
        });
        this.showActionMenu = false; // 隐藏菜单
      this.selectedCourses = []; // 清空选中课程

      } catch (error) {
        console.error('提交失败:', error);
        alert('定制失败，请稍后重试');
      }
    },
    async confirmRemove() {
      try {
        const courseIds = this.selectedCourses.map(course => course.courseId);
        console.log('Selected courses for removal:', courseIds);
        const response = await fetch('http://localhost:8080/student/removePersonalCurriculum', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            userId: 1,
            courseIds: courseIds // 提取所有 courseId
          })
        });

        if (!response.ok) {
          const errorMessage = await response.text(); // 获取错误信息
          alert(errorMessage); // 显示给用户
          return;
        }

        const successMessage = await response.text();
        alert(successMessage); // 比如 “删除课程进入培养方案成功”
        this.selectedCourses.forEach(selectedCourse => {
          const course = this.courses.find(c => c.courseId === selectedCourse.courseId);
          if (course) {
            course.status = '待添加';
          }
        });
        this.showActionMenu = false; // 隐藏菜单
        this.selectedCourses = []; // 清空选中课程

      } catch (error) {
        console.error('删除失败:', error);
        alert('删除失败，请稍后重试');
      }
    },
    async getCourseStatus(course) {
      const userId = 1; // 默认userId为1，需要更改！
      const courseId = course.courseId;
      try {
        const response = await fetch(`http://localhost:8080/student/getCourseStatus?userId=${userId}&courseId=${courseId}`);
        if (!response.ok) {
          throw new Error('获取课程状态失败');
        }
        const result = await response.json();
        // 假设后端返回1 表示已添加，0 表示未添加
        const statusValue = result.status !== undefined ? result.status : result;
        if (statusValue === 1) {
          return '已添加';
        } else if (statusValue === 0) {
          return '待添加';
        } else {
          return '未知状态';
        }
      } catch (error) {
        console.error('获取课程状态失败:', error);
        return '未知状态';
      }
    }
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
  display: flex;
  justify-content: space-between; /* 左右分布 */
  align-items: flex-start; /* 顶部对齐 */
  margin-bottom: 20px;
  position: relative;
}

.button-container {
  display: flex;
  flex-direction: column; /* 垂直排列按钮 */
  align-items: flex-end; /* 按钮靠右对齐 */
}

.search-container {
  position: absolute; /* 绝对定位 */
  bottom: 0; /* 距离底部为0 */
  left: 0; /* 距离左侧为0 */
  width: 50%; /* 宽度与父级相同 */
  box-sizing: border-box; /* 确保padding不会影响宽度 */
  padding-left: 10px; /* 根据需要添加内边距 */
}

.search-input {
  padding: 8px;
  width: calc(100% - 20px); /* 减去左右内边距 */
  border: 1px solid #ddd;
  border-radius: 4px;
}

.header-row h1 {
  font-size: 30px;
  font-weight: 600;
  color: #0d47a1;
  margin: 0;
}

.header-row .confirm-btn {
  padding: 10px 20px;
  background-color: #0d47a1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

/* 培养方案模态框 */
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

.button-group {
  display: flex;
  justify-content: flex-end; /* 靠右对齐 */
  margin-top: 20px;
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

.confirm-btn {
  padding: 10px 20px;
  background-color: #0d47a1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 20px;
}

.confirm-btn:hover {
  background-color: #1565c0;
}

/* 遮罩层 */
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

/* 遮罩层 */
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

/* 弹窗主体 */
.action-menu {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  text-align: center;
  z-index: 10000;
}

/* 按钮容器 - 水平排列 */
.action-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center;
  gap: 15px; /* 按钮之间的间距 */
}

.action-menu li {
  margin: 0;
}

/* 按钮样式 */
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

/* 添加按钮颜色 */
.action-menu button:nth-child(1) {
  background-color: #4caf50;
}

/* 删除按钮颜色 */
.action-menu button:nth-child(2) {
  background-color: #f44336;
}

/* 取消按钮颜色 */
.action-menu button:nth-child(3) {
  background-color: #9e9e9e;
}
</style>