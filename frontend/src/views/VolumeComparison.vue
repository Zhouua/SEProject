<template>
  <div class="page-container">
    <div class="content-wrapper">
      <TruckLoader :show="loading" text="加载交易量数据中..." />
      <!-- Page Header 
      <div class="page-header">
      <div>
        <h2 class="page-title">{{ t('sidebar.volumeComparison') }}</h2>
        <p class="page-subtitle">Compare trading volumes across exchanges</p>
      </div>
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
        <div class="stat-icon binance"><BarChart2 :size="24" /></div>
        <div class="stat-content">
          <span class="label">Binance Volume</span>
          <span class="value">{{ formatNumber(totalVolumeBinance) }} ETH</span>
          <span class="sub-value">≈ ${{ formatNumber(totalUsdtBinance) }}</span>
        </div>
      </div>
      
      <div class="card stat-card">
        <div class="stat-icon uniswap"><PieChart :size="24" /></div>
        <div class="stat-content">
          <span class="label">Uniswap Volume</span>
          <span class="value">{{ formatNumber(totalVolumeUniswap) }} ETH</span>
          <span class="sub-value">≈ ${{ formatNumber(totalUsdtUniswap) }}</span>
        </div>
      </div>

      <div class="card stat-card">
        <div class="stat-icon ratio"><Percent :size="24" /></div>
        <div class="stat-content">
          <span class="label">Volume Ratio</span>
          <span class="value">{{ volumeRatio }}</span>
          <span class="sub-value">Binance / Uniswap</span>
        </div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="card chart-card">
        <h3 class="card-title">ETH Volume Comparison</h3>
        <div ref="ethVolumeChartRef" style="width: 100%; height: 350px;"></div>
      </div>

      <div class="card chart-card">
        <h3 class="card-title">USDT Volume Comparison</h3>
        <div ref="usdtVolumeChartRef" style="width: 100%; height: 350px;"></div>
      </div>

      <div class="card chart-card full-width">
        <h3 class="card-title">Volume Correlation (ETH vs USDT)</h3>
        <p class="chart-desc">Correlation between trade size and value</p>
        <div ref="volumeRatioChartRef" style="width: 100%; height: 350px;"></div>
      </div>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts'
import { api } from '@/api'
import { store } from '@/store'
import { BarChart2, PieChart, Percent } from 'lucide-vue-next'
import TruckLoader from '@/components/TruckLoader.vue'

const { t } = useI18n()
const dateRange = ref(['2025-09-01 00:00:00', '2025-09-30 23:59:59'])
const priceData = ref([])

const disabledDate = (time) => {
  const minDate = new Date('2025-09-01T00:00:00')
  const maxDate = new Date('2025-09-30T23:59:59')
  return time < minDate || time > maxDate
}

const ethVolumeChartRef = ref(null)
const usdtVolumeChartRef = ref(null)
const volumeRatioChartRef = ref(null)

let ethVolumeChart = null
let usdtVolumeChart = null
let volumeRatioChart = null

const totalVolumeBinance = computed(() => {
  return priceData.value.reduce((sum, item) => sum + (item.binance?.eth_volume || 0), 0)
})

const totalVolumeUniswap = computed(() => {
  return priceData.value.reduce((sum, item) => sum + (item.uniswap?.eth_volume || 0), 0)
})

const totalUsdtBinance = computed(() => {
  return priceData.value.reduce((sum, item) => sum + (item.binance?.usdt_volume || 0), 0)
})

const totalUsdtUniswap = computed(() => {
  return priceData.value.reduce((sum, item) => sum + (item.uniswap?.usdt_volume || 0), 0)
})

const volumeRatio = computed(() => {
  if (totalVolumeUniswap.value === 0) return 'N/A'
  return (totalVolumeBinance.value / totalVolumeUniswap.value).toFixed(2) + ' : 1'
})

const formatNumber = (num) => {
  if (num >= 1000000) return (num / 1000000).toFixed(2) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(2) + 'K'
  return num.toFixed(2)
}

const loading = ref(false)

const fetchData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2) return
  
  loading.value = true
  
  // 延迟 50ms，确保 loading 动画能显示
  await new Promise(resolve => setTimeout(resolve, 50))
  
  try {
    const [start, end] = dateRange.value
    
    const cachedData = store.getCachedPriceData(start, end)
    if (cachedData) {
      priceData.value = cachedData
      updateCharts()
      return
    }
    
    const data = await api.getHistoricalPrices(start, end, 50000)
    store.setPriceData(data, start, end)
    priceData.value = data
    updateCharts()
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    loading.value = false
  }
}

const initCharts = () => {
  if (ethVolumeChartRef.value) ethVolumeChart = echarts.init(ethVolumeChartRef.value)
  if (usdtVolumeChartRef.value) usdtVolumeChart = echarts.init(usdtVolumeChartRef.value)
  if (volumeRatioChartRef.value) volumeRatioChart = echarts.init(volumeRatioChartRef.value)

  window.addEventListener('resize', () => {
    ethVolumeChart?.resize()
    usdtVolumeChart?.resize()
    volumeRatioChart?.resize()
  })
}

