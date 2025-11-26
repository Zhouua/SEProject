<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h2 class="page-title">{{ t('sidebar.liquidityAnalysis') }}</h2>
        <p class="page-subtitle">Market Depth & Liquidity Analysis</p>
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

    <div class="liquidity-cards">
      <div class="card liquidity-card">
        <div class="card-header">
          <div class="platform-info">
            <img src="https://cryptologos.cc/logos/binance-coin-bnb-logo.png" class="platform-icon" />
            <h3>Binance</h3>
          </div>
          <span class="badge centralized">CEX</span>
        </div>
        <div class="metrics">
          <div class="metric">
            <span class="label">Avg. Volume / Min</span>
            <span class="value">{{ formatNumber(avgVolumeBinance) }} ETH</span>
          </div>
          <div class="metric">
            <span class="label">Total Volume</span>
            <span class="value">${{ formatNumber(totalUsdtBinance) }}</span>
          </div>
          <div class="metric">
            <span class="label">Liquidity Score</span>
            <div class="score-bar">
              <div class="score-fill binance" :style="{ width: liquidityScoreBinance + '%' }"></div>
              <span class="score-text">{{ liquidityScoreBinance }}/100</span>
            </div>
          </div>
        </div>
      </div>

      <div class="card liquidity-card">
        <div class="card-header">
          <div class="platform-info">
            <img src="https://cryptologos.cc/logos/uniswap-uni-logo.png" class="platform-icon" />
            <h3>Uniswap V3</h3>
          </div>
          <span class="badge decentralized">DEX</span>
        </div>
        <div class="metrics">
          <div class="metric">
            <span class="label">Avg. Volume / Min</span>
            <span class="value">{{ formatNumber(avgVolumeUniswap) }} ETH</span>
          </div>
          <div class="metric">
            <span class="label">Total Volume</span>
            <span class="value">${{ formatNumber(totalUsdtUniswap) }}</span>
          </div>
          <div class="metric">
            <span class="label">Liquidity Score</span>
            <div class="score-bar">
              <div class="score-fill uniswap" :style="{ width: liquidityScoreUniswap + '%' }"></div>
              <span class="score-text">{{ liquidityScoreUniswap }}/100</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="card chart-card full-width">
        <div class="chart-header">
          <h3 class="chart-title">Liquidity Trend (USDT)</h3>
          <p class="chart-desc">Total liquidity value over time</p>
        </div>
        <div ref="liquidityTrendChartRef" style="width: 100%; height: 400px;"></div>
      </div>

      <div class="card chart-card">
        <h3 class="chart-title">Hourly Volume Comparison</h3>
        <div ref="hourlyVolumeChartRef" style="width: 100%; height: 350px;"></div>
      </div>

      <div class="card chart-card">
        <h3 class="chart-title">Liquidity Distribution</h3>
        <div ref="liquidityDistributionChartRef" style="width: 100%; height: 350px;"></div>
      </div>

      <div class="card chart-card full-width">
        <div class="chart-header">
          <h3 class="chart-title">Price Volatility Analysis</h3>
          <p class="chart-desc">Hourly price change percentage</p>
        </div>
        <div ref="volatilityChartRef" style="width: 100%; height: 350px;"></div>
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

const { t } = useI18n()
const dateRange = ref(['2025-09-01 00:00:00', '2025-09-30 23:59:59'])
const priceData = ref([])

const disabledDate = (time) => {
  const minDate = new Date('2025-09-01T00:00:00')
  const maxDate = new Date('2025-09-30T23:59:59')
  return time < minDate || time > maxDate
}

const hourlyVolumeChartRef = ref(null)
const liquidityDistributionChartRef = ref(null)
const liquidityTrendChartRef = ref(null)
const volatilityChartRef = ref(null)

let hourlyVolumeChart = null
let liquidityDistributionChart = null
let liquidityTrendChart = null
let volatilityChart = null

