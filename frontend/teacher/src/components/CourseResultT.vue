<template>
  <div class="page-container">
    <div class="inner-container">
      <h1>选课结果</h1>
      <div class="search-container">
        <input list="year-list" placeholder="上课年份" class="search-input" v-model="currentYear">
        <datalist id="year-list">
          <option value="2026"></option>
          <option value="2025"></option>
          <option value="2024"></option>
          <option value="2023"></option>
          <option value="2022"></option>
          <option value="2021"></option>
        </datalist>
        <input list="semester-list" placeholder="上课学期" class="search-input" v-model="currentSemester">
        <datalist id="semester-list">
          <option value="春夏"></option>
          <option value="秋冬"></option>
          <option value="春"></option>
          <option value="夏"></option>
          <option value="秋"></option>
          <option value="冬"></option>
          <option value="短"></option>
        </datalist>
        <input type="text" v-model="searchCourseName" placeholder="请输入课程名称" class="search-input">
        <button @click="searchCourse" class="search-btn">查询</button>
      </div>

      <div id="searchResult" class="search-result-display">{{ searchResult }}</div>
      <table id="courseTable">
        <thead>
        <tr>
          <th>课程名称</th>
          <th>年份</th>
          <th>学期</th>
          <th>选课学生数量</th>
          <th>上课时间</th>
          <th>上课地点</th>
        </tr>
        </thead>
        <tbody>
        <tr v-if="courses.length === 0 && !initialLoad">
          <td colspan="6" style="text-align: center; padding: 20px; color: #555;">
            您在该时间段没有对应课程
          </td>
        </tr>
        <tr v-for="(course, index) in courses" :key="index">
          <td>{{ course.name }}</td>
          <td>{{ course.year }}</td>
          <td>{{ formatSemester(course.semester) }}</td>
          <td>{{ course.takes }}</td>
          <td>{{ formatTime(course.time) }}</td>
          <td>{{ course.place }}</td>
        </tr>
        </tbody>
      </table>
      <button class="print-btn" @click="printTimetable">打印选课结果</button>
    </div>
  </div>
</template>

