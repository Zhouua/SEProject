<template>
  <div class="price-comparison">
    <div class="header">
      <h2>{{ t('priceComparison.title') }}</h2>
      <div class="controls">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="To"
          start-placeholder="Start date"
          end-placeholder="End date"
          :default-value="[new Date('2025-09-01'), new Date('2025-09-30')]"
          @change="fetchData"
        />
      </div>
    </div>

    <div class="chart-container">
      <div ref="chartRef" style="width: 100%; height: 500px;"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts'
import { api } from '@/api'

const { t } = useI18n()
const chartRef = ref(null)
let chart = null
const dateRange = ref([new Date('2025-09-01'), new Date('2025-09-30')])

const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    window.addEventListener('resize', () => chart.resize())
  }
}

const fetchData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2) return
  
  const [start, end] = dateRange.value
  const data = await api.getHistoricalPrices(start, end)
  updateChart(data)
}

const updateChart = (data) => {
  if (!chart) return

  const dates = data.map(item => item.date)
  const uniswapPrices = data.map(item => item.uniswap)
  const binancePrices = data.map(item => item.binance)

  const option = {
    title: {
      text: 'USDT/ETH Price Comparison',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['Uniswap V3', 'Binance'],
      bottom: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates
    },
    yAxis: {
      type: 'value',
      scale: true // Better for showing price differences
    },
    series: [
      {
        name: 'Uniswap V3',
        type: 'line',
        data: uniswapPrices,
        smooth: true,
        lineStyle: { color: '#ff007a' } // Uniswap pink
      },
      {
        name: 'Binance',
        type: 'line',
        data: binancePrices,
        smooth: true,
        lineStyle: { color: '#f0b90b' } // Binance yellow
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
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-container {
  margin-top: 20px;
}
</style>
