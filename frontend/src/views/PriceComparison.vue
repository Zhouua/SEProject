<template>
  <div class="page-container">
    <TruckLoader :show="loading" text="加载价格数据中..." />
    
    <div class="main-layout">
      <div class="left-content">
        <div class="card chart-card full-height-card">
          <div class="chart-info-bar">
            <div class="view-controls">
              <el-radio-group v-model="viewMode" size="small" @change="updateChartDisplay">
                <el-radio-button label="both">{{ t('chart.showBoth') }}</el-radio-button>
                <el-radio-button label="candle">{{ t('chart.onlyPrice') }}</el-radio-button>
                <el-radio-button label="volume">{{ t('chart.onlyVolume') }}</el-radio-button>
              </el-radio-group>
            </div>
            
            <div class="chart-description">
              <span class="desc-text">{{ t('chart.candlestickInfo') }}</span>
            </div>
          </div>

          <div ref="chartRef" :style="{ width: '100%', height: viewMode === 'both' ? '500px' : '450px' }"></div>

          <div class="terminal-panel">
            <div class="panel-header">
              <div class="tabs">
                <div class="tab-item active">{{ t('chart.arbitrageAnalysis') }}</div>
              </div>
              <div class="account-summary" v-if="selectedData">
                <span class="label">{{ t('chart.selectedTime') }}:</span>
                <span class="value">{{ selectedData.time }}</span>
              </div>
            </div>

            <div class="panel-body">
              <table class="terminal-table" v-if="selectedData">
                <thead>
                  <tr>
                    <th>{{ t('chart.exchange') }}</th>
                    <th>{{ t('chart.open') }}</th>
                    <th>{{ t('chart.close') }}</th>
                    <th>{{ t('chart.high') }}</th>
                    <th>{{ t('chart.low') }}</th>
                    <th>{{ t('chart.change') }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><span class="dot binance-dot"></span> Binance (CEX)</td>
                    <td>${{ selectedData.binance.open }}</td>
                    <td>${{ selectedData.binance.close }}</td>
                    <td>${{ selectedData.binance.high }}</td>
                    <td>${{ selectedData.binance.low }}</td>
                    <td :class="getPriceClass(selectedData.binance)">{{ getPriceChange(selectedData.binance) }}%</td>
                  </tr>
                  <tr>
                    <td><span class="dot uniswap-dot"></span> Uniswap V3 (DEX)</td>
                    <td>${{ selectedData.uniswap.open }}</td>
                    <td>${{ selectedData.uniswap.close }}</td>
                    <td>${{ selectedData.uniswap.high }}</td>
                    <td>${{ selectedData.uniswap.low }}</td>
                    <td :class="getPriceClass(selectedData.uniswap)">{{ getPriceChange(selectedData.uniswap) }}%</td>
                  </tr>
                  <tr class="highlight-row">
                    <td><strong>💰 {{ t('chart.potentialArbitrage') }}</strong></td>
                    <td colspan="4" class="spread-info">
                      {{ t('chart.priceSpread') }}: <strong>${{ Math.abs(selectedData.binance.close - selectedData.uniswap.close).toFixed(4) }}</strong>
                    </td>
                    <td class="profit-value">
                      {{ (Math.abs(1 - selectedData.binance.close / selectedData.uniswap.close) * 100).toFixed(4) }}%
                    </td>
                  </tr>
                </tbody>
              </table>
              <div class="empty-state" v-else>
                <el-icon><Pointer /></el-icon>
                <p>{{ t('chart.clickHint') }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="right-sidebar">
        <div class="card sidebar-card full-height-card">
          <div class="sidebar-section">
            <div class="sidebar-header">
              <h3 class="sidebar-title">{{ t('dashboard.watchlist') }}</h3>
              <span class="more-link" @click="$router.push('/arbitrage-history')">{{ t('dashboard.more') }}</span>
            </div>
            <div class="asset-list scrollbar-custom">
              <div v-for="(item, index) in watchlist" :key="'recent-'+index" class="asset-item" @click="handleWatchlistItemClick(item)">
                <div class="asset-main">
                  <img :src="item.icon" class="asset-logo" />
                  <div class="asset-meta">
                    <span class="pair-name">{{ item.symbol }}</span>
                    <span class="strategy-tag">{{ item.time.split(' ')[1] }}</span>
                  </div>
                </div>
                <div class="asset-stats">
                  <div class="current-price text-up">+${{ item.price }}</div>
                  <div class="profit-tag">{{ t('chart.priceSpread') }}: ${{ item.change }}</div>
                </div>
              </div>
            </div>
          </div>

          <el-divider />

          <div class="sidebar-section">
            <div class="sidebar-header">
              <h3 class="sidebar-title">{{ t('dashboard.topMovers') || 'Top Movers' }}</h3>
            </div>
            <div class="asset-list">
              <div v-for="(item, index) in topMovers" :key="'mover-'+index" class="asset-item">
                <div class="asset-main">
                  <div class="asset-icon" :class="'rank-' + (index + 1)">{{ index + 1 }}</div>
                  <div class="asset-meta">
                    <span class="pair-name">{{ item.symbol }}</span>
                    <span class="strategy-tag">{{ t('chart.maxProfit') || 'Max Profit' }}</span>
                  </div>
                </div>
                <div class="asset-stats">
                  <div class="current-price">${{ item.price }}</div>
                  <div class="profit-tag text-up">+{{ item.change }}%</div>
                </div>
              </div>
            </div>
          </div>

          <div class="sidebar-footer">
            <button class="btn btn-secondary" @click="refreshAllData">
              <el-icon><Refresh /></el-icon> {{ t('common.refresh') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts'
import { Pointer, Refresh } from '@element-plus/icons-vue'
import { api } from '@/api'
import TruckLoader from '@/components/TruckLoader.vue'

const { t, locale } = useI18n()
const chartRef = ref(null)
let chart = null

const loading = ref(false)
const viewMode = ref('both')
const selectedData = ref(null)
const watchlist = ref([])
const topMovers = ref([])
let allRawData = []
let refreshTimer = null

const dateRange = ref(['2025-09-01 00:00:00', '2025-09-30 23:59:59'])
const interval = ref('4h')

// 监听语言切换，刷新图表图例标签
watch(locale, () => { 
  if (allRawData.length) updateChart(allRawData) 
})

const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    window.addEventListener('resize', () => chart.resize())
    chart.on('click', (params) => {
      const index = params.dataIndex
      if (allRawData[index]) selectedData.value = allRawData[index]
    })
  }
}

const fetchSidebarData = async () => {
  try {
    const [start, end] = dateRange.value
    
    // 1. 获取最近套利机会数据
    const recentArb = await api.getArbitrageOpportunities(start, end, 0, 5, 0, 'time_desc')
    watchlist.value = recentArb.data.map(item => ({
      symbol: 'ETH-USDT',
      price: item.potential_profit_usdt.toFixed(2),
      change: item.price_diff.toFixed(2),
      icon: 'https://cryptologos.cc/logos/ethereum-eth-logo.png?v=029',
      time: item.time,
      raw: item
    }))

    // 2. 获取收益排行
    const topArb = await api.getTopArbitrage(5)
    topMovers.value = topArb.map(item => ({
      symbol: 'ETH-USDT',
      price: item.potential_profit_usdt.toFixed(2),
      change: ((item.price_diff / item.binance_price) * 100).toFixed(2),
      time: item.time
    }))
  } catch (error) {
    console.error('Sidebar Data Fetch Error:', error)
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
    console.error('Chart Data Fetch Error:', error) 
  } finally { 
    loading.value = false 
  }
}

const refreshAllData = () => {
  fetchData()
  fetchSidebarData()
}

const handleWatchlistItemClick = (item) => {
  console.log('User clicked arbitrage record:', item.raw)
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

  let grid = [], xAxis = [], yAxis = [], series = []
  
  // 注入 i18n 标签
  const labelBinance = 'Binance'
  const labelUniswap = 'Uniswap'
  const labelVolB = t('chart.binanceVol') || 'Binance Vol'
  const labelVolU = t('chart.uniswapVol') || 'Uniswap Vol'

  if (viewMode.value === 'both') {
    grid = [
      { left: '4%', right: '4%', top: '8%', height: '55%', containLabel: true }, 
      { left: '4%', right: '4%', top: '72%', height: '18%', containLabel: true }
    ]
    xAxis = [
      { type: 'category', data: dates, gridIndex: 0 }, 
      { type: 'category', data: dates, gridIndex: 1 }
    ]
    yAxis = [{ scale: true, gridIndex: 0 }, { scale: true, gridIndex: 1 }]
    series = [
      { name: labelBinance, type: 'candlestick', data: binanceData, xAxisIndex: 0, yAxisIndex: 0, itemStyle: { color: '#10B981', color0: '#EF4444' } },
      { name: labelUniswap, type: 'candlestick', data: uniswapData, xAxisIndex: 0, yAxisIndex: 0, itemStyle: { color: '#3B82F6', color0: '#F59E0B' } },
      { name: labelVolB, type: 'bar', data: binanceVolume, xAxisIndex: 1, yAxisIndex: 1, itemStyle: { color: 'rgba(16, 185, 129, 0.3)' } },
      { name: labelVolU, type: 'bar', data: uniswapVolume, xAxisIndex: 1, yAxisIndex: 1, itemStyle: { color: 'rgba(59, 130, 246, 0.3)' } }
    ]
  } else {
    grid = [{ left: '4%', right: '4%', top: '8%', height: '80%', containLabel: true }]
    xAxis = [{ type: 'category', data: dates }]
    yAxis = [{ scale: true }]
    series = viewMode.value === 'candle' ? [
      { name: labelBinance, type: 'candlestick', data: binanceData, itemStyle: { color: '#10B981', color0: '#EF4444' } },
      { name: labelUniswap, type: 'candlestick', data: uniswapData, itemStyle: { color: '#3B82F6', color0: '#F59E0B' } }
    ] : [
      { name: labelVolB, type: 'bar', data: binanceVolume, itemStyle: { color: 'rgba(16, 185, 129, 0.3)' } },
      { name: labelVolU, type: 'bar', data: uniswapVolume, itemStyle: { color: 'rgba(59, 130, 246, 0.3)' } }
    ]
  }
  chart.setOption({ 
    tooltip: { trigger: 'axis', showContent: false, axisPointer: { type: 'cross' } }, 
    legend: { show: true, top: 0 }, 
    grid, xAxis, yAxis, series 
  }, true)
}

onMounted(() => {
  nextTick(() => {
    initChart()
    fetchData()
    fetchSidebarData()
    refreshTimer = setInterval(fetchSidebarData, 30000)
  })
})

onUnmounted(() => { 
  if (refreshTimer) clearInterval(refreshTimer) 
})
</script>

<style lang="scss" scoped>
.page-container {
  padding: 0 24px 24px 20px;
  max-width: 100%;
}

.main-layout {
  display: flex;
  gap: 20px;
  align-items: stretch; /* 保证左右高度一致 */
}

.left-content {
  flex: 1;
  min-width: 0;
}

.right-sidebar {
  width: 320px;
  flex-shrink: 0;
}

.full-height-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card {
  padding: 20px;
  background: #ffffff;
  border-radius: var(--radius-lg);
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.sidebar-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  .sidebar-title { font-size: 15px; font-weight: 700; color: var(--color-text-primary); }
  .more-link { font-size: 12px; color: var(--color-accent); cursor: pointer; &:hover { text-decoration: underline; } }
}

.asset-list {
  overflow-y: auto;
  flex: 1;
  .asset-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-radius: var(--radius-md);
    transition: 0.2s;
    cursor: pointer;
    &:hover { background: var(--color-bg-primary); transform: translateX(-4px); }
    
    .asset-main {
      display: flex;
      align-items: center;
      gap: 10px;
      .asset-logo { width: 28px; height: 28px; }
      .asset-icon { 
        width: 28px; height: 28px; background: #f0fdf4; color: #10b981; 
        display: flex; align-items: center; justify-content: center; 
        border-radius: 50%; font-weight: 800; font-size: 12px;
        &.rank-1 { background: #fef3c7; color: #d97706; }
        &.rank-2 { background: #f3f4f6; color: #4b5563; }
      }
      .asset-meta {
        display: flex; flex-direction: column;
        .pair-name { font-weight: 600; font-size: 13px; }
        .strategy-tag { font-size: 11px; color: var(--color-text-tertiary); }
      }
    }
    .asset-stats {
      text-align: right;
      .current-price { font-family: monospace; font-weight: 700; font-size: 13px; }
      .profit-tag { font-size: 11px; color: var(--color-text-tertiary); }
    }
  }
}

.terminal-panel {
  margin-top: 24px; border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden;
  .panel-header {
    display: flex; justify-content: space-between; align-items: center; padding: 0 20px; background: #f8fafc; border-bottom: 1px solid var(--color-border);
    .tab-item { padding: 12px 20px; font-size: 13px; color: var(--color-accent); border-bottom: 2px solid var(--color-accent); font-weight: 600; }
  }
  .panel-body { padding: 10px; .terminal-table { width: 100%; border-collapse: collapse; th { text-align: left; padding: 12px; color: var(--color-text-tertiary); font-size: 12px; } td { padding: 12px; border-bottom: 1px solid var(--color-bg-primary); font-size: 13px; } } }
}

.text-up { color: #10B981; }
.text-down { color: #EF4444; }
.scrollbar-custom::-webkit-scrollbar { width: 4px; }
.scrollbar-custom::-webkit-scrollbar-thumb { background: #e5e7eb; border-radius: 10px; }
.sidebar-footer { padding-top: 15px; .btn { width: 100%; padding: 10px; } }
</style>