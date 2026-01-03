<template>
  <div class="page-container">
    <TruckLoader :show="loading" text="Loading Market Data..." />
    
    <!-- Ticker Header -->
    <div class="ticker-header card">
      <div class="asset-info">
        <div class="asset-icon">
          <img :src="headerInfo.logo" :alt="headerInfo.name" />
        </div>
        <div class="asset-names">
          <div class="asset-symbol">{{ headerInfo.symbol }}</div>
          <div class="asset-name">{{ headerInfo.name }}</div>
        </div>
      </div>
      
      <div class="ticker-stats">
        
        <!-- Binance Stat -->
        <div class="stat-card" v-if="exchangeFilter !== 'uniswap'">
          <div class="stat-label">Binance Price</div>
          <div class="stat-value text-binance">
            ${{ formatPrice(latestData?.binance?.close) }}
            <span class="change-badge" :class="getChange(latestData?.binance) >= 0 ? 'bg-green' : 'bg-red'">
               {{ getChange(latestData?.binance) }}%
            </span>
          </div>
        </div>

        <!-- Uniswap Stat -->
        <div class="stat-card" v-if="exchangeFilter !== 'binance'">
          <div class="stat-label">Uniswap Price</div>
          <div class="stat-value text-uniswap">
            ${{ formatPrice(latestData?.uniswap?.close) }}
            <span class="change-badge" :class="getChange(latestData?.uniswap) >= 0 ? 'bg-green' : 'bg-red'">
               {{ getChange(latestData?.uniswap) }}%
            </span>
          </div>
        </div>

        <!-- Spread / Arb Signal -->
        <div class="stat-card highlight" v-if="exchangeFilter === 'both'">
          <div class="stat-label">Arbitrage Spread</div>
          <div class="stat-main">
             <span class="spread-percent" :class="latestSpreadPercent > 0.5 ? 'text-up' : 'text-neutral'">
                {{ latestSpreadPercent }}%
             </span>
             <span class="spread-value">(${{ formatPrice(Math.abs(latestSpread)) }})</span>
          </div>
          <div class="arb-signal" v-if="Math.abs(latestSpreadPercent) > 0.1">
             <span class="signal-tag">{{ arbDirection }}</span>
          </div>
        </div>

        <!-- Volume -->
        <div class="stat-card">
          <div class="stat-label">24h Volume (USDT)</div>
          <div class="stat-value">{{ formatVolume(latestData?.binance?.usdt_volume) }}</div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="main-layout">
      <!-- Left: Chart Section -->
      <div class="left-section">
        <div class="card chart-card">
          <div class="chart-header">
             <div class="chart-tabs">
               <div class="tab-item active">Price Chart</div>
               <div class="tab-item">Depth</div>
             </div>
             
             <div class="time-controls">
                <span 
                  v-for="t in ['1H', '4H', '1D', '1W']" 
                  :key="t"
                  class="time-btn" 
                  :class="{ active: interval === t.toLowerCase() }"
                  @click="changeInterval(t.toLowerCase())"
                >
                  {{ t }}
                </span>
             </div>
          </div>
          
          <div class="chart-container">
             <div ref="chartRef" style="width: 100%; height: 500px;"></div>
          </div>
          
          <div class="chart-controls-footer">
             <el-radio-group v-model="exchangeFilter" size="small" @change="updateChart">
                <el-radio-button label="binance">Binance</el-radio-button>
                <el-radio-button label="uniswap">Uniswap</el-radio-button>
                <el-radio-button label="both">Compare Both</el-radio-button>
              </el-radio-group>
              
              <div class="nav-controls">
                 <el-button link :icon="ArrowLeft" @click="navigateDays(-7)" :disabled="currentStartIndex <= 0" />
                 <span class="date-range">{{ displayDateRange }}</span>
                 <el-button link :icon="ArrowRight" @click="navigateDays(7)" :disabled="currentStartIndex + windowSize >= allRawData.length" />
              </div>
          </div>
        </div>
      </div>

      <!-- Right: Order Book -->
      <div class="right-section">
        <div class="card order-book-card">
          <div class="card-header">
            <h3 class="title">Order Book</h3>
          </div>
          
          <div class="order-book-header">
            <div class="col">Price(USDT)</div>
            <div class="col text-right">Vol(USDT)</div>
            <div class="col text-right">Spread</div>
          </div>
          
          <div class="order-book-list" ref="orderBookRef">
             <div 
               v-for="(item, index) in getCurrentWindowData" 
               :key="index"
               class="order-row"
               :class="{ 'selected': selectedData && selectedData.time === item.time }"
               @click="selectRow(item)"
               :id="'row-' + item.time.replace(/[: ]/g, '-')"
             >
                <div class="col price-col" :class="item.binance.close >= item.binance.open ? 'text-up' : 'text-down'">
                  {{ formatPrice(item.binance.close) }}
                </div>
                <div class="col text-right vol-col">
                  {{ formatVolumeShort(item.binance.usdt_volume) }}
                </div>
                <div class="col text-right spread-col">
                  {{ (Math.abs(item.binance.close - item.uniswap.close)).toFixed(2) }}
                </div>
             </div>
          </div>
          
          <div class="order-stats" v-if="selectedData">
             <div class="stat-row">
                <span>Selected Time</span>
                <span class="mono">{{ formatTime(selectedData.time) }}</span>
             </div>
             <div class="stat-divider"></div>
             <div class="stat-row" v-if="exchangeFilter !== 'uniswap'">
                <span>Binance</span>
                <span class="mono">${{ formatPrice(selectedData.binance.close) }}</span>
             </div>
             <div class="stat-row" v-if="exchangeFilter !== 'binance'">
                <span>Uniswap</span>
                <span class="mono contrast">${{ formatPrice(selectedData.uniswap.close) }}</span>
             </div>
             <div class="arb-opportunity" v-if="exchangeFilter === 'both' && Math.abs(selectedData.binance.close - selectedData.uniswap.close) > 10">
                Arbitrage Opportunity Detected
             </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, onUnmounted, computed } from 'vue'
