<!-- szx -->
<template>
  <div class="page-container">
    <div class="inner-container">
      <h1>查询课程信息</h1>
      <div class="search-container">
        <input type="text" id="courseId" placeholder="请输入课程id" class="search-input">
        <input type="text" id="courseName" placeholder="请输入课程名称" class="search-input">
        <input type="text" id="college" placeholder="请输入开课学院" class="search-input">
        <button @click="searchCourses" class="search-btn">查询</button>
      </div>
      <div id="searchResult"></div>
      <table id="courseTable">
        <thead>
        <tr>
          <th>课程ID</th>
          <th>课程名称</th>
          <th>开课学院</th>
          <th>学分</th>
          <th>课程信息</th>
          <th>教学班规模</th>
        </tr>
        </thead>
        <tbody id="courseTableBody">
        <tr v-for="course in allCourses" :key="course.courseId">
          <td>{{ course.courseId}}</td>
          <td>{{ course.title }}</td>
          <td>{{ course.deptName }}</td>
          <td>{{ course.credit }}</td>
          <td>{{ course.courseInfo }}</td>
          <td>{{ course.capacity }}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      allCourses: [] // 存放所有课程数据
    };
  },
  mounted() {
    this.searchCourses();
  },
  methods: {
    async searchCourses() {
      // 获取筛选条件
      const courseId = document.getElementById('courseId').value;
      const courseName = document.getElementById('courseName').value;
      const college = document.getElementById('college').value;

      const searchData = {
        courseId,
        courseName,
        college
      };

      try {
        // 若未加载过数据，则请求一次后端
        if (this.allCourses.length === 0) {
          this.allCourses = await this.queryDatabase();
        }
        // 本地筛选
        const results = this.compute(this.allCourses, searchData);
        this.allCourses=results;
      } catch (error) {
        alert('查询失败：' + error.message);
      }
    },
    async queryDatabase() {
      // 向后端请求所有课程信息
      const response = await fetch('http://localhost:8083/student/getAllCourses'); // 路径请与后端保持一致
      if (!response.ok) throw new Error("后端接口错误");
      const data = await response.json();
      return data;
    },
    // 筛选功能独立为 compute
    compute(courses, searchData) {
      return courses.filter(course => {
        const matchId = !searchData.courseId || (course.courseId && String(course.courseId).includes(searchData.courseId));
        const matchName = !searchData.courseName || (course.title && course.title.includes(searchData.courseName));
        // 注意course没有时间、学院、教师字段时适当处理
        const matchCollege = !searchData.college || (course.deptName && course.deptName.includes(searchData.college));
        return matchId && matchName && matchCollege ;
      });
    }
  }
}
</script>
<style scoped>

/* 页面内容容器 */
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

/* 表格样式 */
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  background-color: white;
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

/* 搜索框和按钮样式 */
.search-container {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-right: 10px;
}

.search-btn {
  padding: 10px 20px;
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

</style>