const avgVolumeBinance = computed(() => {
  if (priceData.value.length === 0) return 0
  const total = priceData.value.reduce((sum, item) => sum + (item.binance?.eth_volume || 0), 0)
  return total / priceData.value.length
})

const avgVolumeUniswap = computed(() => {
  if (priceData.value.length === 0) return 0
  const total = priceData.value.reduce((sum, item) => sum + (item.uniswap?.eth_volume || 0), 0)
  return total / priceData.value.length
})

const totalUsdtBinance = computed(() => {
  return priceData.value.reduce((sum, item) => sum + (item.binance?.usdt_volume || 0), 0)
})

const totalUsdtUniswap = computed(() => {
  return priceData.value.reduce((sum, item) => sum + (item.uniswap?.usdt_volume || 0), 0)
})

const maxVolumeBinance = computed(() => {
  return Math.max(...priceData.value.map(item => item.binance?.eth_volume || 0))
})

const maxVolumeUniswap = computed(() => {
  return Math.max(...priceData.value.map(item => item.uniswap?.eth_volume || 0))
})

const liquidityScoreBinance = computed(() => {
  if (priceData.value.length === 0) return 0
  const avgScore = Math.min(avgVolumeBinance.value / 10, 50)
  const maxScore = Math.min(maxVolumeBinance.value / 100, 50)
  return Math.round(avgScore + maxScore)
})

const liquidityScoreUniswap = computed(() => {
  if (priceData.value.length === 0) return 0
  const avgScore = Math.min(avgVolumeUniswap.value / 2, 50)
  const maxScore = Math.min(maxVolumeUniswap.value / 20, 50)
  return Math.round(avgScore + maxScore)
})

const formatNumber = (num) => {
  if (num >= 1000000) return (num / 1000000).toFixed(2) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(2) + 'K'
  return num.toFixed(2)
}

const fetchData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2) return
  
  const [start, end] = dateRange.value
  
  const liqData = await api.getLiquidityAnalysis(start, end, '1h')
  updateLiquidityTrendChart(liqData)
  
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
}

const initCharts = () => {
  if (hourlyVolumeChartRef.value) hourlyVolumeChart = echarts.init(hourlyVolumeChartRef.value)
  if (liquidityDistributionChartRef.value) liquidityDistributionChart = echarts.init(liquidityDistributionChartRef.value)
  if (liquidityTrendChartRef.value) liquidityTrendChart = echarts.init(liquidityTrendChartRef.value)
  if (volatilityChartRef.value) volatilityChart = echarts.init(volatilityChartRef.value)

  window.addEventListener('resize', () => {
    hourlyVolumeChart?.resize()
    liquidityDistributionChart?.resize()
    liquidityTrendChart?.resize()
    volatilityChart?.resize()
  })
}

