<template>
  <div class="arbitrage-analysis">
    <div class="header">
      <h2>{{ t('arbitrage.title') }}</h2>
      <div class="controls">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="To"
          start-placeholder="Start date"
          end-placeholder="End date"
          :default-value="[new Date('2025-09-01'), new Date('2025-09-30')]"
          @change="fetchData"
        />
      </div>
    </div>

    <div class="stats-cards">
      <div class="card">
        <h3>Total Opportunities</h3>
        <div class="value">{{ opportunities.length }}</div>
      </div>
      <div class="card">
        <h3>Total Potential Profit</h3>
        <div class="value">${{ totalProfit.toFixed(2) }}</div>
      </div>
      <div class="card">
        <h3>Avg. Profit / Trade</h3>
        <div class="value">${{ avgProfit.toFixed(2) }}</div>
      </div>
    </div>

    <div class="content-grid">
      <div class="chart-section">
        <div ref="chartRef" style="width: 100%; height: 400px;"></div>
      </div>
      
      <div class="table-section">
        <el-table :data="opportunities" style="width: 100%" height="400">
          <el-table-column prop="timestamp" label="Time" width="180">
            <template #default="scope">
              {{ new Date(scope.row.timestamp).toLocaleString() }}
            </template>
          </el-table-column>
          <el-table-column prop="path" label="Path" width="180" />
          <el-table-column prop="amount" label="Amount (ETH)" width="120" />
          <el-table-column prop="profit" label="Profit (USDT)" sortable>
            <template #default="scope">
              <span class="profit-text">+{{ scope.row.profit }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts'
import { api } from '@/api'

const { t } = useI18n()
const chartRef = ref(null)
let chart = null
const dateRange = ref([new Date('2025-09-01'), new Date('2025-09-30')])
const opportunities = ref([])

const totalProfit = computed(() => opportunities.value.reduce((sum, item) => sum + item.profit, 0))
const avgProfit = computed(() => opportunities.value.length ? totalProfit.value / opportunities.value.length : 0)

const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    window.addEventListener('resize', () => chart.resize())
  }
}

const fetchData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2) return
  
  const [start, end] = dateRange.value
  opportunities.value = await api.getArbitrageOpportunities(start, end)
  updateChart()
}

const updateChart = () => {
  if (!chart) return

  // Aggregate profit by day
  const dailyProfit = {}
  opportunities.value.forEach(opp => {
    const date = opp.timestamp.split('T')[0]
    dailyProfit[date] = (dailyProfit[date] || 0) + opp.profit
  })

  const dates = Object.keys(dailyProfit).sort()
  const profits = dates.map(d => dailyProfit[d])

  const option = {
    title: {
      text: 'Daily Arbitrage Profit',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: dates
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: profits,
        type: 'bar',
        itemStyle: { color: '#4CAF50' }
      }
    ]
  }

  chart.setOption(option)
}

onMounted(() => {
  nextTick(() => {
    initChart()
    fetchData()
  })
})
</script>

<style scoped>
.arbitrage-analysis {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  text-align: center;
}

.card h3 {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}

.card .value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.chart-section, .table-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.profit-text {
  color: #4CAF50;
  font-weight: bold;
}
</style>
