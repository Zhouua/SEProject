<template>
  <div class="arbitrage-analysis">
    <div class="header">
      <h2>{{ t('sidebar.arbitrage.title') }}</h2>
      <div class="controls">
        <el-date-picker
          v-model="dateRange"
          type="datetimerange"
          range-separator="至"
          start-placeholder="开始时间"
          end-placeholder="结束时间"
          :default-value="['2025-09-01 00:00:00', '2025-09-30 23:59:59']"
          :disabled-date="disabledDate"
          value-format="YYYY-MM-DD HH:mm:ss"
          @change="fetchData"
        />
      </div>
    </div>

    <div class="stats-cards">
      <div class="card">
        <h3>Total Opportunities</h3>
        <div class="value">{{ totalOpportunities }}</div>
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
      
      <div class="chart-section">
        <div ref="pieChartRef" style="width: 100%; height: 400px;"></div>
      </div>
    </div>
      
    <div class="table-section">
        <el-table 
          :data="opportunities" 
          style="width: 100%" 
          height="400"
          v-loading="tableLoading"
        >
          <el-table-column prop="time" label="时间" width="180">
            <template #default="scope">
              {{ new Date(scope.row.time).toLocaleString() }}
            </template>
          </el-table-column>
          <el-table-column prop="strategy" label="策略" width="250" />
          <el-table-column prop="eth_volume_uniswap" label="交易量 (ETH)" width="140">
            <template #default="scope">
              {{ scope.row.eth_volume_uniswap?.toFixed(4) }}
            </template>
          </el-table-column>
          <el-table-column prop="potential_profit_usdt" label="利润 (USDT)" sortable>
            <template #default="scope">
              <span class="profit-text">+{{ scope.row.potential_profit_usdt?.toFixed(2) }}</span>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="totalOpportunities"
            :page-sizes="[20, 50, 100]"
            layout="total, sizes, prev, pager, next"
            @current-change="handlePageChange"
            @size-change="fetchTableData"
          />
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
const pieChartRef = ref(null)
let chart = null
let pieChart = null
// 使用标准ISO格式初始化日期，确保浏览器兼容性
const dateRange = ref(['2025-09-01 00:00:00', '2025-09-30 23:59:59'])
const opportunities = ref([])
const totalOpportunities = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const dailyStats = ref([])

// 限制日期选择范围：只允许 2025-09-01 至 2025-09-30
const disabledDate = (time) => {
  const minDate = new Date('2025-09-01T00:00:00')
  const maxDate = new Date('2025-09-30T23:59:59')
  return time < minDate || time > maxDate
}

const totalProfit = computed(() => dailyStats.value.reduce((sum, item) => sum + (item.total_profit || 0), 0))
const avgProfit = computed(() => totalOpportunities.value ? totalProfit.value / totalOpportunities.value : 0)

const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    window.addEventListener('resize', () => chart.resize())
  }
  if (pieChartRef.value) {
    pieChart = echarts.init(pieChartRef.value)
    window.addEventListener('resize', () => pieChart.resize())
  }
}

const loading = ref(false)
const tableLoading = ref(false)

const fetchData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2) return
  
  loading.value = true
  try {
    const [start, end] = dateRange.value
    console.log('Fetching arbitrage data:', start, end)
    
    // 1. Fetch aggregated stats for chart (fast)
    dailyStats.value = await api.getDailyArbitrageStats(start, end)
    updateChart()
    
    // 2. Fetch paginated table data
    await fetchTableData()
    
    // 3. Update Pie Chart (Need full data or distribution stats, for now approximate from table or fetch all for stats)
    // To be accurate, we should fetch all opportunities (lightweight) or add a stats endpoint.
    // Let's fetch a larger batch for distribution analysis (e.g. 1000) or just use what we have if pagination is small.
    // Better: fetch all IDs and profits for stats.
    // For now, let's use the daily stats to estimate or fetch 1000 items for the pie chart sample.
    const sampleData = await api.getArbitrageOpportunities(start, end, 0, 1000)
    updatePieChart(sampleData.data)
    
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    loading.value = false
  }
}

const fetchTableData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2) return
  
  tableLoading.value = true
  try {
    const [start, end] = dateRange.value
    const offset = (currentPage.value - 1) * pageSize.value
    
    const response = await api.getArbitrageOpportunities(start, end, 0, pageSize.value, offset)
    opportunities.value = response.data || []
    // Note: Backend currently returns count of returned items, not total count. 
    // We might need to update backend to return total count for pagination.
    // For now, let's assume we can get total from daily stats sum of counts.
    totalOpportunities.value = dailyStats.value.reduce((sum, item) => sum + item.count, 0)
    
  } catch (error) {
    console.error('Error fetching table data:', error)
  } finally {
    tableLoading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchTableData()
}

const updateChart = () => {
  if (!chart) return
  
  const dates = dailyStats.value.map(item => item.date)
  const profits = dailyStats.value.map(item => item.total_profit)

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

const updatePieChart = (data) => {
  if (!pieChart || !data) return
  
  let low = 0, mid = 0, high = 0
  
  data.forEach(item => {
    const profit = item.potential_profit_usdt
    if (profit < 10) low++
    else if (profit < 50) mid++
    else high++
  })
  
  const option = {
    title: {
      text: 'Profit Distribution',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: 'Profit Range',
        type: 'pie',
        radius: '50%',
        data: [
          { value: low, name: '< $10' },
          { value: mid, name: '$10 - $50' },
          { value: high, name: '> $50' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  pieChart.setOption(option)
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

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
