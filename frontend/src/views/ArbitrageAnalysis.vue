<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">{{ t('sidebar.arbitrage.title') }}</h2>
      <div class="controls">
        <el-date-picker
          v-model="dateRange"
          type="datetimerange"
          range-separator="-"
          :start-placeholder="t('common.startDate')"
          :end-placeholder="t('common.endDate')"
          :default-value="['2025-09-01 00:00:00', '2025-09-30 23:59:59']"
          :disabled-date="disabledDate"
          value-format="YYYY-MM-DD HH:mm:ss"
          @change="fetchData"
          class="custom-picker"
        />
      </div>
    </div>

    <div class="stats-grid">
      <div class="card stat-card">
        <div class="stat-icon"><Activity :size="24" /></div>
        <div class="stat-content">
          <span class="label">Total Opportunities</span>
          <span class="value">{{ totalOpportunities }}</span>
        </div>
      </div>
      <div class="card stat-card">
        <div class="stat-icon"><DollarSign :size="24" /></div>
        <div class="stat-content">
          <span class="label">Total Potential Profit</span>
          <span class="value text-up">${{ totalProfit.toFixed(2) }}</span>
        </div>
      </div>
      <div class="card stat-card">
        <div class="stat-icon"><TrendingUp :size="24" /></div>
        <div class="stat-content">
          <span class="label">Avg. Profit / Trade</span>
          <span class="value">${{ avgProfit.toFixed(2) }}</span>
        </div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="card chart-card">
        <h3 class="card-title">Daily Profit Trend</h3>
        <div ref="chartRef" style="width: 100%; height: 350px;"></div>
      </div>
      
      <div class="card chart-card">
        <h3 class="card-title">Profit Distribution</h3>
        <div ref="pieChartRef" style="width: 100%; height: 350px;"></div>
      </div>
    </div>
      
    <div class="card table-card">
      <h3 class="card-title">Opportunity Log</h3>
      <el-table 
        :data="opportunities" 
        style="width: 100%" 
        v-loading="tableLoading"
        class="custom-table"
      >
        <el-table-column prop="time" label="Time" width="180">
          <template #default="scope">
            <span class="text-secondary">{{ new Date(scope.row.time).toLocaleString() }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="strategy" label="Strategy" width="250">
           <template #default="scope">
            <span class="strategy-tag">{{ scope.row.strategy || 'Triangular Arbitrage' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="eth_volume_uniswap" label="Volume (ETH)" width="140">
          <template #default="scope">
            {{ scope.row.eth_volume_uniswap?.toFixed(4) }}
          </template>
        </el-table-column>
        <el-table-column prop="potential_profit_usdt" label="Profit (USDT)" sortable>
          <template #default="scope">
            <span class="text-up font-medium">+{{ scope.row.potential_profit_usdt?.toFixed(2) }}</span>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="totalOpportunities"
          :page-sizes="[20, 50, 100]"
          layout="prev, pager, next"
          @current-change="handlePageChange"
          @size-change="fetchTableData"
          background
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
import { Activity, DollarSign, TrendingUp } from 'lucide-vue-next'

const { t } = useI18n()
const chartRef = ref(null)
const pieChartRef = ref(null)
let chart = null
let pieChart = null
const dateRange = ref(['2025-09-01 00:00:00', '2025-09-30 23:59:59'])
const opportunities = ref([])
const totalOpportunities = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const dailyStats = ref([])

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
    dailyStats.value = await api.getDailyArbitrageStats(start, end)
    updateChart()
    await fetchTableData()
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
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#E5E7EB',
      textStyle: { color: '#111827' }
    },
    grid: { left: '3%', right: '3%', bottom: '3%', top: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#E5E7EB' } },
      axisLabel: { color: '#9CA3AF' },
      splitLine: { show: false }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#F3F4F6' } },
      axisLabel: { color: '#9CA3AF' }
    },
    series: [
      {
        data: profits,
        type: 'bar',
        itemStyle: { 
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#10B981' },
            { offset: 1, color: '#34D399' }
          ]),
          borderRadius: [4, 4, 0, 0]
        },
        barMaxWidth: 40
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
    tooltip: { trigger: 'item' },
    legend: { bottom: 0, icon: 'circle', textStyle: { color: '#6B7280' } },
    series: [
      {
        name: 'Profit Range',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '45%'],
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: { show: false },
        data: [
          { value: low, name: '< $10', itemStyle: { color: '#9CA3AF' } },
          { value: mid, name: '$10 - $50', itemStyle: { color: '#3B82F6' } },
          { value: high, name: '> $50', itemStyle: { color: '#F59E0B' } }
        ]
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

<style lang="scss" scoped>
.page-container {
  padding: var(--spacing-lg) var(--spacing-xl);
  max-width: 1600px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  
  .page-title {
    font-size: 24px;
    font-weight: 600;
    color: var(--color-text-primary);
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
  
  .stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: var(--color-bg-tertiary);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text-primary);
  }
  
  .stat-content {
    display: flex;
    flex-direction: column;
    
    .label {
      font-size: 13px;
      color: var(--color-text-secondary);
      margin-bottom: 4px;
    }
    
    .value {
      font-size: 24px;
      font-weight: 700;
      color: var(--color-text-primary);
    }
  }
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.chart-card {
  padding: var(--spacing-lg);
  
  .card-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: var(--spacing-lg);
  }
}

.table-card {
  padding: var(--spacing-lg);
  
  .card-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: var(--spacing-lg);
  }
}

.pagination-container {
  margin-top: var(--spacing-lg);
  display: flex;
  justify-content: flex-end;
}

.strategy-tag {
  background: var(--color-bg-tertiary);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: var(--color-text-secondary);
}

/* Custom Element Plus Overrides */
:deep(.el-table) {
  --el-table-border-color: var(--color-border);
  --el-table-header-bg-color: var(--color-bg-primary);
  --el-table-row-hover-bg-color: var(--color-bg-tertiary);
}

:deep(.el-table th.el-table__cell) {
  background-color: var(--color-bg-primary);
  color: var(--color-text-secondary);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
}

:deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: var(--color-text-primary);
  color: white;
}
</style>
