<!-- lmt -->
<template>
  <div class="page-container">
    <div class="inner-container">
      <h1>我的课表</h1>
      <div class="search-container">
        <!-- 年份和学期选择框 -->
        <input
            list="year-list"
            id="courseYear"
            placeholder="上课年份"
            class="search-input"
            v-model.number="searchCourseYear"
        >
        <datalist id="year-list">
          <option value="2026"></option>
          <option value="2025"></option>
          <option value="2024"></option>
          <option value="2023"></option>
        </datalist>
        <input
            list="semester-list"
            id="courseSemester"
            placeholder="上课学期"
            class="search-input"
            v-model="searchCourseSemester"
        >
        <datalist id="semester-list">
          <option value="春"></option>
          <option value="夏"></option>
          <option value="秋"></option>
          <option value="冬"></option>
        </datalist>
        <div class="button-group">
          <button @click="searchCoursetable" class="search-btn">查询课表</button>
          <button @click="printPage" class="print-btn">打印课表</button>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>加载课表中...</p>
      </div>

      <!-- 错误提示 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- 课表展示区域 -->
      <div v-if="tableData.length > 0" class="timetable-container" ref="timetable">
        <div class="timetable-header">
          <h2>{{ searchCourseYear }}年{{ searchCourseSemester }}季学期课表</h2>
        </div>
        <div class="table-wrapper"> <!-- 新增表格包装器 -->
          <table class="timetable-table">
            <thead>
            <tr>
              <th>时间段</th>
              <th>周一</th>
              <th>周二</th>
              <th>周三</th>
              <th>周四</th>
              <th>周五</th>
            </tr>
            </thead>
            <tbody>
            <!-- 遍历所有时间段（1-8节，每节对应一行） -->
            <tr v-for="(period, periodIndex) in periodList" :key="periodIndex">
              <td class="time-cell">{{ period.time }}</td>
              <!-- 遍历每一天 -->
              <td v-for="day in ['周一', '周二', '周三', '周四', '周五']" :key="day">
                <!-- 查找当前时间段和星期对应的课程 -->
                <div
                    v-if="getCourseByDayAndPeriod(day, period.time)"
                    class="course-cell"
                    @click="showCourseDetails(getCourseByDayAndPeriod(day, period.time))"
                >
                  <div class="course-name ellipsis">
                    {{ getCourseByDayAndPeriod(day, period.time).courseName }}
                  </div>
                  <div class="course-location ellipsis">
                    {{ getCourseByDayAndPeriod(day, period.time).location }}
                  </div>
                </div>
                <div v-else class="empty-cell">-</div>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 无数据提示 -->
      <div v-if="noDataMessage" class="no-data-message">
        {{ noDataMessage }}
      </div>
    </div>

    <!-- 课程详情弹窗 -->
    <div v-if="showPopup" class="popup-container">
      <div class="popup-content">
        <h3>课程详情</h3>
        <p><strong>课程名称：</strong> {{ currentCourse.courseName }}</p>
        <p><strong>上课地点：</strong> {{ currentCourse.location }}</p>
        <p><strong>时间段：</strong> {{ currentCourse.period }}</p>
        <p><strong>星期：</strong> {{ currentCourse.day }}</p>
        <button @click="closePopup">关闭</button>
      </div>
    </div>

    <!-- 打印专用容器 -->
    <div id="print-container" class="print-container" style="display: none;"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchCourseYear: null, // 改为数字类型
      searchCourseSemester: '', // 默认值
      tableData: [],
      loading: false,
      errorMessage: '',
      noDataMessage: '',
      showPopup: false,
      currentCourse: {},
      // 定义时间段映射（与后端逻辑一致）
      periodConfig: [
        { time: '8:00-8:50', slot: 1 },
        { time: '9:00-9:50', slot: 2 },
        { time: '10:00-10:50', slot: 3 },
        { time: '11:00-11:50', slot: 4 },
        { time: '13:00-13:50', slot: 5 },
        { time: '14:00-14:50', slot: 6 },
        { time: '15:00-15:50', slot: 7 },
        { time: '16:00-16:50', slot: 8 },
      ]
    };
  },
  computed: {
    periodList() {
      return this.periodConfig; // 时间段列表（用于渲染表格行）
    },
    userId(){
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
    async searchCoursetable() {
      // 验证输入
      if (!this.searchCourseYear || isNaN(this.searchCourseYear)) {
        this.errorMessage = '请选择有效年份';
        return;
      }
      if (!this.searchCourseSemester) {
        this.errorMessage = '请选择学期';
        return;
      }

      this.loading = true;
      this.errorMessage = '';
      this.noDataMessage = '';
      this.tableData = [];

      // 验证 userId 是否存在（由路由保证必填）
      if (!this.userId) {
        alert('用户信息异常，请重新登录');
        return;
      }

      const params = new URLSearchParams();
      if (this.searchCourseYear) params.append('courseYear', this.searchCourseYear);
      if (this.searchCourseSemester) params.append('courseSemester', this.getEnglishSemester(this.searchCourseSemester));

      try {
        // 发送请求
        const response = await fetch(`http://localhost:8083/student/${this.userId}/CourseTableS?${params.toString()}`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) throw new Error('请求失败');
        const data = await response.json();
        console.log('后端返回数据:', data); // 新增调试日志

        // 处理错误信息
        if (data.errorMessage) {
          this.errorMessage = data.errorMessage;
          return;
        }
        if (data.timetable && Object.keys(data.timetable).length === 0) {
          this.noDataMessage = '暂无选课记录';
          return;
        }

        // 转换数据格式：将后端的{timetable: {周一: [...], 周二: [...], ...}}转为前端所需结构
        this.tableData = this.transformTimetable(data.timetable);
        console.log('转换后tableData:', this.tableData); // 新增调试日志
      } catch (error) {
        this.errorMessage = '获取课表失败，请重试';
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    transformTimetable(timetableData) {
      // 初始化所有时间段和星期的课程为null，并添加period字段
      const transformed = this.periodConfig.reduce((acc, period) => {
        acc[period.time] = {
          time: period.time,
          slot: period.slot,
          period: period.time, // 添加时间段字段
          slots: {
            周一: null,
            周二: null,
            周三: null,
            周四: null,
            周五: null
          }
        };
        return acc;
      }, {});

      // 填充课程数据，并添加星期信息
      Object.entries(timetableData).forEach(([day, courses]) => {
        courses.forEach(course => {
          const periodTime = course.period; // 直接使用后端返回的时间段字符串
          console.log('课程时间段:', periodTime); // 新增调试日志
          if (transformed[periodTime]) { // 检查时间段是否在periodConfig中
            transformed[periodTime].slots[day] = {
              ...course,
              day: day // 添加星期信息
            };
          } else {
            console.warn(`未定义的时间段: ${periodTime}，请检查后端数据或前端periodConfig`);
          }
        });
      });

      // 转换为数组并按时间段排序
      return Object.values(transformed).sort((a, b) => a.slot - b.slot);
    },

    // 辅助函数：根据星期和时间段获取课程
    getCourseByDayAndPeriod(day, periodTime) {
      return this.tableData.find(period => period.time === periodTime)?.slots[day];
    },

    // 打印功能 - 只打印课表信息
    printPage() {
      // 检查是否有课表数据
      if (!this.tableData || this.tableData.length === 0) {
        this.errorMessage = '没有可打印的课表数据';
        return;
      }

      // 创建打印专用容器
      const printContainer = document.getElementById('print-container');
      printContainer.innerHTML = '';

      // 复制课表内容到打印容器
      const timetableCopy = this.$refs.timetable.cloneNode(true);

      // 创建打印样式
      const printStyle = document.createElement('style');
      printStyle.textContent = `
        @media print {
          .table-wrapper { overflow-x: visible !important; }
          .timetable-table { table-layout: auto !important; width: auto !important; min-width: auto !important; }
          .timetable-table th,
          .timetable-table td {
            width: auto !important; /* 取消固定列宽 */
            height: auto !important; /* 取消固定行高 */
            line-height: normal;
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: unset !important;
            word-wrap: break-word; /* 允许单词内换行 */
          }
          .ellipsis { display: block !important; height: auto !important; }
        }
        @media print {
          body * {
            visibility: hidden;
          }
          #print-container, #print-container * {
            visibility: visible;
          }
          #print-container {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            padding: 20px;
            box-sizing: border-box;
          }
          .timetable-table {
            width: 100%;
            border-collapse: collapse;
          }
          .timetable-table th,
          .timetable-table td {
            border: 1px solid #000;
            padding: 8px;
            text-align: center;
          }
          .course-cell {
            background-color: #f0f0f0 !important;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
            word-wrap: break-word; /* 打印时允许自动换行 */
          }
          .timetable-table tbody tr {
            page-break-inside: avoid;
          }
          .ellipsis {
            white-space: normal !important; /* 打印时取消省略号，允许换行 */
            overflow: visible !important;
            text-overflow: unset !important;
          }
        }
      `;

      // 添加样式到打印容器
      timetableCopy.appendChild(printStyle);

      // 添加到打印容器
      printContainer.appendChild(timetableCopy);

      // 显示打印容器
      printContainer.style.display = 'block';

      // 执行打印
      window.print();

      // 打印完成后隐藏打印容器
      setTimeout(() => {
        printContainer.style.display = 'none';
      }, 100);
    },

    // 弹窗相关方法
    showCourseDetails(course) {
      this.currentCourse = course;
      this.showPopup = true;
    },
    closePopup() {
      this.showPopup = false;
    }
  }
};
</script>

<style scoped>
/* 新增表格包装器样式 */
.table-wrapper {
  overflow-x: auto; /* 允许水平滚动 */
  width: 100%;
}

/* 固定列宽和行高 */
.timetable-table {
  table-layout: fixed; /* 关键属性：固定表格布局 */
  width: 100%;
  min-width: 900px; /* 防止表格过窄 */
}

.timetable-table th,
.timetable-table td {
  width: 150px; /* 固定列宽 */
  height: 100px; /* 固定行高 */
  line-height: 1.4; /* 固定行间距 */
  overflow: hidden;
  padding: 10px;
  border: 1px solid #e0e0e0;
  text-align: center;
  vertical-align: top;
}

.ellipsis {
  white-space: nowrap; /* 禁止换行 */
  overflow: hidden;
  text-overflow: ellipsis; /* 显示省略号 */
  max-width: 100%;
  display: block;
  height: 1.4em; /* 根据行高设置，确保单行显示 */
}

/* 弹窗样式 */
.popup-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
}

.popup-content button {
  margin-top: 15px;
  padding: 8px 20px;
  background-color: #0d47a1;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

</style>

<style scoped>
/* 新增表格包装器样式 */
.table-wrapper {
  overflow-x: auto; /* 允许水平滚动 */
  width: 100%;
}

/* 固定列宽和行高 */
.timetable-table {
  table-layout: fixed; /* 关键属性：固定表格布局 */
  width: 100%;
  min-width: 900px; /* 防止表格过窄 */
}

.timetable-table th,
.timetable-table td {
  width: 150px; /* 固定列宽 */
  height: 100px; /* 固定行高 */
  line-height: 1.4; /* 固定行间距 */
  overflow: hidden;
  padding: 10px;
  border: 1px solid #e0e0e0;
  text-align: center;
  vertical-align: top;
}

.ellipsis {
  white-space: nowrap; /* 禁止换行 */
  overflow: hidden;
  text-overflow: ellipsis; /* 显示省略号 */
  max-width: 100%;
  display: block;
  height: 1.4em; /* 根据行高设置，确保单行显示 */
}

/* 弹窗样式 */
.popup-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
}

.popup-content button {
  margin-top: 15px;
  padding: 8px 20px;
  background-color: #0d47a1;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
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
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.inner-container h1 {
  font-size: 30px;
  font-weight: 600;
  color: #0d47a1;
  margin: 0 0 20px 0;
  text-align: center;
}

/* 表格样式 */
.timetable-container {
  margin-top: 30px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.timetable-header {
  text-align: center;
  margin-bottom: 20px;
}

.timetable-header h2 {
  color: #0d47a1;
  font-size: 22px;
  margin: 0;
}

.timetable-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.timetable-table th {
  background-color: #0d47a1;
  color: white;
  font-weight: bold;
  padding: 12px 8px;
  text-align: center;
}

.timetable-table td {
  padding: 10px;
  border: 1px solid #e0e0e0;
  text-align: center;
  height: 80px;
  vertical-align: top;
}

.time-cell {
  background-color: #e3f2fd;
  font-weight: bold;
  color: #0d47a1;
}

.course-cell {
  background-color: #e8f5e9;
  border-radius: 4px;
  padding: 8px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.course-name {
  font-weight: bold;
  color: #2e7d32;
  margin-bottom: 5px;
}

.course-location {
  font-size: 13px;
  color: #388e3c;
}

.empty-cell {
  color: #bdbdbd;
  font-style: italic;
}

/* 搜索区域样式 */
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

.search-input:focus {
  border-color: #0d47a1;
  outline: none;
  box-shadow: 0 0 0 2px rgba(13, 71, 161, 0.1);
}

.search-btn, .print-btn {
  padding: 12px 20px;
  background-color: #0d47a1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  white-space: nowrap;
}

.search-btn:hover, .print-btn:hover {
  background-color: #1565c0;
}

.print-btn {
  background-color: #2e7d32;
}

.print-btn:hover {
  background-color: #388e3c;
}

.button-group {
  display: flex;
  gap: 20px; /* 为按钮之间添加更大的间距 */
}

/* 加载动画 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  margin-top: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #0d47a1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 消息提示 */
.error-message, .no-data-message {
  padding: 15px;
  margin-top: 20px;
  border-radius: 6px;
  text-align: center;
  font-size: 16px;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  border: 1px solid #ffcdd2;
}

.no-data-message {
  background-color: #e3f2fd;
  color: #0d47a1;
  border: 1px solid #bbdefb;
}

/* 新增固定列宽和省略号样式 */
.timetable-table th,
.timetable-table td {
  width: 150px; /* 固定列宽 */
  height: 100px; /* 固定行高 */
  line-height: 1.4; /* 固定行间距 */
  overflow: hidden;
  position: relative;
}

.ellipsis {
  white-space: nowrap; /* 禁止换行 */
  overflow: hidden;
  text-overflow: ellipsis; /* 显示省略号 */
  max-width: 100%;
  display: block;
  height: 1.4em; /* 根据行高设置，确保单行显示 */
}

/* 弹窗样式 */
.popup-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
}

.popup-content button {
  margin-top: 15px;
  padding: 8px 20px;
  background-color: #0d47a1;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>