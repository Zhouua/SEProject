<template>
  <div class="page-container">
    <!--
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
    -->
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
      <div class="card-header">
        <h3 class="card-title">Opportunity Log</h3>
      </div>
      <el-table 
        :data="opportunities" 
        style="width: 100%" 
        v-loading="tableLoading"
        class="custom-table"
      >
        <el-table-column prop="trade_id" label="TRADE ID" width="120" align="center">
          <template #default="scope">
            <span class="trade-id-tag">#{{ scope.row.trade_id }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="time" label="TIME" width="180">
          <template #default="scope">
            <span class="text-secondary font-mono">{{ formatTime(scope.row.time) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="strategy" label="STRATEGY" min-width="200">
           <template #default="scope">
            <span class="strategy-tag" :class="getStrategyClass(scope.row.direction)">{{ scope.row.strategy || 'Triangular Arbitrage' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="potential_profit_usdt" label="PROFIT (USDT)" width="150" align="right" sortable>
          <template #default="scope">
            <span class="text-up font-medium font-mono">+${{ scope.row.potential_profit_usdt?.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="DETAILS" width="120" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" @click="showDetails(scope.row)" class="details-btn">
              <el-icon><View /></el-icon>
              View
            </el-button>
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

    <!-- 详情模态框 -->
    <el-dialog
      v-model="detailsVisible"
      title="Arbitrage Opportunity Details"
      width="600px"
      :close-on-click-modal="false"
      class="details-dialog"
    >
      <div v-if="selectedOpportunity" class="details-content">
        <!-- 基础信息 -->
        <div class="detail-section">
          <h4 class="section-title">
            <el-icon><Document /></el-icon>
            Basic Information
          </h4>
          <div class="detail-grid">
            <div class="detail-item">
              <span class="label">Trade ID:</span>
              <span class="value">#{{ selectedOpportunity.trade_id }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Time:</span>
              <span class="value">{{ formatTime(selectedOpportunity.time) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Strategy:</span>
              <span class="value">
                <span class="strategy-tag" :class="getStrategyClass(selectedOpportunity.direction)">
                  {{ selectedOpportunity.strategy }}
                </span>
              </span>
            </div>
            <div class="detail-item">
              <span class="label">Direction:</span>
              <span class="value">{{ selectedOpportunity.direction === 0 ? 'Uniswap → Binance' : 'Binance → Uniswap' }}</span>
            </div>
          </div>
        </div>

        <!-- 价格信息 -->
        <div class="detail-section">
          <h4 class="section-title">
            <el-icon><TrendingUp /></el-icon>
            Price Information
          </h4>
          <div class="detail-grid">
            <div class="detail-item">
              <span class="label">Binance Price:</span>
              <span class="value price">${{ selectedOpportunity.binance_price?.toFixed(2) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Uniswap Price:</span>
              <span class="value price">${{ selectedOpportunity.uniswap_price?.toFixed(2) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Price Difference:</span>
              <span class="value" :class="selectedOpportunity.price_diff >= 0 ? 'text-up' : 'text-down'">
                ${{ selectedOpportunity.price_diff?.toFixed(2) }} ({{ selectedOpportunity.price_diff_percent?.toFixed(2) }}%)
              </span>
            </div>
            <div class="detail-item">
              <span class="label">ETH Volume (Uniswap):</span>
              <span class="value">{{ selectedOpportunity.eth_volume_uniswap?.toFixed(4) }} ETH</span>
            </div>
          </div>
        </div>

        <!-- 收益信息 -->
        <div class="detail-section">
          <h4 class="section-title">
            <el-icon><DollarSign /></el-icon>
            Profit Metrics
          </h4>
          <div class="detail-grid">
            <div class="detail-item highlight">
              <span class="label">Potential Profit:</span>
              <span class="value profit">+${{ selectedOpportunity.potential_profit_usdt?.toFixed(2) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Profit Rate:</span>
              <span class="value text-up">{{ (selectedOpportunity.profit_rate * 100)?.toFixed(4) }}%</span>
            </div>
            <div class="detail-item">
              <span class="label">Score:</span>
              <span class="value score">{{ selectedOpportunity.score?.toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button @click="detailsVisible = false">Close</el-button>
        <el-button type="primary" @click="exportOpportunity">
          <el-icon><Download /></el-icon>
          Export
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts'
import { api } from '@/api'
import { Activity, DollarSign, TrendingUp, View, Download, Document } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

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
const detailsVisible = ref(false)
const selectedOpportunity = ref(null)

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

const formatTime = (timeStr) => {
  const date = new Date(timeStr)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const getStrategyClass = (direction) => {
  return direction === 0 ? 'strategy-u2b' : 'strategy-b2u'
}

const showDetails = (row) => {
  selectedOpportunity.value = row
  detailsVisible.value = true
}

const exportOpportunity = () => {
  if (!selectedOpportunity.value) return
  
  const data = [
    ['Field', 'Value'],
    ['Trade ID', selectedOpportunity.value.trade_id],
    ['Time', formatTime(selectedOpportunity.value.time)],
    ['Strategy', selectedOpportunity.value.strategy],
    ['Direction', selectedOpportunity.value.direction === 0 ? 'Uniswap → Binance' : 'Binance → Uniswap'],
    ['Binance Price', `$${selectedOpportunity.value.binance_price?.toFixed(2)}`],
    ['Uniswap Price', `$${selectedOpportunity.value.uniswap_price?.toFixed(2)}`],
    ['Price Difference', `$${selectedOpportunity.value.price_diff?.toFixed(2)}`],
    ['Price Diff %', `${selectedOpportunity.value.price_diff_percent?.toFixed(2)}%`],
    ['ETH Volume', `${selectedOpportunity.value.eth_volume_uniswap?.toFixed(4)} ETH`],
    ['Potential Profit', `$${selectedOpportunity.value.potential_profit_usdt?.toFixed(2)}`],
    ['Profit Rate', `${(selectedOpportunity.value.profit_rate * 100)?.toFixed(4)}%`],
    ['Score', selectedOpportunity.value.score?.toFixed(2)]
  ]
  
  const csv = data.map(row => row.join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `arbitrage_opportunity_${selectedOpportunity.value.trade_id}.csv`
  a.click()
  window.URL.revokeObjectURL(url)
  
  ElMessage.success('Opportunity data exported successfully!')
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
  padding: 0 24px 24px 20px;
  max-width: 1600px;
  margin: -8px auto 0;
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
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
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
  padding: 0;
  overflow: hidden;
  
  .card-header {
    padding: var(--spacing-lg) var(--spacing-lg) var(--spacing-md);
    margin-bottom: var(--spacing-sm);
  }
}

.strategy-tag {
  background: var(--color-bg-tertiary);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
}

.strategy-u2b {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.strategy-b2u {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border: none;
}

.trade-id-tag {
  display: inline-block;
  padding: 4px 10px;
  background: var(--color-bg-tertiary);
  border-radius: 4px;
  font-family: 'Monaco', 'Courier New', monospace;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.details-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.pagination-container {
  padding: var(--spacing-md) var(--spacing-lg);
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid var(--color-border);
}

/* Custom Element Plus Overrides */
:deep(.el-table) {
  --el-table-border-color: var(--color-border);
  --el-table-header-bg-color: var(--color-bg-primary);
  --el-table-row-hover-bg-color: var(--color-bg-tertiary);
  --el-table-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
}

:deep(.el-table th.el-table__cell) {
  background-color: var(--color-bg-primary);
  color: var(--color-text-tertiary);
  font-weight: 600;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 12px 0;
}

:deep(.el-table td.el-table__cell) {
  padding: 16px 0;
  border-bottom: 1px solid var(--color-bg-tertiary);
}

:deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: var(--color-text-primary);
  color: white;
}

/* 详情模态框样式 */
:deep(.details-dialog) {
  .el-dialog__header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    margin: 0;
    border-radius: 8px 8px 0 0;
  }
  
  .el-dialog__title {
    color: white;
    font-size: 18px;
    font-weight: 600;
  }
  
  .el-dialog__close {
    color: white;
    font-size: 20px;
    
    &:hover {
      color: rgba(255, 255, 255, 0.8);
    }
  }
  
  .el-dialog__body {
    padding: 24px;
  }
  
  .el-dialog__footer {
    padding: 16px 24px;
    border-top: 1px solid var(--color-border);
  }
}

.details-content {
  .detail-section {
    margin-bottom: 24px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .section-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      font-weight: 600;
      color: var(--color-text-primary);
      margin-bottom: 16px;
      padding-bottom: 8px;
      border-bottom: 2px solid var(--color-bg-tertiary);
    }
    
    .detail-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }
    
    .detail-item {
      display: flex;
      flex-direction: column;
      gap: 4px;
      
      &.highlight {
        grid-column: 1 / -1;
        padding: 16px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 8px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        
        .value {
          font-size: 24px;
        }
      }
      
      .label {
        font-size: 12px;
        color: var(--color-text-tertiary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }
      
      .value {
        font-size: 14px;
        color: var(--color-text-primary);
        font-weight: 600;
        
        &.price {
          font-family: 'Monaco', 'Courier New', monospace;
          font-size: 16px;
        }
        
        &.profit {
          font-family: 'Monaco', 'Courier New', monospace;
          color: #10B981;
          font-weight: 700;
        }
        
        &.score {
          font-family: 'Monaco', 'Courier New', monospace;
          color: #667eea;
        }
      }
    }
  }
}
</style>
