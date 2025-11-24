<template>
  <div class="liquidity-analysis">
    <div class="header">
      <h2>市场流动性分析</h2>
      <p class="subtitle">对比 Binance 和 Uniswap 的市场深度与流动性</p>
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

    <!-- 流动性指标卡片 -->
    <div class="liquidity-cards">
      <div class="liquidity-card binance-card">
        <div class="card-header">
          <h3>Binance</h3>
          <span class="badge centralized">中心化交易所</span>
        </div>
        <div class="metrics">
          <div class="metric">
            <span class="label">平均每分钟交易量</span>
            <span class="value">{{ formatNumber(avgVolumeBinance) }} ETH</span>
          </div>
          <div class="metric">
            <span class="label">总交易金额</span>
            <span class="value">${{ formatNumber(totalUsdtBinance) }}</span>
          </div>
          <div class="metric">
            <span class="label">最大单笔交易</span>
            <span class="value">{{ formatNumber(maxVolumeBinance) }} ETH</span>
          </div>
          <div class="metric">
            <span class="label">流动性评分</span>
            <div class="score-bar">
              <div class="score-fill binance" :style="{ width: liquidityScoreBinance + '%' }"></div>
              <span class="score-text">{{ liquidityScoreBinance }}/100</span>
            </div>
          </div>
        </div>
      </div>

      <div class="liquidity-card uniswap-card">
        <div class="card-header">
          <h3>Uniswap V3</h3>
          <span class="badge decentralized">去中心化交易所</span>
        </div>
        <div class="metrics">
          <div class="metric">
            <span class="label">平均每分钟交易量</span>
            <span class="value">{{ formatNumber(avgVolumeUniswap) }} ETH</span>
          </div>
          <div class="metric">
            <span class="label">总交易金额</span>
            <span class="value">${{ formatNumber(totalUsdtUniswap) }}</span>
          </div>
          <div class="metric">
            <span class="label">最大单笔交易</span>
            <span class="value">{{ formatNumber(maxVolumeUniswap) }} ETH</span>
          </div>
          <div class="metric">
            <span class="label">流动性评分</span>
            <div class="score-bar">
              <div class="score-fill uniswap" :style="{ width: liquidityScoreUniswap + '%' }"></div>
              <span class="score-text">{{ liquidityScoreUniswap }}/100</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <div class="chart-card">
        <h3 class="chart-title">平均交易量对比（按小时）</h3>
        <div ref="hourlyVolumeChartRef" style="width: 100%; height: 400px;"></div>
      </div>

      <div class="chart-card">
        <h3 class="chart-title">流动性深度分布</h3>
        <p class="chart-desc">不同交易量级别的分布情况</p>
        <div ref="liquidityDistributionChartRef" style="width: 100%; height: 400px;"></div>
      </div>

      <div class="chart-card full-width">
        <h3 class="chart-title">价格波动与交易量关系</h3>
        <p class="chart-desc">交易量越大，价格越稳定（波动越小）</p>
        <div ref="volumePriceChartRef" style="width: 100%; height: 400px;"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { api } from '@/api'

const dateRange = ref([new Date('2025-09-01'), new Date('2025-09-30')])
const priceData = ref([])

const hourlyVolumeChartRef = ref(null)
const liquidityDistributionChartRef = ref(null)
const volumePriceChartRef = ref(null)

let hourlyVolumeChart = null
let liquidityDistributionChart = null
let volumePriceChart = null

// 计算流动性指标
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

