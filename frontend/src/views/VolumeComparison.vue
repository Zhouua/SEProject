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
          <span class="label">{{ t('volumeComparison.binanceVolume') }}</span>
          <span class="value">{{ formatNumber(totalVolumeBinance) }} ETH</span>
          <span class="sub-value">≈ ${{ formatNumber(totalUsdtBinance) }}</span>
        </div>
      </div>
      
      <div class="card stat-card">
        <div class="stat-icon uniswap"><PieChart :size="24" /></div>
        <div class="stat-content">
          <span class="label">{{ t('volumeComparison.uniswapVolume') }}</span>
          <span class="value">{{ formatNumber(totalVolumeUniswap) }} ETH</span>
          <span class="sub-value">≈ ${{ formatNumber(totalUsdtUniswap) }}</span>
        </div>
      </div>

      <div class="card stat-card">
        <div class="stat-icon ratio"><Percent :size="24" /></div>
        <div class="stat-content">
          <span class="label">{{ t('volumeComparison.volumeRatio') }}</span>
          <span class="value">{{ volumeRatio }}</span>
          <span class="sub-value">{{ t('volumeComparison.binanceUniswap') }}</span>
        </div>
      </div>
    </div>

    <!-- 流动性分析卡片 - 只显示DEX -->
    <div class="liquidity-cards">
      <div class="card liquidity-card">
        <div class="card-header">
          <div class="platform-info">
            <img src="https://cryptologos.cc/logos/uniswap-uni-logo.png" class="platform-icon" />
            <h3>Uniswap V3 Liquidity</h3>
          </div>
          <span class="badge decentralized">{{ t('liquidityAnalysis.dex') }}</span>
        </div>
        <div class="metrics">
          <div class="metric">
            <span class="label">{{ t('liquidityAnalysis.avgVolumePerMin') }}</span>
            <span class="value">{{ formatNumber(avgVolumeUniswap) }} ETH</span>
          </div>
          <div class="metric">
            <span class="label">{{ t('liquidityAnalysis.totalVolume') }}</span>
            <span class="value">${{ formatNumber(totalUsdtUniswap) }}</span>
          </div>
          <div class="metric">
            <span class="label">{{ t('liquidityAnalysis.liquidityScore') }}</span>
            <el-tooltip 
              effect="dark" 
              placement="top"
              popper-class="score-tooltip"
            >
              <template #content>
                <div class="tooltip-content">
                  <div class="tooltip-title">{{ t('liquidityAnalysis.scoreFormula') }}</div>
                  <div class="formula-item">
                    <span class="formula-label">{{ t('liquidityAnalysis.avgScore') }}:</span>
                    <span class="formula-value">min({{ t('liquidityAnalysis.avgVolumePerMin') }} / 10, 50)</span>
                  </div>
                  <div class="formula-item">
                    <span class="formula-label">{{ t('liquidityAnalysis.maxScore') }}:</span>
                    <span class="formula-value">min({{ t('liquidityAnalysis.maxVolume') }} / 100, 50)</span>
                  </div>
                  <div class="formula-divider"></div>
                  <div class="formula-item">
                    <span class="formula-label">{{ t('liquidityAnalysis.totalScore') }}:</span>
                    <span class="formula-value">{{ t('liquidityAnalysis.avgScore') }} + {{ t('liquidityAnalysis.maxScore') }}</span>
                  </div>
                </div>
              </template>
              <div class="score-bar">
                <div class="score-fill uniswap" :style="{ width: liquidityScoreUniswap + '%' }"></div>
                <span class="score-text">{{ liquidityScoreUniswap }}/100</span>
              </div>
            </el-tooltip>
          </div>
        </div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="card chart-card">
        <h3 class="card-title">{{ t('volumeComparison.ethVolumeComparison') }}</h3>
        <div ref="ethVolumeChartRef" style="width: 100%; height: 350px;"></div>
      </div>

      <div class="card chart-card">
        <h3 class="card-title">{{ t('volumeComparison.usdtVolumeComparison') }}</h3>
        <div ref="usdtVolumeChartRef" style="width: 100%; height: 350px;"></div>
      </div>

      <div class="card chart-card full-width">
        <h3 class="card-title">{{ t('volumeComparison.volumeCorrelation') }}</h3>
        <p class="chart-desc">{{ t('volumeComparison.volumeCorrelationDesc') }}</p>
        <div ref="volumeRatioChartRef" style="width: 100%; height: 350px;"></div>
      </div>
      
      <!-- 流动性分析图表 -->
      <div class="card chart-card full-width">
        <div class="chart-header">
          <h3 class="chart-title">{{ t('liquidityAnalysis.liquidityTrend') }}</h3>
          <p class="chart-desc">{{ t('liquidityAnalysis.liquidityTrendDesc') }}</p>
        </div>
        <div ref="liquidityTrendChartRef" style="width: 100%; height: 400px;"></div>
      </div>

      <div class="card chart-card">
        <h3 class="chart-title">{{ t('liquidityAnalysis.hourlyVolumeComparison') }}</h3>
        <div ref="hourlyVolumeChartRef" style="width: 100%; height: 350px;"></div>
      </div>

      <div class="card chart-card">
        <h3 class="chart-title">{{ t('liquidityAnalysis.liquidityDistribution') }}</h3>
        <div ref="liquidityDistributionChartRef" style="width: 100%; height: 350px;"></div>
      </div>

      <div class="card chart-card full-width">
        <div class="chart-header">
          <h3 class="chart-title">{{ t('liquidityAnalysis.priceVolatilityAnalysis') }}</h3>
          <p class="chart-desc">{{ t('liquidityAnalysis.priceVolatilityDesc') }}</p>
        </div>
        <div ref="volatilityChartRef" style="width: 100%; height: 350px;"></div>
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
const liquidityTrendChartRef = ref(null)
const hourlyVolumeChartRef = ref(null)
const liquidityDistributionChartRef = ref(null)
const volatilityChartRef = ref(null)