const updateCharts = () => {
  if (!priceData.value || priceData.value.length === 0) return

  const times = priceData.value.map(item => item.time)
  const ethBinance = priceData.value.map(item => item.binance?.eth_volume || 0)
  const ethUniswap = priceData.value.map(item => item.uniswap?.eth_volume || 0)
  const usdtBinance = priceData.value.map(item => item.binance?.usdt_volume || 0)
  const usdtUniswap = priceData.value.map(item => item.uniswap?.usdt_volume || 0)

  if (ethVolumeChart) {
    ethVolumeChart.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
      legend: { bottom: 0, icon: 'circle', textStyle: { color: '#6B7280' } },
      grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
      xAxis: {
        type: 'category',
        data: times,
        axisLine: { lineStyle: { color: '#E5E7EB' } },
        axisLabel: { show: false },
        splitLine: { show: false }
      },
      yAxis: {
        type: 'value',
        name: 'ETH',
        splitLine: { lineStyle: { color: '#F3F4F6' } },
        axisLabel: { color: '#9CA3AF' }
      },
      series: [
        {
          name: 'Binance',
          type: 'line',
          data: ethBinance,
          smooth: true,
          showSymbol: false,
          sampling: 'lttb',  // ECharts 内置的采样算法，保持趋势
          large: true,       // 大数据优化
          lineStyle: { color: '#F59E0B', width: 2 },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(245, 158, 11, 0.2)' },
              { offset: 1, color: 'rgba(245, 158, 11, 0)' }
            ])
          }
        },
        {
          name: 'Uniswap',
          type: 'line',
          data: ethUniswap,
          smooth: true,
          showSymbol: false,
          sampling: 'lttb',
          large: true,
          lineStyle: { color: '#EC4899', width: 2 },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(236, 72, 153, 0.2)' },
              { offset: 1, color: 'rgba(236, 72, 153, 0)' }
            ])
          }
        }
      ]
    })
  }

  if (usdtVolumeChart) {
    usdtVolumeChart.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
      legend: { bottom: 0, icon: 'circle', textStyle: { color: '#6B7280' } },
      grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
      xAxis: {
        type: 'category',
        data: times,
        axisLine: { lineStyle: { color: '#E5E7EB' } },
        axisLabel: { show: false },
        splitLine: { show: false }
      },
      yAxis: {
        type: 'value',
        name: 'USDT',
        splitLine: { lineStyle: { color: '#F3F4F6' } },
        axisLabel: { 
          color: '#9CA3AF',
          formatter: (value) => {
            if (value >= 1000000) return (value / 1000000).toFixed(0) + 'M'
            if (value >= 1000) return (value / 1000).toFixed(0) + 'K'
            return value
          }
        }
      },
      series: [
        {
          name: 'Binance',
          type: 'bar',
          data: usdtBinance,
          itemStyle: { color: '#F59E0B' }
        },
        {
          name: 'Uniswap',
          type: 'bar',
          data: usdtUniswap,
          itemStyle: { color: '#EC4899' }
        }
      ]
    })
  }

  if (volumeRatioChart) {
    const scatterData = priceData.value.map(item => [
      item.binance?.eth_volume || 0,
      item.binance?.usdt_volume || 0
    ])

    volumeRatioChart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: (params) => `ETH: ${params.value[0].toFixed(2)}<br/>USDT: ${params.value[1].toFixed(2)}`
      },
      grid: { left: '5%', right: '5%', bottom: '10%', top: '10%', containLabel: true },
      xAxis: {
        type: 'value',
        name: 'ETH Volume',
        nameLocation: 'middle',
        nameGap: 30,
        axisLine: { lineStyle: { color: '#E5E7EB' } },
        axisLabel: { color: '#9CA3AF' },
        splitLine: { show: false }
      },
      yAxis: {
        type: 'value',
        name: 'USDT Volume',
        nameLocation: 'middle',
        nameGap: 50,
        splitLine: { lineStyle: { color: '#F3F4F6' } },
        axisLabel: { color: '#9CA3AF' }
      },
      series: [{
        type: 'scatter',
        data: scatterData,
        large: true,           // 大数据模式
        largeThreshold: 2000,  // 大于 2000 个点启用大数据优化
        symbolSize: 4,         // 减小点的大小
        itemStyle: {
          color: '#10B981',
          opacity: 0.4       // 降低透明度
        }
      }]
    })
  }
}

onMounted(() => {
  nextTick(() => {
    initCharts()
    fetchData()
  })
})
</script>

<style lang="scss" scoped>
.page-container {
  padding: 0 24px 24px 20px;
  max-width: 1600px;
  margin: -8px auto 0;
  position: relative;
}

.content-wrapper {
  position: relative;
  min-height: 400px;
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
    margin-bottom: 4px;
  }
  
  .page-subtitle {
    font-size: 14px;
    color: var(--color-text-secondary);
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
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    
    &.binance { background: linear-gradient(135deg, #F59E0B 0%, #FCD34D 100%); }
    &.uniswap { background: linear-gradient(135deg, #EC4899 0%, #F472B6 100%); }
    &.ratio { background: linear-gradient(135deg, #10B981 0%, #34D399 100%); }
  }
  
  .stat-content {
    display: flex;
    flex-direction: column;
    
    .label { font-size: 13px; color: var(--color-text-secondary); margin-bottom: 4px; }
    .value { font-size: 20px; font-weight: 700; color: var(--color-text-primary); margin-bottom: 2px; }
    .sub-value { font-size: 12px; color: var(--color-text-tertiary); }
  }
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-lg);
  
  .full-width {
    grid-column: 1 / -1;
  }
}

.chart-card {
  padding: var(--spacing-lg);
  
  .card-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: var(--spacing-lg);
  }
  
  .chart-desc {
    font-size: 12px;
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-lg);
  }
}
</style>