const updateLiquidityTrendChart = (data) => {
  if (!liquidityTrendChart || !data || data.length === 0) return

  const times = data.map(item => item.time)
  const binanceLiq = data.map(item => item.binance_liquidity)
  const uniswapLiq = data.map(item => item.uniswap_liquidity)

  liquidityTrendChart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#E5E7EB',
      textStyle: { color: '#111827' }
    },
    legend: {
      data: ['Binance', 'Uniswap'],
      bottom: 0,
      icon: 'circle',
      textStyle: { color: '#6B7280' }
    },
    grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
    xAxis: {
      type: 'category',
      data: times,
      boundaryGap: false,
      axisLine: { lineStyle: { color: '#E5E7EB' } },
      axisLabel: { 
        color: '#9CA3AF',
        formatter: (value) => {
          const date = new Date(value)
          return `${date.getMonth() + 1}/${date.getDate()}`
        }
      },
      splitLine: { show: false }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#F3F4F6' } },
      axisLabel: { 
        color: '#9CA3AF',
        formatter: (value) => {
          if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M'
          if (value >= 1000) return (value / 1000).toFixed(1) + 'K'
          return value
        }
      }
    },
    series: [
      {
        name: 'Binance',
        type: 'line',
        data: binanceLiq,
        smooth: true,
        showSymbol: false,
        itemStyle: { color: '#F59E0B' },
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
        data: uniswapLiq,
        smooth: true,
        showSymbol: false,
        itemStyle: { color: '#EC4899' },
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

const updateCharts = () => {
  if (!priceData.value || priceData.value.length === 0) return

  const hourlyData = {}
  priceData.value.forEach(item => {
    const hour = new Date(item.time).getHours()
    if (!hourlyData[hour]) hourlyData[hour] = { binance: [], uniswap: [] }
    hourlyData[hour].binance.push(item.binance?.eth_volume || 0)
    hourlyData[hour].uniswap.push(item.uniswap?.eth_volume || 0)
  })

  const hours = Object.keys(hourlyData).sort((a, b) => a - b)
  const avgBinance = hours.map(h => {
    const arr = hourlyData[h].binance
    return arr.reduce((a, b) => a + b, 0) / arr.length
  })
  const avgUniswap = hours.map(h => {
    const arr = hourlyData[h].uniswap
    return arr.reduce((a, b) => a + b, 0) / arr.length
  })

  if (hourlyVolumeChart) {
    hourlyVolumeChart.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      legend: { bottom: 0, icon: 'circle' },
      grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
      xAxis: {
        type: 'category',
        data: hours.map(h => h + ':00'),
        axisLine: { lineStyle: { color: '#E5E7EB' } },
        axisLabel: { color: '#9CA3AF' }
      },
      yAxis: {
        type: 'value',
        splitLine: { lineStyle: { color: '#F3F4F6' } },
        axisLabel: { color: '#9CA3AF' }
      },
      series: [
        {
          name: 'Binance',
          type: 'bar',
          data: avgBinance,
          itemStyle: { color: '#F59E0B', borderRadius: [4, 4, 0, 0] }
        },
        {
          name: 'Uniswap',
          type: 'bar',
          data: avgUniswap,
          itemStyle: { color: '#EC4899', borderRadius: [4, 4, 0, 0] }
        }
      ]
    })
  }

  if (liquidityDistributionChart) {
    const ranges = [
      { label: '0-10', min: 0, max: 10 },
      { label: '10-50', min: 10, max: 50 },
      { label: '50-100', min: 50, max: 100 },
      { label: '100+', min: 100, max: Infinity }
    ]

    const distributionB = ranges.map(range => {
      return priceData.value.filter(item => {
        const vol = item.binance?.eth_volume || 0
        return vol >= range.min && vol < range.max
      }).length
    })

    const distributionU = ranges.map(range => {
      return priceData.value.filter(item => {
        const vol = item.uniswap?.eth_volume || 0
        return vol >= range.min && vol < range.max
      }).length
    })

    liquidityDistributionChart.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      legend: { bottom: 0, icon: 'circle' },
      grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
      xAxis: {
        type: 'category',
        data: ranges.map(r => r.label),
        axisLine: { lineStyle: { color: '#E5E7EB' } },
        axisLabel: { color: '#9CA3AF' }
      },
      yAxis: {
        type: 'value',
        splitLine: { lineStyle: { color: '#F3F4F6' } },
        axisLabel: { color: '#9CA3AF' }
      },
      series: [
        {
          name: 'Binance',
          type: 'bar',
          data: distributionB,
          itemStyle: { color: '#F59E0B', borderRadius: [4, 4, 0, 0] }
        },
        {
          name: 'Uniswap',
          type: 'bar',
          data: distributionU,
          itemStyle: { color: '#EC4899', borderRadius: [4, 4, 0, 0] }
        }
      ]
    })
  }

  // Volatility Chart
  if (volatilityChart && priceData.value.length > 1) {
    const volatilityData = []
    for (let i = 1; i < priceData.value.length; i++) {
      const prev = priceData.value[i - 1]
      const curr = priceData.value[i]
      
      const binanceChange = prev.binance?.price && curr.binance?.price
        ? ((curr.binance.price - prev.binance.price) / prev.binance.price) * 100
        : 0
      
      const uniswapChange = prev.uniswap?.price && curr.uniswap?.price
        ? ((curr.uniswap.price - prev.uniswap.price) / prev.uniswap.price) * 100
        : 0
      
      volatilityData.push({
        time: curr.time,
        binance: binanceChange,
        uniswap: uniswapChange
      })
    }
    
    const times = volatilityData.map(d => {
      const date = new Date(d.time)
      return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:00`
    })
    const binanceVol = volatilityData.map(d => d.binance.toFixed(4))
    const uniswapVol = volatilityData.map(d => d.uniswap.toFixed(4))
    
    volatilityChart.setOption({
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderColor: '#E5E7EB',
        textStyle: { color: '#111827' },
        formatter: (params) => {
          let result = params[0].axisValue + '<br/>'
          params.forEach(param => {
            result += `${param.seriesName}: ${param.value}%<br/>`
          })
          return result
        }
      },
      legend: {
        data: ['Binance', 'Uniswap'],
        bottom: 0,
        icon: 'circle',
        textStyle: { color: '#6B7280' }
      },
      grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
      xAxis: {
        type: 'category',
        data: times,
        boundaryGap: false,
        axisLine: { lineStyle: { color: '#E5E7EB' } },
        axisLabel: { 
          color: '#9CA3AF',
          rotate: 45
        },
        splitLine: { show: false }
      },
      yAxis: {
        type: 'value',
        splitLine: { lineStyle: { color: '#F3F4F6' } },
        axisLabel: { 
          color: '#9CA3AF',
          formatter: '{value}%'
        }
      },
      dataZoom: [
        {
          type: 'inside',
          start: 0,
          end: 100
        },
        {
          show: true,
          type: 'slider',
          top: '90%',
          height: 20,
          start: 0,
          end: 100
        }
      ],
      series: [
        {
          name: 'Binance',
          type: 'line',
          data: binanceVol,
          smooth: true,
          showSymbol: false,
          itemStyle: { color: '#F59E0B' },
          lineStyle: { width: 2 }
        },
        {
          name: 'Uniswap',
          type: 'line',
          data: uniswapVol,
          smooth: true,
          showSymbol: false,
          itemStyle: { color: '#EC4899' },
          lineStyle: { width: 2 }
        }
      ]
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
    margin-bottom: 4px;
  }
  
  .page-subtitle {
    font-size: 14px;
    color: var(--color-text-secondary);
  }
}

.liquidity-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.liquidity-card {
  padding: var(--spacing-lg);
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
    padding-bottom: var(--spacing-md);
    border-bottom: 1px solid var(--color-bg-primary);
    
    .platform-info {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .platform-icon {
        width: 32px;
        height: 32px;
      }
      
      h3 {
        font-size: 18px;
        font-weight: 600;
      }
    }
    
    .badge {
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      
      &.centralized {
        background: #FFFBEB;
        color: #F59E0B;
      }
      
      &.decentralized {
        background: #FCE7F3;
        color: #EC4899;
      }
    }
  }
  
  .metrics {
    display: flex;
    flex-direction: column;
    gap: 16px;
    
    .metric {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .label { color: var(--color-text-secondary); font-size: 14px; }
      .value { font-weight: 600; color: var(--color-text-primary); }
      
      .score-bar {
        position: relative;
        width: 120px;
        height: 20px;
        background: var(--color-bg-primary);
        border-radius: 10px;
        overflow: hidden;
        
        .score-fill {
          height: 100%;
          border-radius: 10px;
          
          &.binance { background: #F59E0B; }
          &.uniswap { background: #EC4899; }
        }
        
        .score-text {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
          font-size: 10px;
          font-weight: 600;
          color: var(--color-text-primary);
        }
      }
    }
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
  
  .chart-header {
    margin-bottom: var(--spacing-lg);
  }
  
  .chart-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 4px;
  }
  
  .chart-desc {
    font-size: 12px;
    color: var(--color-text-secondary);
  }
}
</style>
