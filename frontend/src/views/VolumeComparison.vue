<template>
  <div class="volume-comparison">
    <div class="header">
      <h2>交易量对比分析</h2>
      <p class="subtitle">对比 Binance 和 Uniswap 的 ETH 和 USDT 交易量</p>
      <div class="controls">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          :default-value="[new Date('2025-09-01'), new Date('2025-09-30')]"
          @change="fetchData"
        />
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon binance">
          <el-icon><TrendCharts /></el-icon>
        </div>
        <div class="stat-content">
          <p class="stat-label">Binance 总交易量</p>
          <h3 class="stat-value">{{ formatNumber(totalVolumeBinance) }} ETH</h3>
          <p class="stat-sub">≈ ${{ formatNumber(totalUsdtBinance) }}</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon uniswap">
          <el-icon><DataAnalysis /></el-icon>
        </div>
        <div class="stat-content">
          <p class="stat-label">Uniswap 总交易量</p>
          <h3 class="stat-value">{{ formatNumber(totalVolumeUniswap) }} ETH</h3>
          <p class="stat-sub">≈ ${{ formatNumber(totalUsdtUniswap) }}</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon ratio">
          <el-icon><Histogram /></el-icon>
        </div>
        <div class="stat-content">
          <p class="stat-label">交易量比率</p>
          <h3 class="stat-value">{{ volumeRatio }}</h3>
          <p class="stat-sub">Binance / Uniswap</p>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-grid">
      <!-- ETH 交易量对比 -->
      <div class="chart-card">
        <h3 class="chart-title">ETH 交易量对比</h3>
        <div ref="ethVolumeChartRef" style="width: 100%; height: 350px;"></div>
      </div>

      <!-- USDT 交易量对比 -->
      <div class="chart-card">
        <h3 class="chart-title">USDT 交易量对比</h3>
        <div ref="usdtVolumeChartRef" style="width: 100%; height: 350px;"></div>
      </div>

      <!-- 交易量比率图 -->
      <div class="chart-card full-width">
        <h3 class="chart-title">ETH vs USDT 交易量关系</h3>
        <p class="chart-desc">展示每笔交易中 ETH 数量与 USDT 金额的关系（应该成正比）</p>
        <div ref="volumeRatioChartRef" style="width: 100%; height: 350px;"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { api } from '@/api'
import { TrendCharts, DataAnalysis, Histogram } from '@element-plus/icons-vue'

const dateRange = ref([new Date('2025-09-01'), new Date('2025-09-30')])
const priceData = ref([])

const ethVolumeChartRef = ref(null)
const usdtVolumeChartRef = ref(null)
const volumeRatioChartRef = ref(null)

let ethVolumeChart = null
let usdtVolumeChart = null
let volumeRatioChart = null

// 计算总交易量
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

const fetchData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2) return
  
  const [start, end] = dateRange.value
  const data = await api.getHistoricalPrices(
    start.toISOString().split('T')[0],
    end.toISOString().split('T')[0],
    10000
  )
  
  priceData.value = data
  updateCharts()
}

const initCharts = () => {
  if (ethVolumeChartRef.value) {
    ethVolumeChart = echarts.init(ethVolumeChartRef.value)
  }
  if (usdtVolumeChartRef.value) {
    usdtVolumeChart = echarts.init(usdtVolumeChartRef.value)
  }
  if (volumeRatioChartRef.value) {
    volumeRatioChart = echarts.init(volumeRatioChartRef.value)
  }

  window.addEventListener('resize', () => {
    ethVolumeChart?.resize()
    usdtVolumeChart?.resize()
    volumeRatioChart?.resize()
  })
}

