<template>
  <div class="price-comparison">
    <div class="header">
      <h2>{{ t('sidebar.priceComparison.title') }}</h2>
      <div class="controls">
        <el-radio-group v-model="interval" size="small" @change="fetchData">
          <el-radio-button label="1h">1H</el-radio-button>
          <el-radio-button label="4h">4H</el-radio-button>
          <el-radio-button label="1d">1D</el-radio-button>
        </el-radio-group>
        <el-date-picker
          v-model="dateRange"
          type="datetimerange"
          range-separator="至"
          start-placeholder="开始时间"
          end-placeholder="结束时间"
          :default-value="['2025-09-01 00:00:00', '2025-09-30 23:59:59']"
          :disabled-date="disabledDate"
          value-format="YYYY-MM-DD HH:mm:ss"
          @change="fetchData"
        />
      </div>
    </div>

    <div class="chart-container" v-loading="loading">
      <div ref="chartRef" style="width: 100%; height: 600px;"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts'
import { api } from '@/api'

const { t } = useI18n()
const chartRef = ref(null)
let chart = null

const dateRange = ref(['2025-09-01 00:00:00', '2025-09-30 23:59:59'])
const interval = ref('4h') // Default to 4H for better view
const loading = ref(false)

// 限制日期选择范围：只允许 2025-09-01 至 2025-09-30
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
    // Use getPriceCandles instead of getHistoricalPrices
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
  
  // Prepare Candlestick Data: [Open, Close, Low, High]
  // Note: ECharts K-line expects [Open, Close, Lowest, Highest]
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

  const option = {
    title: {
      text: 'Price Comparison (Candlestick)',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['Binance', 'Uniswap'],
      bottom: 10
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%'
    },
    xAxis: {
      type: 'category',
      data: dates,
      scale: true,
      boundaryGap: false,
      axisLine: { onZero: false },
      splitLine: { show: false },
      min: 'dataMin',
      max: 'dataMax'
    },
    yAxis: {
      scale: true,
      splitArea: {
        show: true
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
        start: 0,
        end: 100
      }
    ],
    series: [
      {
        name: 'Binance',
        type: 'candlestick',
        data: binanceData,
        itemStyle: {
          color: '#ec0000',
          color0: '#00da3c',
          borderColor: '#8A0000',
          borderColor0: '#008F28'
        }
      },
      {
        name: 'Uniswap',
        type: 'candlestick',
        data: uniswapData,
        itemStyle: {
          color: '#eb5454',
          color0: '#47b262',
          borderColor: '#eb5454',
          borderColor0: '#47b262'
        }
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

<style scoped>
.price-comparison {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.controls {
  display: flex;
  gap: 16px;
  align-items: center;
}

.chart-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}
</style>
