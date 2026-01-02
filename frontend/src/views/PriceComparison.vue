<template>
  <div class="page-container">
    <TruckLoader :show="loading" :text="t('common.loadingData') || '加载图表数据中...'" />
    
    <div class="card chart-card">
      <div class="chart-info-bar">
        <div class="view-controls">
          <el-radio-group v-model="viewMode" size="small" @change="updateChartDisplay">
            <el-radio-button label="both">{{ t('chart.showBoth') || '全部显示' }}</el-radio-button>
            <el-radio-button label="candle">{{ t('chart.onlyPrice') || '仅价格' }}</el-radio-button>
            <el-radio-button label="volume">{{ t('chart.onlyVolume') || '仅成交量' }}</el-radio-button>
          </el-radio-group>
        </div>
        
        <div class="chart-description">
          <span class="desc-text">{{ t('chart.candlestickInfo') || 'Candlestick chart with volume indicators' }}</span>
        </div>
      </div>

      <div ref="chartRef" :style="{ width: '100%', height: viewMode === 'both' ? '500px' : '450px' }"></div>

      <div class="terminal-panel">
        <div class="panel-header">
          <div class="tabs">
            <div class="tab-item active">{{ t('chart.arbitrageAnalysis') || '套利机会分析 (Arbitrage Analysis)' }}</div>
          </div>
          <div class="account-summary" v-if="selectedData">
            <span class="label">{{ t('chart.selectedTime') || 'Selected Time' }}:</span>
            <span class="value">{{ selectedData.time }}</span>
          </div>
        </div>

        <div class="panel-body">
          <table class="terminal-table" v-if="selectedData">
            <thead>
              <tr>
                <th>{{ t('chart.exchange') || '交易所 (Exchange)' }}</th>
                <th>{{ t('chart.open') || '开盘价 (Open)' }}</th>
                <th>{{ t('chart.close') || '收盘价 (Close)' }}</th>
                <th>{{ t('chart.high') || '最高价 (High)' }}</th>
                <th>{{ t('chart.low') || '最低价 (Low)' }}</th>
                <th>{{ t('chart.change') || '涨跌幅 (Change)' }}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="dot binance-dot"></span> Binance (CEX)</td>
                <td>${{ selectedData.binance.open }}</td>
                <td>${{ selectedData.binance.close }}</td>
                <td>${{ selectedData.binance.high }}</td>
                <td>${{ selectedData.binance.low }}</td>
                <td :class="getPriceClass(selectedData.binance)">
                  {{ getPriceChange(selectedData.binance) }}%
                </td>
              </tr>
              <tr>
                <td><span class="dot uniswap-dot"></span> Uniswap V3 (DEX)</td>
                <td>${{ selectedData.uniswap.open }}</td>
                <td>${{ selectedData.uniswap.close }}</td>
                <td>${{ selectedData.uniswap.high }}</td>
                <td>${{ selectedData.uniswap.low }}</td>
                <td :class="getPriceClass(selectedData.uniswap)">
                  {{ getPriceChange(selectedData.uniswap) }}%
                </td>
              </tr>
              <tr class="highlight-row">
                <td><strong>💰 {{ t('chart.potentialArbitrage') || '潜在套利空间' }}</strong></td>
                <td colspan="4" class="spread-info">
                  {{ t('chart.priceSpread') || '收盘价差' }}: <strong>${{ Math.abs(selectedData.binance.close - selectedData.uniswap.close).toFixed(4) }}</strong>
                </td>
                <td class="profit-value">
                  {{ (Math.abs(1 - selectedData.binance.close / selectedData.uniswap.close) * 100).toFixed(4) }}%
                </td>
              </tr>
            </tbody>
          </table>
          
          <div class="empty-state" v-else>
            <el-icon><Pointer /></el-icon>
            <p>{{ t('chart.clickHint') || '请点击图表中的 K 线，查看该时点的比较数据' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts'
import { Pointer } from '@element-plus/icons-vue'
import { api } from '@/api'
import TruckLoader from '@/components/TruckLoader.vue'

const { t, locale } = useI18n() // 引入 locale 以便监听语言变化
const chartRef = ref(null)
let chart = null

const loading = ref(false)
const viewMode = ref('both')
const selectedData = ref(null)
let allRawData = []

const dateRange = ref(['2025-09-01 00:00:00', '2025-09-30 23:59:59'])
const interval = ref('4h')

// 监听语言切换，语言改变时重新渲染图表文字
watch(locale, () => {
  if (allRawData.length) updateChart(allRawData)
})

const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    window.addEventListener('resize', () => chart.resize())
    
    chart.on('click', (params) => {
      const index = params.dataIndex
      if (allRawData[index]) {
        selectedData.value = allRawData[index]
      }
    })
  }
}

const fetchData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2) return
  loading.value = true
  try {
    const [start, end] = dateRange.value
    const data = await api.getPriceCandles(start, end, interval.value)
    allRawData = data
    updateChart(data)
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    loading.value = false
  }
}

const getPriceClass = (data) => data.close >= data.open ? 'text-up' : 'text-down'
const getPriceChange = (data) => (((data.close - data.open) / data.open) * 100).toFixed(2)

const updateChartDisplay = () => {
  if (allRawData.length) updateChart(allRawData)
}

