<template>
  <div class="page-container">
    <div class="inner-container" id="studentSearchContainer">
      <h1>搜索特殊学生</h1>
      <div class="search-container">
        <input type="text" id="studentId" placeholder="学号" class="search-input" v-model="searchStudentId">
        <input type="text" id="studentName" placeholder="姓名" class="search-input" v-model="searchStudentName">
        <button class="search-btn" @click="searchStudents">查询</button>
      </div>
      <table id="studentTable">
        <thead>
        <tr>
          <th>学号</th>
          <th>姓名</th>
          <th>学院</th>
          <th>操作</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="student in students" :key="student.student_id">
          <td>{{ student.student_id }}</td>
          <td>{{ student.student_name }}</td>
          <td>{{ student.dept_name }}</td>
          <td>
            <button @click="selectStudent(student.student_id)">选择</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
    <div class="inner-container" id="courseSearchContainer" style="display: none;">
      <h1>搜索课程</h1>
      <div class="search-container">
        <input list="year-list" id="courseYear" placeholder="上课年份" class="search-input" v-model="searchCourseYear">
        <datalist id="year-list">
          <option value="2026"></option>
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
        <input type="text" id="courseName" placeholder="课程名称" class="search-input" v-model="searchCourseName">
        <input type="text" id="courseInstrutor" placeholder="任课教师" class="search-input" v-model="searchCourseInstructor">
        <button class="search-btn" @click="searchCourses">查询</button>
      </div>
      <table id="courseTable">
        <thead>
        <tr>
          <th>课程ID</th>
          <th>教学班ID</th>
          <th>课程名称</th>
          <th>任课教师</th>
          <th>课程学分</th>
          <th>上课时间</th>
          <th>上课地点</th>
          <th>课程剩余容量</th>
          <th>操作</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="course in courses" :key="course.courseId">
          <td>{{ course.courseId }}</td>
          <td>{{ course.sectionId }}</td>
          <td>{{ course.name }}</td>
          <td>{{ course.instructor }}</td>
          <td>{{ course.credit }}</td>
          <td>{{ course.time }}</td>
          <td>{{ course.place }}</td>
          <td>{{ course.capacity }}</td>
          <td>
            <button @click="selectCourse(course.sectionId)">选择</button>
          </td>
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
      searchStudentId: null,
      searchStudentName: null,
      students: [
        { student_id: '', student_name: '', dept_name: ''}
      ],
      selectedStudentId: null,

      searchCourseYear:null,
      searchCourseSemester: null,
      searchCourseName: null,
      searchCourseInstructor: null,
      courses: [
        { courseId: '', name: '', instructor: '', credit: '', time: '', place: '', sectionId: '', capacity: ''}
      ],
      selectedCourseId: null,
    };
  },
  methods: {
    async searchStudents() {
      if (!this.searchStudentId && !this.searchStudentName) {
        alert('请至少填写一个学生查询条件');
        return;
      }

      const params = new URLSearchParams();
      if (this.searchStudentId) params.append('studentId', this.searchStudentId);
      if (this.searchStudentName) params.append('studentName', this.searchStudentName);

      try {
        const response = await fetch(`http://localhost:8080/admin/HelpSelect/students?${params.toString()}`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (response.status === 404) {
          alert('未查询到相关学生，请检查输入信息是否正确');
        } else {
          const data = await response.json();
          this.students = data;
          alert(`查询成功！`);
        }
      } catch (error) {
        alert(`查询失败: ${error.message}`);
      }
    },
    selectStudent(studentId) {
      if (confirm('是否确认选择该学生？')) {
        if (!studentId) {
          alert('未选中学生');
          return;
        }
        this.selectedStudentId = studentId;
        document.getElementById('studentSearchContainer').style.display = 'none';
        document.getElementById('courseSearchContainer').style.display = 'block';
      }
    },
    async searchCourses() {
      if (!this.searchCourseYear) {
        alert('请填写选课年份！');
        return;
      }
      if (!this.searchCourseSemester && !this.searchCourseName && !this.searchCourseInstructor) {
        alert('请至少填写一个课程查询条件');
        return;
      }

      const params = new URLSearchParams();
      params.append('courseYear', this.searchCourseYear);
      if (this.searchCourseSemester) params.append('courseSemester', this.searchCourseSemester);
      if (this.searchCourseName) params.append('courseName', this.searchCourseName);
      if (this.searchCourseInstructor) params.append('courseInstructor', this.searchCourseInstructor);

      try {
        const response = await fetch(`http://localhost:8080/admin/HelpSelect/courses?${params.toString()}`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (response.status === 404) {
          alert('未查询到相关课程，请检查输入信息是否正确！');
        } else {
          const data = await response.json();
          this.courses = data;
          alert(`查询成功！`);
        }
      } catch (error) {
        alert(`查询失败: ${error.message}`);
      }
    },
    async selectCourse(sectionId) {
      if (confirm('是否确认选择该课程？')) {
        try {
          if (!sectionId){
            alert('未选中课程');
            return;
          }
          const response = await fetch('http://localhost:8080/admin/HelpSelect',{
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              studentId: this.selectedStudentId,
              sectionId: sectionId
            })
          });

          if (!response.ok) {
            const errorMessage = await response.text();
            alert(errorMessage);
            if (!confirm('是否继续选课')){
              document.getElementById('studentSearchContainer').style.display = 'block';
              document.getElementById('courseSearchContainer').style.display = 'none';
            }
          } else {
            alert('选课成功！');

            const params = new URLSearchParams();
            params.append('courseYear', this.searchCourseYear);
            if (this.searchCourseSemester) params.append('courseSemester', this.searchCourseSemester);
            if (this.searchCourseName) params.append('courseName', this.searchCourseName);
            if (this.searchCourseInstructor) params.append('courseInstructor', this.searchCourseInstructor);

            const response = await fetch(`http://localhost:8080/admin/HelpSelect/courses?${params.toString()}`, {
              method: 'GET',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json'
              }
            });
            const data = await response.json();
            this.courses = data;

            if (!confirm('是否继续选课')){
              document.getElementById('studentSearchContainer').style.display = 'block';
              document.getElementById('courseSearchContainer').style.display = 'none';
            }
          }
        } catch (error) {
          alert('选课失败！');
        }
      }
    }
  }
};
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
</style>