let ethVolumeChart = null
let usdtVolumeChart = null
let volumeRatioChart = null
let liquidityTrendChart = null
let hourlyVolumeChart = null
let liquidityDistributionChart = null
let volatilityChart = null

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

// 流动性分析computed属性
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

const loading = ref(false)

const fetchData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2) return
  
  loading.value = true
  
  // 延迟 50ms，确保 loading 动画能显示
  await new Promise(resolve => setTimeout(resolve, 50))
  
  try {
    const [start, end] = dateRange.value
    
    // 获取流动性分析数据
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
  if (liquidityTrendChartRef.value) liquidityTrendChart = echarts.init(liquidityTrendChartRef.value)
  if (hourlyVolumeChartRef.value) hourlyVolumeChart = echarts.init(hourlyVolumeChartRef.value)
  if (liquidityDistributionChartRef.value) liquidityDistributionChart = echarts.init(liquidityDistributionChartRef.value)
  if (volatilityChartRef.value) volatilityChart = echarts.init(volatilityChartRef.value)

  window.addEventListener('resize', () => {
    ethVolumeChart?.resize()
    usdtVolumeChart?.resize()
    volumeRatioChart?.resize()
    liquidityTrendChart?.resize()
    hourlyVolumeChart?.resize()
    liquidityDistributionChart?.resize()
    volatilityChart?.resize()
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
          name: t('volumeComparison.binance'),
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
          name: t('volumeComparison.uniswap'),
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
          name: t('volumeComparison.binance'),
          type: 'bar',
          data: usdtBinance,
          itemStyle: { color: '#F59E0B' }
        },
        {
          name: t('volumeComparison.uniswap'),
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
  
  // 流动性分析图表更新
  updateLiquidityCharts()
}

// 流动性趋势图表
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
      data: [t('liquidityAnalysis.binance'), t('liquidityAnalysis.uniswap')],
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
        name: t('liquidityAnalysis.uniswap'),
        type: 'line',
        data: uniswapLiq,
        smooth: true,
        showSymbol: false,
        itemStyle: { color: '#8B5CF6' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(139, 92, 246, 0.3)' },
            { offset: 1, color: 'rgba(139, 92, 246, 0)' }
          ])
        }
      }
    ]
  })
}