import * as echarts from 'echarts'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { api } from '@/api'
import TruckLoader from '@/components/TruckLoader.vue'

const chartRef = ref(null)
const orderBookRef = ref(null)
let chart = null

const loading = ref(false)
const exchangeFilter = ref('both')
const selectedData = ref(null)
let allRawData = []
const interval = ref('4h')

const currentStartIndex = ref(0)
const windowSize = computed(() => Math.ceil(7 * 24 / 4)) // Approx 7 days

// Header Info Computed
const headerInfo = computed(() => {
  if (exchangeFilter.value === 'binance') {
    return {
      symbol: 'BNB/USDT',
      name: 'Binance Data',
      logo: 'https://cryptologos.cc/logos/binance-coin-bnb-logo.png'
    }
  } else if (exchangeFilter.value === 'uniswap') {
    return {
      symbol: 'UNI/USDT',
      name: 'Uniswap Data',
      logo: 'https://cryptologos.cc/logos/uniswap-uni-logo.png'
    }
  } else {
    return {
      symbol: 'BTC/USDT',
      name: 'Bitcoin (Comparison)',
      logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png'
    }
  }
})

const latestData = computed(() => allRawData[allRawData.length - 1] || {})
const latestSpread = computed(() => {
    if(!latestData.value.binance) return 0
    return latestData.value.binance.close - latestData.value.uniswap.close
})
const latestSpreadPercent = computed(() => {
    if(!latestData.value.binance) return '0.00'
    return Math.abs(((latestSpread.value / latestData.value.binance.close) * 100)).toFixed(2)
})

const arbDirection = computed(() => {
    if (latestSpread.value > 0) {
        return "Buy Uniswap → Sell Binance" // Binance is higher, so buy low (Uni) sell high (Bin)
    } else {
        return "Buy Binance → Sell Uniswap" // Uniswap is higher
    }
})

const getChange = (candle) => {
    if(!candle) return '0.00'
    // Simple calc: (Close - Open) / Open
    return ((candle.close - candle.open) / candle.open * 100).toFixed(2)
}

const displayDateRange = computed(() => {
  if (!allRawData.length) return '-'
  const startIdx = currentStartIndex.value
  const endIdx = Math.min(startIdx + windowSize.value, allRawData.length) - 1
  if (endIdx < 0) return '-'
  const startDate = allRawData[startIdx]?.time?.split(' ')[0] || '-'
  const endDate = allRawData[endIdx]?.time?.split(' ')[0] || '-'
  return `${startDate} ~ ${endDate}`
})

const getCurrentWindowData = computed(() => {
  const startIdx = currentStartIndex.value
  const endIdx = Math.min(startIdx + windowSize.value, allRawData.length)
  return allRawData.slice(startIdx, endIdx).reverse()
})

const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    window.addEventListener('resize', () => chart.resize())
    chart.on('click', (params) => {
      const startIdx = currentStartIndex.value
      const endIdx = Math.min(startIdx + windowSize.value, allRawData.length)
      const windowData = allRawData.slice(startIdx, endIdx)
      
      const clickedItem = windowData[params.dataIndex]
      if (clickedItem) {
        selectRow(clickedItem)
        nextTick(() => {
           const id = 'row-' + clickedItem.time.replace(/[: ]/g, '-')
           const el = document.getElementById(id)
           if(el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
        })
      }
    })
  }
}