<script>
// 如果不使用axios，则不需要导入
export default {
  data() {

    return {
      searchResult: '',
      searchCourseName: '',
      courses: [],
      isLoading: false,
      isLoadingPrint: false,
      initialLoad: true,
      // 确保这些值是动态获取或正确设置的
      teacherId: this.$route.params.userId || '', // 示例: 教师ID
      currentYear: '', // 示例: 当前年份
      currentSemester: '', // 示例: 当前学期
      searchedYear: '',
      searchedSemester: '',
      // 如果您决定保留 searchResult 用于显示特定信息，请在这里定义
      // searchResult: '',
    };
  },
  computed: {
    // 推荐用 computed 保证响应式
    teacherIdFromRoute() {
      return this.$route.params.userId;
    }
  },
  watch: {
    teacherIdFromRoute(newId) {
      this.teacherId = newId;
    }
  },
  created() {
    this.fetchCourseResults(); // 初始加载课程列表
  },
  methods: {
    getBackendSemester(frontendSemester) {
      const mapping = {
        '春夏': 'SpringSummer', // 假设数据库中用 'SpringSummer' 代表春夏两学期
        '秋冬': 'FallWinter',   // 假设数据库中用 'FallWinter' 代表秋冬两学期
        '春': 'Spring',
        '夏': 'Summer',
        '秋': 'Fall',
        '冬': 'Winter',
        '短': 'Short', // 假设的短期学期英文表示
        // 添加其他必要的映射
      };
      return mapping[frontendSemester] || frontendSemester; // 如果没有映射，则返回原值
    },
    formatSemester(semester) {
      // 将学期转换为更易读的格式
      // 例："Spring" => "春"
      const mapping = {
        'Spring': '春',
        'Summer': '夏',
        'Fall': '秋',
        'Winter': '冬',
        'SpringSummer': '春夏',
        'FallWinter': '秋冬',
        'Short': '短', // 假设的短期学期
      };
      return mapping[semester] || semester; // 如果没有映射，则返回原值
    },
    formatTime(timeStr) {
      // 匹配并去掉秒，只保留小时和分钟
      // 例："周一 08:00:00-09:35:00" => "周一 08:00-09:35"
      if (!timeStr) return '';
      return timeStr.replace(/(\d{2}:\d{2}):\d{2}/g, '$1');
    },
    searchCourse() {
      this.fetchCourseResults();
    },
    async fetchCourseResults() {
      this.$router.push({ name: 'CourseResultT', params: { userId: this.teacherId } });
      this.isLoading = true;
      this.initialLoad = false;
      this.courses = []; // 清空旧数据

      const yearToSearch = this.currentYear;
      const semesterToSearch = this.currentSemester;
      const courseNameToSearch = this.searchCourseName;

      try {
        const backendSearchSemester = this.getBackendSemester(this.currentSemester);
        const queryParams = new URLSearchParams({
          courseName: this.searchCourseName || '',
          courseYear: this.currentYear,
          courseSemester: backendSearchSemester, // 使用转换后的学期值
        });

        const response = await fetch(`http://localhost:8080/teacher/${this.teacherId}/CourseResultT?${queryParams}`);

        if (!response.ok) {
          // HTTP 状态码不在 200-299 范围
          let errorDetail = `请求失败，状态码: ${response.status} ${response.statusText}`;
          try {
            // 尝试读取响应体作为文本，因为错误页面通常是HTML或文本
            const errorText = await response.text();
            // 截取一部分HTML错误信息，避免控制台输出过长
            const briefErrorText = errorText.length > 300 ? errorText.substring(0, 300) + "..." : errorText;
            console.error('服务器错误响应体:', briefErrorText); // 在控制台打印详细错误，帮助调试
            if (errorText.toLowerCase().includes("<!doctype html")) {
              errorDetail += " (服务器返回了HTML页面，可能是后端错误或API路径无效)";
            } else {
              errorDetail += ` - ${briefErrorText}`;
            }
          } catch (e) {
            // 读取响应体失败
          }
          throw new Error(errorDetail);
        }

        // 只有当 response.ok 为 true 时，才尝试解析JSON
        this.courses = await response.json();
        this.searchedYear = yearToSearch;
        this.searchedSemester = semesterToSearch;
        // 2. 更新提示文字
        this.searchResult = `当前查询：${this.searchedYear}学年 ${this.searchedSemester}学期`;
        // 3. 清空课程名称输入框
        this.searchCourseName = courseNameToSearch;
        this.currentYear = '';
        this.currentSemester = '';

      } catch (error) {
        console.error('获取课程结果列表时发生错误:', error.message);
        // 可以在这里设置一个用户可见的错误提示，例如:
        // this.userMessage = error.message; // 假设有一个 userMessage data属性
        this.courses = []; // 清空列表以表示加载失败
      } finally {
        this.isLoading = false;
      }
    },

    async printTimetable() {
      if (!this.searchedYear || !this.searchedSemester) {
        alert("请指定学年和学期，再打印课表。");
        return;
      }
      this.$router.push({ name: 'CourseResultT', params: { userId: this.teacherId } });
      this.isLoadingPrint = true;
      try {
        const backendSearchSemesterForTimetable = this.getBackendSemester(this.searchedSemester);

        const queryParams = new URLSearchParams({
          year: this.searchedYear,
          semester: backendSearchSemesterForTimetable,
        });
        const response = await fetch(`http://localhost:8080/teacher/${this.teacherId}/timetable?${queryParams}`);

        // ... 后续逻辑保持不变 ...

        if (!response.ok) {
          let errorDetail = `请求课表数据失败，状态码: ${response.status} ${response.statusText}`;
          try {
            const errorText = await response.text();
            const briefErrorText = errorText.length > 300 ? errorText.substring(0, 300) + "..." : errorText;
            console.error('服务器错误响应体 (课表):', briefErrorText);
            if (errorText.toLowerCase().includes("<!doctype html")) {
              errorDetail += " (服务器返回了HTML页面)";
            } else {
              errorDetail += ` - ${briefErrorText}`;
            }
          } catch (e) {/*ignore*/ }
          throw new Error(errorDetail);
        }

        const timetableApiResponseData = await response.json();

        if (timetableApiResponseData.errorMessage) {
          alert(`准备课表数据时出错: ${timetableApiResponseData.errorMessage}`);
          this.isLoadingPrint = false;
          return;
        }
        const timetableData = timetableApiResponseData.timetable;

        // ... （后续生成HTML和打印的逻辑不变） ...
        const daysOrder = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"];
        const periods = [
          "08:00-08:50",
          "09:00-09:50",
          "10:00-10:50",
          "11:00-11:50",
          "13:00-13:50",
          "14:00-14:50",
          "15:00-15:50",
          "16:00-16:50"
        ];
        const periodMap = {
          "第08:00-08:50节": "08:00-08:50",
          "第09:00-09:50节": "09:00-09:50", // 假设这两节课都属于 "第1-2节"

          "第10:00-10:50节": "10:00-10:50",
          "第11:00-11:50节": "11:00-11:50",

          "第13:00-13:50节": "13:00-13:50", // 后端返回这个
          "第14:00-14:50节": "14:00-14:50", // 后端返回这个

          "第15:00-15:50节": "15:00-15:50", // 后端返回这个
          "第16:00-16:50节": "16:00-16:50",
        };

        let timetableHtml = `
          <h2>${this.searchedYear}学年 ${this.searchedSemester}学期 教师课表</h2>
          <table border="1" style="border-collapse:collapse; width:100%; font-size:12px; text-align:center;">
            <thead>
              <tr>
                <th style="padding:5px;">时间/星期</th>`;
        daysOrder.forEach(day => {
          timetableHtml += `<th style="padding:5px;">${day}</th>`;
        });
        timetableHtml += `</tr></thead><tbody>`;
        periods.forEach(period => {
          timetableHtml += `<tr><td style="padding:5px; white-space: nowrap;">${period}</td>`;
          daysOrder.forEach(day => {
            let cellContent = "";
            if (timetableData && timetableData[day]) {
              const entriesForDay = timetableData[day];
              const entry = entriesForDay.find(e => periodMap[e.period] === period);
              if (entry) {
                // 修改 cellContent 来包含选课人数
                cellContent = `${entry.courseName}<br/>@${entry.location}<br/>人数: ${entry.studentCount}`;
              }
            }
            timetableHtml += `<td style="padding:5px; min-height: 60px; vertical-align: top;">${cellContent}</td>`; // 可能需要调整 min-height
          });
          timetableHtml += `</tr>`;
        });
        timetableHtml += `</tbody></table>
          <p style="font-size:10px; text-align:center; margin-top:10px;">打印时间: ${new Date().toLocaleString()}</p>`;

        const printIframe = document.createElement('iframe');
        printIframe.style.display = 'none';
        document.body.appendChild(printIframe);
        const iframeDoc = printIframe.contentDocument || printIframe.contentWindow.document;
        iframeDoc.open();
        iframeDoc.write(`<html><head><title>教师课表</title><style>body { font-family: Arial, sans-serif; } table { width: 100%; border-collapse: collapse; font-size: 12px; } th, td { border: 1px solid #ccc; padding: 5px; text-align: center; vertical-align: top; } th { background-color: #f2f2f2; } h2 { text-align: center; }</style></head><body>${timetableHtml}</body></html>`);
        iframeDoc.close();
        printIframe.onload = function () {
          try {
            printIframe.contentWindow.focus();
            printIframe.contentWindow.print();
          } catch (e) {
            console.error("打印出错:", e);
            alert("打印功能可能被浏览器阻止或发生错误。");
          } finally {
            document.body.removeChild(printIframe);
          }
        };
      } catch (error) {
        console.error('准备打印课表时发生错误:', error.message);
        alert(`准备打印数据失败: ${error.message}`);
      } finally {
        this.isLoadingPrint = false;
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

  .print-btn {
  padding: 10px 20px;
  background-color: #0d47a1;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 20px;
  margin-top: 20px;
}

  .print-btn:hover {
    background-color: #1565c0;
}

  /* 搜索框和按钮样式 */
  .search-container {
  display: flex;
  align-items: center;
  margin-top: 20px;
  margin-bottom: 10px; /* 修改了下边距 */
}

  /* 新增的样式 */
  .search-result-display {
  color: #555;
  font-size: 14px;
  margin-bottom: 20px;
  height: 1em; /* 保证元素占位，防止页面内容跳动 */
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