// 更新流动性分析图表
const updateLiquidityCharts = () => {
  if (!priceData.value || priceData.value.length === 0) return

  // 每小时交易量对比 - 仅DEX
  const hourlyData = {}
  priceData.value.forEach(item => {
    const hour = new Date(item.time).getHours()
    if (!hourlyData[hour]) hourlyData[hour] = { uniswap: [] }
    hourlyData[hour].uniswap.push(item.uniswap?.eth_volume || 0)
  })

  const hours = Object.keys(hourlyData).sort((a, b) => a - b)
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
          name: t('liquidityAnalysis.uniswap'),
          type: 'bar',
          data: avgUniswap,
          itemStyle: { 
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#10B981' },
              { offset: 1, color: '#34D399' }
            ]),
            borderRadius: [4, 4, 0, 0] 
          }
        }
      ]
    })
  }

  // 流动性分布 - 仅DEX
  if (liquidityDistributionChart) {
    const ranges = [
      { label: '0-10', min: 0, max: 10 },
      { label: '10-50', min: 10, max: 50 },
      { label: '50-100', min: 50, max: 100 },
      { label: '100+', min: 100, max: Infinity }
    ]

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
          name: t('liquidityAnalysis.uniswap'),
          type: 'bar',
          data: distributionU,
          itemStyle: { 
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#3B82F6' },
              { offset: 1, color: '#60A5FA' }
            ]),
            borderRadius: [4, 4, 0, 0] 
          }
        }
      ]
    })
  }

  // 价格波动性 - 仅DEX
  if (volatilityChart && priceData.value.length > 1) {
    const volatilityData = []
    for (let i = 1; i < priceData.value.length; i++) {
      const prev = priceData.value[i - 1]
      const curr = priceData.value[i]
      
      const uniswapChange = prev.uniswap?.price && curr.uniswap?.price
        ? ((curr.uniswap.price - prev.uniswap.price) / prev.uniswap.price) * 100
        : 0
      
      volatilityData.push({
        time: curr.time,
        uniswap: uniswapChange
      })
    }
    
    const times = volatilityData.map(d => {
      const date = new Date(d.time)
      return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:00`
    })
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
        data: [t('liquidityAnalysis.uniswap')],
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
          name: t('liquidityAnalysis.uniswap'),
          type: 'line',
          data: uniswapVol,
          smooth: true,
          showSymbol: false,
          itemStyle: { color: '#EC4899' },
          lineStyle: { width: 2 },
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
  
  .chart-header {
    margin-bottom: var(--spacing-lg);
  }
  
  .card-title,
  .chart-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 4px;
  }
  
  .chart-desc {
    font-size: 12px;
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-lg);
  }
}

// 流动性分析样式 - 单列显示
.liquidity-cards {
  display: grid;
  grid-template-columns: 1fr;
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
        cursor: help;
        
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

// Tooltip样式
:deep(.score-tooltip) {
  max-width: 400px;
  
  .tooltip-content {
    padding: 4px;
    
    .tooltip-title {
      font-size: 14px;
      font-weight: 600;
      margin-bottom: 12px;
      color: #fff;
    }
    
    .formula-item {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
      font-size: 12px;
      
      .formula-label {
        color: #E5E7EB;
        margin-right: 12px;
        white-space: nowrap;
      }
      
      .formula-value {
        color: #fff;
        font-family: 'Monaco', 'Courier New', monospace;
        text-align: right;
      }
    }
    
    .formula-divider {
      height: 1px;
      background: rgba(255, 255, 255, 0.2);
      margin: 8px 0;
    }
  }
}
</style>
