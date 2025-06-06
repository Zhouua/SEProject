<template>
  <div class="page-container">
    <div class="inner-container">
      <h1>设置选课时间</h1>
      <div class="time-setting-container">
        <h2>初选时间设置</h2>
        <label for="primaryStart">初选开始时间：</label>
        <input type="datetime-local" id="primaryStart" class="time-input" v-model="primaryStart">
        <div style="height: 20px;"></div> <!-- 这里添加了一个20px高的空隙 -->
        <label for="primaryEnd">初选结束时间：</label>
        <input type="datetime-local" id="primaryEnd" class="time-input" v-model="primaryEnd">
      </div>
      <div class="time-setting-container">
        <h2>补选时间设置</h2>
        <label for="supplementaryStart">补选开始时间：</label>
        <input type="datetime-local" id="supplementaryStart" class="time-input" v-model="supplementaryStart">
        <div style="height: 20px;"></div> <!-- 这里添加了一个20px高的空隙 -->
        <label for="supplementaryEnd">补选结束时间：</label>
        <input type="datetime-local" id="supplementaryEnd" class="time-input" v-model="supplementaryEnd">
      </div>
      <button @click="saveSettings" class="save-btn">保存设置</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      primaryStart: '',
      primaryEnd: '',
      supplementaryStart: '',
      supplementaryEnd: ''
    };
  },
  methods: {
    async saveSettings() {
      if ((!this.primaryStart || !this.primaryEnd) &&
          (!this.supplementaryStart || !this.supplementaryEnd)) {
        alert('请填写完整的时间信息');
        return;
      }
      const response = await fetch('http://localhost:8080/admin/SelectionTime',{
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          primaryStart: this.primaryStart,
          primaryEnd: this.primaryEnd,
          supplementaryStart: this.supplementaryStart,
          supplementaryEnd: this.supplementaryEnd
        })
      });

      if (!response.ok) {
        const errorMessage = await response.text();
        alert(errorMessage);
      } else {
        const successMessage = await response.text();
        alert(successMessage);
      }
      this.primaryStart = this.primaryEnd = this.supplementaryStart = this.supplementaryEnd = "";
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

.time-setting-container {
  margin-bottom: 20px;
}

.time-setting-container h2 {
  font-size: 20px;
  margin-bottom: 10px;
}

.time-setting-container label {
  display: inline-block;
  width: 150px;
  margin-bottom: 10px;
}

.time-input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 10px;
}

.save-btn {
  padding: 10px 20px;
  background-color: #0d47a1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-btn:hover {
  background-color: #1565c0;
}
</style>