const updateChart = (data) => {
  if (!chart || !data) return
  const dates = data.map(item => item.time)
  
  const binanceData = data.map(item => [item.binance.open, item.binance.close, item.binance.low, item.binance.high])
  const uniswapData = data.map(item => [item.uniswap.open, item.uniswap.close, item.uniswap.low, item.uniswap.high])
  const binanceVolume = data.map(item => item.binance.usdt_volume || 0)
  const uniswapVolume = data.map(item => item.uniswap.usdt_volume || 0)

  let grid = []
  let xAxis = []
  let yAxis = []
  let series = []

  if (viewMode.value === 'both') {
    grid = [
      { left: '3%', right: '3%', top: '8%', height: '55%', containLabel: true },
      { left: '3%', right: '3%', top: '72%', height: '18%', containLabel: true }
    ]
    xAxis = [
      { type: 'category', data: dates, gridIndex: 0, axisLine: { lineStyle: { color: '#E5E7EB' } } },
      { type: 'category', data: dates, gridIndex: 1, axisLine: { lineStyle: { color: '#E5E7EB' } } }
    ]
    yAxis = [{ scale: true, gridIndex: 0 }, { scale: true, gridIndex: 1 }]
    series = [
      { name: 'Binance', type: 'candlestick', data: binanceData, xAxisIndex: 0, yAxisIndex: 0, itemStyle: { color: '#10B981', color0: '#EF4444' } },
      { name: 'Uniswap', type: 'candlestick', data: uniswapData, xAxisIndex: 0, yAxisIndex: 0, itemStyle: { color: '#3B82F6', color0: '#F59E0B' } },
      { name: t('chart.binanceVol') || 'Binance Volume', type: 'bar', data: binanceVolume, xAxisIndex: 1, yAxisIndex: 1, itemStyle: { color: 'rgba(16, 185, 129, 0.3)' } },
      { name: t('chart.uniswapVol') || 'Uniswap Volume', type: 'bar', data: uniswapVolume, xAxisIndex: 1, yAxisIndex: 1, itemStyle: { color: 'rgba(59, 130, 246, 0.3)' } }
    ]
  } else if (viewMode.value === 'candle') {
    grid = [{ left: '3%', right: '3%', top: '8%', height: '80%', containLabel: true }]
    xAxis = [{ type: 'category', data: dates, axisLine: { lineStyle: { color: '#E5E7EB' } } }]
    yAxis = [{ scale: true }]
    series = [
      { name: 'Binance', type: 'candlestick', data: binanceData, itemStyle: { color: '#10B981', color0: '#EF4444' } },
      { name: 'Uniswap', type: 'candlestick', data: uniswapData, itemStyle: { color: '#3B82F6', color0: '#F59E0B' } }
    ]
  } else {
    grid = [{ left: '3%', right: '3%', top: '8%', height: '80%', containLabel: true }]
    xAxis = [{ type: 'category', data: dates, axisLine: { lineStyle: { color: '#E5E7EB' } } }]
    yAxis = [{ scale: true }]
    series = [
      { name: t('chart.binanceVol') || 'Binance Volume', type: 'bar', data: binanceVolume, itemStyle: { color: 'rgba(16, 185, 129, 0.3)' } },
      { name: t('chart.uniswapVol') || 'Uniswap Volume', type: 'bar', data: uniswapVolume, itemStyle: { color: 'rgba(59, 130, 246, 0.3)' } }
    ]
  }

  const option = {
    tooltip: { trigger: 'axis', showContent: false, axisPointer: { type: 'cross' } },
    legend: { 
      show: true, 
      top: 0, 
      data: viewMode.value === 'volume' 
        ? [t('chart.binanceVol') || 'Binance Volume', t('chart.uniswapVol') || 'Uniswap Volume'] 
        : ['Binance', 'Uniswap']
    },
    grid,
    xAxis,
    yAxis,
    series
  }

  chart.setOption(option, true)
}

onMounted(() => {
  nextTick(() => {
    initChart()
    fetchData()
  })
})
</script>

<style lang="scss" scoped>
/* 样式保持不变 */
.page-container {
  padding: 0 24px 24px 20px;
  max-width: 1600px;
  margin: -8px auto 0;
}
.chart-card { padding: 20px; background: #ffffff; border-radius: 12px; }
.chart-info-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.terminal-panel {
  margin-top: 24px;
  border: 1px solid #eef0f2;
  border-radius: 8px;
  overflow: hidden;
  background: #fcfdfe;
  .panel-header {
    display: flex; justify-content: space-between; align-items: center; padding: 0 20px; background: #f8fafc; border-bottom: 1px solid #eef0f2;
    .tabs { display: flex; .tab-item { padding: 12px 20px; font-size: 13px; color: #10b981; border-bottom: 2px solid #10b981; font-weight: 600; } }
    .account-summary { font-size: 13px; .label { color: #94a3b8; margin-right: 8px; } .value { color: #1e293b; font-family: monospace; font-weight: 600; } }
  }
  .panel-body {
    min-height: 180px; padding: 10px;
    .terminal-table {
      width: 100%; border-collapse: collapse; font-size: 13px;
      th { text-align: left; padding: 12px; color: #94a3b8; border-bottom: 1px solid #f1f5f9; }
      td { padding: 14px 12px; color: #334155; border-bottom: 1px solid #f1f5f9; }
      .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }
      .binance-dot { background: #10b981; }
      .uniswap-dot { background: #3b82f6; }
      .text-up { color: #10b981; }
      .text-down { color: #ef4444; }
      .highlight-row { background: #f0fdf4; td { border-bottom: none; color: #166534; } .profit-value { font-weight: 700; font-size: 15px; color: #10b981; } }
    }
    .empty-state { height: 160px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #94a3b8; gap: 12px; }
  }
}
</style>