const updateCharts = () => {
  if (priceData.value.length === 0) return

  const times = priceData.value.map(item => item.time)
  const ethBinance = priceData.value.map(item => item.binance?.eth_volume || 0)
  const ethUniswap = priceData.value.map(item => item.uniswap?.eth_volume || 0)
  const usdtBinance = priceData.value.map(item => item.binance?.usdt_volume || 0)
  const usdtUniswap = priceData.value.map(item => item.uniswap?.usdt_volume || 0)

  // ETH 交易量图表
  if (ethVolumeChart) {
    ethVolumeChart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross' }
      },
      legend: {
        data: ['Binance', 'Uniswap'],
        bottom: 10
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: times,
        axisLabel: {
          rotate: 45,
          formatter: (value) => {
            const date = new Date(value)
            return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
          }
        }
      },
      yAxis: {
        type: 'value',
        name: 'ETH 数量',
        axisLabel: {
          formatter: '{value}'
        }
      },
      series: [
        {
          name: 'Binance',
          type: 'line',
          data: ethBinance,
          smooth: true,
          lineStyle: { color: '#f0b90b', width: 2 },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(240, 185, 11, 0.3)' },
              { offset: 1, color: 'rgba(240, 185, 11, 0.05)' }
            ])
          }
        },
        {
          name: 'Uniswap',
          type: 'line',
          data: ethUniswap,
          smooth: true,
          lineStyle: { color: '#ff007a', width: 2 },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(255, 0, 122, 0.3)' },
              { offset: 1, color: 'rgba(255, 0, 122, 0.05)' }
            ])
          }
        }
      ]
    })
  }

  // USDT 交易量图表
  if (usdtVolumeChart) {
    usdtVolumeChart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross' }
      },
      legend: {
        data: ['Binance', 'Uniswap'],
        bottom: 10
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: times,
        axisLabel: {
          rotate: 45,
          formatter: (value) => {
            const date = new Date(value)
            return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
          }
        }
      },
      yAxis: {
        type: 'value',
        name: 'USDT 金额',
        axisLabel: {
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
          type: 'bar',
          data: usdtBinance,
          itemStyle: { color: '#f0b90b' }
        },
        {
          name: 'Uniswap',
          type: 'bar',
          data: usdtUniswap,
          itemStyle: { color: '#ff007a' }
        }
      ]
    })
  }

  // 交易量关系散点图
  if (volumeRatioChart) {
    const scatterData = priceData.value.map(item => [
      item.binance?.eth_volume || 0,
      item.binance?.usdt_volume || 0
    ])

    volumeRatioChart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: (params) => {
          return `ETH: ${params.value[0].toFixed(2)}<br/>USDT: ${params.value[1].toFixed(2)}`
        }
      },
      grid: {
        left: '10%',
        right: '10%',
        bottom: '10%',
        top: '10%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        name: 'ETH 交易量',
        nameLocation: 'middle',
        nameGap: 30
      },
      yAxis: {
        type: 'value',
        name: 'USDT 交易量',
        nameLocation: 'middle',
        nameGap: 50,
        axisLabel: {
          formatter: (value) => {
            if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M'
            if (value >= 1000) return (value / 1000).toFixed(1) + 'K'
            return value
          }
        }
      },
      series: [{
        type: 'scatter',
        data: scatterData,
        symbolSize: 8,
        itemStyle: {
          color: '#4CAF50',
          opacity: 0.6
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
.volume-comparison {
  padding: 20px;
}

.header {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;

  h2 {
    margin: 0 0 8px 0;
    font-size: 24px;
    color: #1a1a1a;
  }

  .subtitle {
    margin: 0 0 16px 0;
    color: #666;
    font-size: 14px;
  }
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 16px;

  .stat-icon {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: white;

    &.binance {
      background: linear-gradient(135deg, #f0b90b 0%, #f8d12f 100%);
    }

    &.uniswap {
      background: linear-gradient(135deg, #ff007a 0%, #ff4d9f 100%);
    }

    &.ratio {
      background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
    }
  }

  .stat-content {
    flex: 1;

    .stat-label {
      margin: 0 0 4px 0;
      font-size: 13px;
      color: #999;
    }

    .stat-value {
      margin: 0 0 4px 0;
      font-size: 22px;
      font-weight: 700;
      color: #1a1a1a;
    }

    .stat-sub {
      margin: 0;
      font-size: 12px;
      color: #666;
    }
  }
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;

  .chart-card {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

    &.full-width {
      grid-column: 1 / -1;
    }

    .chart-title {
      margin: 0 0 8px 0;
      font-size: 16px;
      font-weight: 600;
      color: #1a1a1a;
    }

    .chart-desc {
      margin: 0 0 16px 0;
      font-size: 13px;
      color: #666;
    }
  }
}
</style>