const fetchData = async () => {
  loading.value = true
  try {
     // Using fixed range for demo
    const data = await api.getPriceCandles('2025-09-01 00:00:00', '2025-09-30 23:59:59', interval.value)
    allRawData = data
    currentStartIndex.value = Math.max(0, allRawData.length - windowSize.value) 
    updateChart()
  } catch (error) { 
    console.error('Data Fetch Error:', error) 
  } finally { 
    loading.value = false 
  }
}

const updateChart = () => {
  if (!chart || !allRawData.length) return
  
  const startIdx = currentStartIndex.value
  const endIdx = Math.min(startIdx + windowSize.value, allRawData.length)
  const windowData = allRawData.slice(startIdx, endIdx)
  
  const dates = windowData.map(item => item.time)
  const binanceData = windowData.map(item => [item.binance.open, item.binance.close, item.binance.low, item.binance.high])
  const uniswapData = windowData.map(item => [item.uniswap.open, item.uniswap.close, item.uniswap.low, item.uniswap.high])

  let series = []
  
  if (exchangeFilter.value === 'both' || exchangeFilter.value === 'binance') {
      series.push({
          name: 'Binance', type: 'candlestick', data: binanceData,
          itemStyle: { color: '#10B981', color0: '#EF4444', borderColor: '#10B981', borderColor0: '#EF4444' }
      })
  }
  if (exchangeFilter.value === 'both' || exchangeFilter.value === 'uniswap') {
      series.push({
          name: 'Uniswap', type: 'candlestick', data: uniswapData,
          itemStyle: { color: '#3B82F6', color0: '#F59E0B', borderColor: '#3B82F6', borderColor0: '#F59E0B' }
      })
  }

  chart.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
    legend: { show: true, top: 0, textStyle: { fontWeight: 'bold' } },
    grid: { left: '3%', right: '3%', top: '10%', bottom: '10%', containLabel: true },
    xAxis: { type: 'category', data: dates, axisLine: { lineStyle: { color: '#E5E7EB' } }, axisLabel: { color: '#6B7280' } },
    yAxis: { scale: true, splitLine: { lineStyle: { color: '#F3F4F6' } }, axisLabel: { color: '#6B7280' } },
    dataZoom: [{ type: 'inside', start: 0, end: 100 }],
    series
  }, true)
}

const navigateDays = (days) => {
  const step = Math.ceil(days * 24 / 4)
  let newIndex = currentStartIndex.value + step
  newIndex = Math.max(0, Math.min(newIndex, allRawData.length - windowSize.value))
  currentStartIndex.value = newIndex
  updateChart()
}

const changeInterval = (newInterval) => {
    interval.value = newInterval
    fetchData()
}

const selectRow = (item) => {
    selectedData.value = item
}

const formatPrice = (p) => p ? parseFloat(p).toFixed(2) : '-'
const formatVolume = (v) => v ? parseInt(v).toLocaleString() : '-'
const formatVolumeShort = (v) => {
    if(!v) return '-'
    if(v > 1000000) return (v/1000000).toFixed(1) + 'M'
    if(v > 1000) return (v/1000).toFixed(1) + 'K'
    return v.toFixed(0)
}
const formatTime = (t) => t || '-'

onMounted(() => {
  nextTick(() => {
    initChart()
    fetchData()
  })
})
</script>

<style lang="scss" scoped>
.page-container {
  padding: 20px;
  max-width: 1600px;
  margin: 0 auto;
  font-family: 'Inter', sans-serif;
  color: #1F2937;
}

.card {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  border: 1px solid #E5E7EB;
}

