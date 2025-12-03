<template>
  <div class="page-container">
    <TruckLoader :show="loading" text="加载图表数据中..." />
    <div class="card chart-card">
      <div class="chart-info-bar">
        <div class="chart-description">
          <span class="desc-text">{{ t('chart.candlestickInfo') || 'Candlestick chart with volume indicators' }}</span>
        </div>
      </div>
      <div ref="chartRef" style="width: 100%; height: 700px;"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts'
import { api } from '@/api'
import TruckLoader from '@/components/TruckLoader.vue'

const { t } = useI18n()
const chartRef = ref(null)
let chart = null

const dateRange = ref(['2025-09-01 00:00:00', '2025-09-30 23:59:59'])
const interval = ref('4h')
const loading = ref(false)

const disabledDate = (time) => {
  const minDate = new Date('2025-09-01T00:00:00')
  const maxDate = new Date('2025-09-30T23:59:59')
  return time < minDate || time > maxDate
}

const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    window.addEventListener('resize', () => chart.resize())
  }
}

const fetchData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2) return
  
  loading.value = true
  try {
    const [start, end] = dateRange.value
    const data = await api.getPriceCandles(start, end, interval.value)
    updateChart(data)
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    loading.value = false
  }
}

const updateChart = (data) => {
  if (!chart || !data) return
  
  const dates = data.map(item => item.time)
  
  const binanceData = data.map(item => [
    item.binance.open,
    item.binance.close,
    item.binance.low,
    item.binance.high
  ])
  
  const uniswapData = data.map(item => [
    item.uniswap.open,
    item.uniswap.close,
    item.uniswap.low,
    item.uniswap.high
  ])
  
  const binanceVolume = data.map(item => item.binance.usdt_volume || 0)
  const uniswapVolume = data.map(item => item.uniswap.usdt_volume || 0)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { 
        type: 'cross',
        link: [{ xAxisIndex: 'all' }],
        label: { backgroundColor: '#6a7985' } 
      },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E5E7EB',
      borderWidth: 1,
      textStyle: { color: '#111827', fontSize: 12 },
      formatter: function(params) {
        let result = params[0].axisValue + '<br/>'
        params.forEach(param => {
          if (param.seriesType === 'candlestick') {
            const data = param.data
            result += `<div style="margin: 4px 0;">
              <strong>${param.seriesName}</strong><br/>
              Open: $${data[1]}<br/>
              Close: $${data[2]}<br/>
              Low: $${data[3]}<br/>
              High: $${data[4]}
            </div>`
          } else if (param.seriesType === 'bar') {
            result += `${param.marker} ${param.seriesName}: ${param.value.toLocaleString()} USDT<br/>`
          }
        })
        return result
      }
    },
    legend: {
      data: ['Binance', 'Uniswap', 'Binance Volume', 'Uniswap Volume'],
      top: 10,
      right: 30,
      orient: 'horizontal',
      icon: 'circle',
      itemGap: 24,
      textStyle: { color: '#6B7280', fontSize: 12 }
    },
    axisPointer: {
      link: [{ xAxisIndex: 'all' }]
    },
    grid: [
      {
        left: '3%',
        right: '3%',
        top: '10%',
        height: '55%',
        containLabel: true
      },
      {
        left: '3%',
        right: '3%',
        top: '72%',
        height: '18%',
        containLabel: true
      }
    ],
    xAxis: [
      {
        type: 'category',
        data: dates,
        scale: true,
        boundaryGap: true,
        axisLine: { lineStyle: { color: '#E5E7EB' } },
        axisLabel: { 
          color: '#9CA3AF',
          formatter: (value) => {
            const date = new Date(value)
            return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
          }
        },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax'
      },
      {
        type: 'category',
        gridIndex: 1,
        data: dates,
        scale: true,
        boundaryGap: true,
        axisLine: { lineStyle: { color: '#E5E7EB' } },
        axisLabel: { 
          color: '#9CA3AF',
          formatter: (value) => {
            const date = new Date(value)
            return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
          }
        },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax'
      }
    ],
    yAxis: [
      {
        scale: true,
        splitLine: { lineStyle: { color: '#F3F4F6' } },
        axisLabel: { 
          color: '#9CA3AF',
          formatter: '${value}'
        }
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        splitLine: { lineStyle: { color: '#F3F4F6' } },
        axisLabel: { 
          color: '#9CA3AF',
          formatter: (value) => {
            if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M'
            if (value >= 1000) return (value / 1000).toFixed(1) + 'K'
            return value
          }
        }
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 0,
        end: 100
      },
      {
        show: true,
        xAxisIndex: [0, 1],
        type: 'slider',
        bottom: '2%',
        height: 20,
        start: 0,
        end: 100,
        borderColor: 'transparent',
        backgroundColor: '#F3F4F6',
        fillerColor: 'rgba(16, 185, 129, 0.2)',
        handleStyle: {
          color: '#10B981',
          shadowBlur: 3,
          shadowColor: 'rgba(0, 0, 0, 0.1)',
          shadowOffsetX: 2,
          shadowOffsetY: 2
        }
      }
    ],
    series: [
      {
        name: 'Binance',
        type: 'candlestick',
        data: binanceData,
        itemStyle: {
          color: '#10B981',
          color0: '#EF4444',
          borderColor: '#10B981',
          borderColor0: '#EF4444'
        },
        barMaxWidth: 10
      },
      {
        name: 'Uniswap',
        type: 'candlestick',
        data: uniswapData,
        itemStyle: {
          color: '#3B82F6',
          color0: '#F59E0B',
          borderColor: '#3B82F6',
          borderColor0: '#F59E0B'
        },
        barMaxWidth: 10
      },
      {
        name: 'Binance Volume',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: binanceVolume,
        itemStyle: {
          color: 'rgba(16, 185, 129, 0.3)'
        },
        barMaxWidth: 8
      },
      {
        name: 'Uniswap Volume',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: uniswapVolume,
        itemStyle: {
          color: 'rgba(59, 130, 246, 0.3)'
        },
        barMaxWidth: 8
      }
    ]
  }

  chart.setOption(option)
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
  position: relative;
}

.chart-card {
  padding: var(--spacing-xl);
  height: auto;
}

.chart-info-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  padding: 0 var(--spacing-lg);
  
  .chart-description {
    .desc-text {
      font-size: 12px;
      color: var(--color-text-secondary);
      font-style: italic;
    }
  }
}
</style>
