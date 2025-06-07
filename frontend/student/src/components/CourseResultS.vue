<!-- lmt -->
<template>
  <div class="page-container">
    <div class="inner-container">
      <h1>选课结果查询</h1>
      <div class="search-container">
        <input list="year-list" id="courseYear" placeholder="上课年份" class="search-input" v-model="searchCourseYear">
        <datalist id="year-list">
          <option value="2025"></option>
          <option value="2024"></option>
          <option value="2023"></option>
          <option value="2022"></option>
          <option value="2021"></option>
        </datalist>
        <input list="semester-list" id="courseSemester" placeholder="上课学期" class="search-input" v-model="searchCourseSemester">
        <datalist id="semester-list">
          <option value="春"></option>
          <option value="夏"></option>
          <option value="秋"></option>
          <option value="冬"></option>
        </datalist>
        <button @click="searchCourse" class="search-btn">查询</button>
      </div>
      <table id="courseTable">
        <thead>
        <tr>
          <th>课程id</th>
          <th>课程名称</th>
          <th>年份</th>
          <th>学期</th>
          <th>上课时间</th>
          <th>上课地点</th>
          <th>任课老师</th>
          <th>课程学分</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="course in courses" :key="course.courseId">
          <td>{{ course.courseId }}</td>
          <td>{{ course.name }}</td>
          <td>{{ course.year}}</td>
          <td>{{ course.semester}}</td>
          <td>{{ course.time}}</td>
          <td>{{ course.place}}</td>
          <td>{{ course.instructor}}</td>
          <td>{{ course.credit }}</td>
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
      searchCourseYear: null,
      searchCourseSemester: null,
      courses:[
        { courseId: '', name: '', year: '', semester: '', time: '', place: '', instructor: '', credit: ''}
      ]
    };
  },
  computed: {
    // 从路由参数中获取 userId
    userId() {
      return this.$route.params.userId;
    }
  },
  methods: {
    // 中文轉英文
    getEnglishSemester(chineseSemester) {
      const map = {
        '春': 'Spring',
        '夏': 'Summer',
        '秋': 'Fall',
        '冬': 'Winter'
      };
      return map[chineseSemester] || chineseSemester;
    },
    async searchCourse() {
      // 验证 userId 是否存在（由路由保证必填）
      if (!this.userId) {
        alert('用户信息异常，请重新登录');
        return;
      }

      const params = new URLSearchParams();
      if (this.searchCourseYear) params.append('courseYear', this.searchCourseYear);
      if (this.searchCourseSemester) params.append('courseSemester', this.getEnglishSemester(this.searchCourseSemester));

      try {
        const response = await fetch(`http://localhost:8083/student/${this.userId}/CourseResultS?${params.toString()}`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok){
          const errorMessage = await response.text();
          alert(errorMessage);
        } else {
          const data = await response.json();
          this.courses = data;
          alert(`找到${data.length}门已选上的课程`);
        }
      } catch (error) {
        alert(`查询失败：${error.message}`);
      }
    }
  },
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