/* Ticker Header */
.ticker-header {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  margin-bottom: 20px;
  gap: 40px;
  
  .asset-info {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 180px;
    
    .asset-icon img { width: 44px; height: 44px; }
    .asset-names {
       display: flex;
       flex-direction: column;
       .asset-symbol { font-size: 18px; font-weight: 700; line-height: 1.2; }
       .asset-name { font-size: 13px; color: #6B7280; }
    }
  }
  
  .ticker-stats {
     display: flex;
     gap: 20px;
     flex: 1;
     
     .stat-card {
        background: #F9FAFB;
        border-radius: 6px;
        padding: 8px 16px;
        min-width: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        
        &.highlight {
            background: #EEF2FF;
            border: 1px solid #C7D2FE;
        }

        .stat-label { font-size: 11px; color: #6B7280; font-weight: 600; text-transform: uppercase; margin-bottom: 4px; }
        .stat-value { font-size: 16px; font-weight: 700; font-family: 'Roboto Mono', monospace; display: flex; align-items: center; gap: 8px; }
        
        .change-badge {
            font-size: 10px;
            padding: 2px 4px;
            border-radius: 4px;
            color: #fff;
            &.bg-green { background: #10B981; }
            &.bg-red { background: #EF4444; }
        }

        .stat-main {
            display: flex;
            align-items: baseline;
            gap: 6px;
            .spread-percent { font-size: 18px; font-weight: 800; font-family: 'Roboto Mono', monospace; }
            .spread-value { font-size: 12px; color: #6B7280; }
        }
        
        .arb-signal {
            margin-top: 4px;
            .signal-tag {
                font-size: 10px;
                color: #4F46E5;
                font-weight: 700;
                background: #E0E7FF;
                padding: 2px 6px;
                border-radius: 4px;
            }
        }
     }
  }
}

.text-binance { color: #10B981; }
.text-uniswap { color: #3B82F6; }
.text-up { color: #10B981; }
.text-down { color: #EF4444; }
.text-neutral { color: #6B7280; }

/* Main Grid */
.main-layout {
  display: flex;
  gap: 20px;
  
  .left-section { flex: 1; min-width: 0; }
  .right-section { width: 320px; flex-shrink: 0; }
}

/* Chart Card */
.chart-card {
  padding: 20px;
  
  .chart-header {
     display: flex;
     justify-content: space-between;
     align-items: center;
     margin-bottom: 16px;
     
     .chart-tabs {
        display: flex;
        gap: 20px;
        .tab-item {
           font-size: 14px;
           font-weight: 600;
           color: #6B7280;
           cursor: pointer;
           &.active { color: #111827; border-bottom: 2px solid #111827; }
        }
     }
     
     .time-controls {
        display: flex;
        gap: 4px;
        .time-btn {
           font-size: 12px;
           padding: 2px 8px;
           border-radius: 4px;
           cursor: pointer;
           color: #6B7280;
           &:hover { background: #F3F4F6; }
           &.active { background: #F3F4F6; color: #111827; font-weight: 600; }
        }
     }
  }
  
  .chart-controls-footer {
     margin-top: 16px;
     display: flex;
     justify-content: space-between;
     align-items: center;
     padding-top: 12px;
     border-top: 1px solid #F3F4F6;
     
     .nav-controls {
        display: flex;
        align-items: center;
        gap: 8px;
        .date-range { font-size: 13px; font-weight: 500; font-family: monospace; }
     }
  }
}

/* Order Book */
.order-book-card {
   height: 650px;
   display: flex;
   flex-direction: column;
   overflow: hidden;
   
   .card-header {
      padding: 16px;
      border-bottom: 1px solid #E5E7EB;
      .title { margin: 0; font-size: 15px; font-weight: 600; }
   }
   
   .order-book-header {
      display: flex;
      padding: 8px 16px;
      background: #F9FAFB;
      font-size: 10px;
      color: #9CA3AF;
      font-weight: 600;
      text-transform: uppercase;
      
      .col { flex: 1; }
   }
   
   .order-book-list {
      flex: 1;
      overflow-y: auto;
      
      .order-row {
         display: flex;
         padding: 6px 16px;
         font-size: 12px;
         cursor: pointer;
         font-family: 'Roboto Mono', monospace;
         
         &:hover { background: #F3F4F6; }
         &.selected { background: #EEF2FF; }
         
         .col { flex: 1; }
         .price-col { font-weight: 600; }
         .spread-col { color: #6B7280; }
      }
   }
   
   .order-stats {
      padding: 16px;
      background: #F9FAFB;
      border-top: 1px solid #E5E7EB;
      
      .stat-row {
         display: flex;
         justify-content: space-between;
         font-size: 12px;
         margin-bottom: 6px;
         color: #4B5563;
         .mono { font-family: 'Roboto Mono', monospace; font-weight: 600; color: #111827; }
         .contrast { color: #3B82F6; }
      }
      .stat-divider { height: 1px; background: #E5E7EB; margin: 8px 0; }
      .arb-opportunity {
         margin-top: 8px;
         background: #ECFDF5;
         color: #047857;
         font-size: 11px;
         font-weight: 600;
         padding: 6px;
         text-align: center;
         border-radius: 4px;
      }
   }
}

.text-right { text-align: right; }
</style>