// 流动性评分（基于交易量和稳定性）
const liquidityScoreBinance = computed(() => {
  if (priceData.value.length === 0) return 0
  // 综合考虑平均交易量和最大交易量
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
  const data = await api.getHistoricalPrices(
    start.toISOString().split('T')[0],
    end.toISOString().split('T')[0],
    10000
  )
  
  priceData.value = data
  updateCharts()
}

const initCharts = () => {
  if (hourlyVolumeChartRef.value) {
    hourlyVolumeChart = echarts.init(hourlyVolumeChartRef.value)
  }
  if (liquidityDistributionChartRef.value) {
    liquidityDistributionChart = echarts.init(liquidityDistributionChartRef.value)
  }
  if (volumePriceChartRef.value) {
    volumePriceChart = echarts.init(volumePriceChartRef.value)
  }

  window.addEventListener('resize', () => {
    hourlyVolumeChart?.resize()
    liquidityDistributionChart?.resize()
    volumePriceChart?.resize()
  })
}

const updateCharts = () => {
  if (priceData.value.length === 0) return

  // 按小时聚合数据
  const hourlyData = {}
  priceData.value.forEach(item => {
    const hour = new Date(item.time).getHours()
    if (!hourlyData[hour]) {
      hourlyData[hour] = { binance: [], uniswap: [] }
    }
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

  // 小时交易量图表
  if (hourlyVolumeChart) {
    hourlyVolumeChart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' }
      },
      legend: {
        data: ['Binance', 'Uniswap'],
        bottom: 10
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '12%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: hours.map(h => h + ':00'),
        name: '小时'
      },
      yAxis: {
        type: 'value',
        name: '平均 ETH 交易量'
      },
      series: [
        {
          name: 'Binance',
          type: 'bar',
          data: avgBinance,
          itemStyle: { color: '#f0b90b' }
        },
        {
          name: 'Uniswap',
          type: 'bar',
          data: avgUniswap,
          itemStyle: { color: '#ff007a' }
        }
      ]
    })
  }

  // 流动性分布图
  if (liquidityDistributionChart) {
    const ranges = [
      { label: '0-10 ETH', min: 0, max: 10 },
      { label: '10-50 ETH', min: 10, max: 50 },
      { label: '50-100 ETH', min: 50, max: 100 },
      { label: '100-500 ETH', min: 100, max: 500 },
      { label: '500+ ETH', min: 500, max: Infinity }
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
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' }
      },
      legend: {
        data: ['Binance', 'Uniswap'],
        bottom: 10
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '12%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: ranges.map(r => r.label),
        axisLabel: { rotate: 20 }
      },
      yAxis: {
        type: 'value',
        name: '交易次数'
      },
      series: [
        {
          name: 'Binance',
          type: 'bar',
          data: distributionB,
          itemStyle: { color: '#f0b90b' }
        },
        {
          name: 'Uniswap',
          type: 'bar',
          data: distributionU,
          itemStyle: { color: '#ff007a' }
        }
      ]
    })
  }

  // 价格波动与交易量关系
  if (volumePriceChart) {
    const scatterData = priceData.value.map(item => [
      item.binance?.eth_volume || 0,
      Math.abs(item.price_diff_percent || 0)
    ])

    volumePriceChart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: (params) => {
          return `交易量: ${params.value[0].toFixed(2)} ETH<br/>价格波动: ${params.value[1].toFixed(4)}%`
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
        name: '价格差异百分比 (%)',
        nameLocation: 'middle',
        nameGap: 50
      },
      series: [{
        type: 'scatter',
        data: scatterData,
        symbolSize: 6,
        itemStyle: {
          color: '#4CAF50',
          opacity: 0.5
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
.liquidity-analysis {
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

.liquidity-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.liquidity-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 2px solid #f0f0f0;

    h3 {
      margin: 0;
      font-size: 20px;
      color: #1a1a1a;
    }

    .badge {
      padding: 4px 12px;
      border-radius: 16px;
      font-size: 12px;
      font-weight: 600;

      &.centralized {
        background: #fff3e0;
        color: #f57c00;
      }

      &.decentralized {
        background: #fce4ec;
        color: #c2185b;
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

      .label {
        font-size: 13px;
        color: #666;
      }

      .value {
        font-size: 16px;
        font-weight: 600;
        color: #1a1a1a;
      }

      .score-bar {
        position: relative;
        width: 150px;
        height: 24px;
        background: #f0f0f0;
        border-radius: 12px;
        overflow: hidden;

        .score-fill {
          position: absolute;
          left: 0;
          top: 0;
          height: 100%;
          border-radius: 12px;
          transition: width 0.3s ease;

          &.binance {
            background: linear-gradient(90deg, #f0b90b, #f8d12f);
          }

          &.uniswap {
            background: linear-gradient(90deg, #ff007a, #ff4d9f);
          }
        }

        .score-text {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
          font-size: 12px;
          font-weight: 600;
          color: #1a1a1a;
          z-index: 1;
        }
      }
    }
  }
}

.charts-section {
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
