<template>
  <div class="trade-page">
    <div class="trade-grid">
      <!-- 左侧：图表和信息 -->
      <div class="left-section">
        <!-- 币种信息栏 -->
        <div class="coin-info-bar">
          <div class="coin-header">
            <img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=029" alt="Bitcoin" class="coin-icon" />
            <div>
              <h2 class="coin-name">Bitcoin <span class="coin-symbol">BTC</span></h2>
            </div>
          </div>
          
          <div class="coin-stats">
            <div class="stat-item">
              <div class="stat-value price">${{ priceData.current.toLocaleString() }}</div>
              <div class="stat-label">${{ priceData.current.toLocaleString() }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">{{ t('trade.change24h') }}</div>
              <div class="stat-value" :class="priceData.change24h >= 0 ? 'text-up' : 'text-down'">
                <el-icon class="change-icon">
                  <CaretTop v-if="priceData.change24h >= 0" />
                  <CaretBottom v-else />
                </el-icon>
                ${{ Math.abs(priceData.changeAmount).toLocaleString() }}
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-label">{{ t('trade.high24h') }}</div>
              <div class="stat-value" :class="priceData.high24h >= 0 ? 'text-up' : 'text-down'">
                <el-icon class="change-icon">
                  <CaretTop v-if="priceData.high24h >= 0" />
                  <CaretBottom v-else />
                </el-icon>
                ${{ priceData.high24hValue.toLocaleString() }}
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-label">{{ t('trade.low24h') }}</div>
              <div class="stat-value" :class="priceData.low24h >= 0 ? 'text-down' : 'text-down'">
                <el-icon class="change-icon">
                  <CaretBottom />
                </el-icon>
                ${{ priceData.low24hValue.toLocaleString() }}
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-label">{{ t('trade.volume24hBTC') }}</div>
              <div class="stat-value">{{ priceData.volumeBTC }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">{{ t('trade.volume24hUSD') }}</div>
              <div class="stat-value">${{ priceData.volumeUSD }}</div>
            </div>
          </div>
          
          <el-icon class="favorite-icon"><StarFilled /></el-icon>
        </div>

        <!-- 图表标签和工具栏 -->
        <div class="chart-toolbar">
          <div class="chart-tabs">
            <button 
              v-for="(tab, index) in chartTabs" 
              :key="tab"
              class="chart-tab"
              :class="{ active: selectedChartTab === tab }"
              @click="selectedChartTab = tab"
            >
              {{ t(chartTabKeys[index]) }}
            </button>
          </div>
          
          <div class="time-range">
            <button 
              v-for="range in timeRanges" 
              :key="range"
              class="time-btn"
              :class="{ active: selectedTimeRange === range }"
              @click="selectedTimeRange = range"
            >
              {{ range }}
            </button>
          </div>
        </div>

        <!-- 价格数据行 -->
        <div class="price-data-row">
          <div class="date-info">2025/08/22</div>
          <div class="ohlc-data">
            <span class="data-item">{{ t('trade.open') }} <strong>${{ ohlcData.open.toLocaleString() }}</strong></span>
            <span class="data-item">{{ t('trade.high') }} <strong class="text-up">${{ ohlcData.high.toLocaleString() }}</strong></span>
            <span class="data-item">{{ t('trade.low') }} <strong class="text-down">${{ ohlcData.low.toLocaleString() }}</strong></span>
            <span class="data-item">{{ t('trade.close') }} <strong>${{ ohlcData.close.toLocaleString() }}</strong></span>
            <span class="data-item">{{ t('trade.change') }} <strong :class="ohlcData.change >= 0 ? 'text-up' : 'text-down'">{{ ohlcData.change }}%</strong></span>
          </div>
        </div>

        <!-- K线图 -->
        <div class="chart-container">
          <div ref="candlestickChartRef" style="width: 100%; height: 500px;"></div>
        </div>

        <!-- 交易类型选择 -->
        <div class="order-type-tabs">
          <button 
            v-for="(type, index) in orderTypes" 
            :key="type"
            class="order-type-tab"
            :class="{ active: selectedOrderType === type }"
            @click="selectedOrderType = type"
          >
            {{ t(orderTypeKeys[index]) }}
          </button>
        </div>

        <!-- 下单表单 -->
        <div class="order-form-section">
          <div class="order-tabs">
            <button 
              v-for="(tab, index) in ['Market', 'Limit', 'Stop Limit']" 
              :key="tab"
              class="order-tab"
              :class="{ active: selectedOrderTab === tab }"
              @click="selectedOrderTab = tab"
            >
              {{ t(orderTabKeys[index]) }}
            </button>
          </div>

          <div class="order-inputs">
            <div class="input-row">
              <div class="input-group">
                <label>{{ t('trade.stop') }}</label>
                <div class="input-wrapper">
                  <img src="https://flagcdn.com/w40/us.png" class="currency-icon" />
                  <span class="currency-label">USDT</span>
                  <input type="number" v-model="orderForm.stop" placeholder="0.01" />
                  <el-icon><ArrowDown /></el-icon>
                </div>
              </div>
              
              <div class="input-group">
                <label>{{ t('trade.stop') }}</label>
                <div class="input-wrapper">
                  <img src="https://flagcdn.com/w40/us.png" class="currency-icon" />
                  <span class="currency-label">USDT</span>
                  <input type="number" v-model="orderForm.stopRight" placeholder="0.01" />
                  <el-icon><ArrowDown /></el-icon>
                </div>
              </div>
            </div>

            <div class="input-row">
              <div class="input-group">
                <label>{{ t('trade.limit') }}</label>
                <div class="input-wrapper">
                  <img src="https://flagcdn.com/w40/us.png" class="currency-icon" />
                  <span class="currency-label">USDT</span>
                  <input type="number" v-model="orderForm.limit" placeholder="113,162.16" />
                  <el-icon><ArrowDown /></el-icon>
                </div>
              </div>
              
              <div class="input-group">
                <label>{{ t('trade.limit') }}</label>
                <div class="input-wrapper">
                  <img src="https://flagcdn.com/w40/us.png" class="currency-icon" />
                  <span class="currency-label">USDT</span>
                  <input type="number" v-model="orderForm.limitRight" placeholder="113,162.16" />
                  <el-icon><ArrowDown /></el-icon>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：订单簿 -->
      <div class="right-section">
        <div class="order-book">
          <h3 class="order-book-title">{{ t('trade.orderBook') }}</h3>
          
          <div class="order-book-header">
            <div class="col">{{ t('trade.price') }} (USDT)</div>
            <div class="col">{{ t('trade.amount') }} (BTC)</div>
            <div class="col">{{ t('trade.total') }} (BTC)</div>
          </div>

          <!-- 卖单 -->
          <div class="order-book-list sell-orders">
            <div 
              v-for="(order, index) in sellOrders" 
              :key="`sell-${index}`"
              class="order-row sell"
              :style="{ '--progress': order.progress + '%' }"
            >
              <div class="col price">{{ order.price }}</div>
              <div class="col amount">{{ order.amount }}</div>
              <div class="col total">{{ order.total }}</div>
            </div>
          </div>

          <!-- 当前价格 -->
          <div class="current-price-row">
            <div class="current-price" :class="priceData.change24h >= 0 ? 'text-up' : 'text-down'">
              {{ priceData.current.toLocaleString(undefined, { minimumFractionDigits: 2 }) }}
            </div>
            <div class="price-arrow">
              <el-icon>
                <CaretTop v-if="priceData.change24h >= 0" />
                <CaretBottom v-else />
              </el-icon>
              ${{ priceData.changeAmount.toLocaleString() }}
            </div>
          </div>

          <!-- 买单 -->
          <div class="order-book-list buy-orders">
            <div 
              v-for="(order, index) in buyOrders" 
              :key="`buy-${index}`"
              class="order-row buy"
              :style="{ '--progress': order.progress + '%' }"
            >
              <div class="col price">{{ order.price }}</div>
              <div class="col amount">{{ order.amount }}</div>
              <div class="col total">{{ order.total }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts'
import { 
  CaretTop, 
  CaretBottom,
  StarFilled,
  ArrowDown
} from '@element-plus/icons-vue'

const { t } = useI18n()

// 价格数据
const priceData = ref({
  current: 112586.15,
  change24h: 118.20,
  changeAmount: 118.20,
  high24h: 118.250,
  high24hValue: 118250,
  low24h: -112.980,
  low24hValue: 112980,
  volumeBTC: '304,816 BTC',
  volumeUSD: '$64.09 B'
})

const ohlcData = ref({
  open: 112500.00,
  high: 113625.00,
  low: 112335.60,
  close: 112586.15,
  change: 0.07
})

// 图表选项
const chartTabs = ['Chart', 'Info', 'Trading Data', 'Trading Analysis', 'Square']
const chartTabKeys = ['trade.chart', 'trade.info', 'trade.tradingData', 'trade.tradingAnalysis', 'trade.square']
const selectedChartTab = ref('Chart')
const timeRanges = ['1H', '4H', '12H', '1D', '1W', '1M']
const selectedTimeRange = ref('1D')

// 订单类型
const orderTypes = ['Spot', 'Cross', 'Isolated', 'Grid']
const orderTypeKeys = ['trade.spot', 'trade.cross', 'trade.isolated', 'trade.grid']
const selectedOrderType = ref('Spot')
const selectedOrderTab = ref('Stop Limit')
const orderTabKeys = ['trade.market', 'trade.limit', 'trade.stopLimit']

// 下单表单
const orderForm = ref({
  stop: 0.01,
  stopRight: 0.01,
  limit: 113162.16,
  limitRight: 113162.16
})

// 订单簿数据
const sellOrders = ref([
  { price: '112,596.00', amount: '0.00075', total: '11.25959', progress: 80 },
  { price: '112,596.01', amount: '0.00010', total: '2.40k', progress: 20 },
  { price: '112,596.89', amount: '0.00043', total: '2.59k', progress: 45 },
  { price: '112,596.90', amount: '0.06554', total: '7.37k', progress: 90 },
  { price: '112,596.54', amount: '0.00075', total: '11.25959', progress: 75 },
  { price: '112,596.20', amount: '0.00075', total: '1.35M', progress: 100 },
  { price: '112,596.00', amount: '0.00075', total: '11.25959', progress: 60 },
  { price: '112,596.01', amount: '0.00010', total: '2.40k', progress: 25 },
  { price: '112,596.89', amount: '0.00043', total: '2.59k', progress: 40 },
  { price: '112,596.90', amount: '0.06554', total: '7.37k', progress: 85 },
])

const buyOrders = ref([
  { price: '112,596.00', amount: '0.01463', total: '11.25959', progress: 70 },
  { price: '112,596.01', amount: '0.00060', total: '2.40k', progress: 30 },
  { price: '112,596.89', amount: '0.00005', total: '5.14k', progress: 50 },
  { price: '112,596.90', amount: '0.02145', total: '2.41k', progress: 35 },
  { price: '112,596.54', amount: '0.00075', total: '11.25959', progress: 80 },
  { price: '112,596.00', amount: '0.00075', total: '11.25959', progress: 65 },
  { price: '112,596.01', amount: '0.00010', total: '2.40k', progress: 20 },
  { price: '112,596.89', amount: '0.00043', total: '2.59k', progress: 45 },
  { price: '112,596.90', amount: '0.06554', total: '7.37k', progress: 90 },
  { price: '112,596.54', amount: '0.00075', total: '11.25959', progress: 75 },
])

// 图表引用
const candlestickChartRef = ref(null)

// 初始化K线图
onMounted(() => {
  initCandlestickChart()
})

const initCandlestickChart = () => {
  const chart = echarts.init(candlestickChartRef.value)
  
  // 生成模拟K线数据
  const data = []
  const volumes = []
  const times = []
  
  for (let i = 0; i < 60; i++) {
    const hour = 10 + Math.floor(i / 6)
    const minute = (i % 6) * 10
    times.push(`${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')} AM`)
    
    const open = 112000 + Math.random() * 2000
    const close = open + (Math.random() - 0.5) * 1000
    const low = Math.min(open, close) - Math.random() * 500
    const high = Math.max(open, close) + Math.random() * 500
    
    data.push([open, close, low, high])
    volumes.push(Math.random() * 50000 + 10000)
  }
  
  const option = {
    grid: [
      { left: '5%', right: '5%', top: '5%', height: '70%' },
      { left: '5%', right: '5%', top: '80%', height: '15%' }
    ],
    xAxis: [
      {
        type: 'category',
        data: times,
        gridIndex: 0,
        axisLine: { lineStyle: { color: '#e0e0e0' } },
        axisLabel: { color: '#999', show: false }
      },
      {
        type: 'category',
        data: times,
        gridIndex: 1,
        axisLine: { lineStyle: { color: '#e0e0e0' } },
        axisLabel: { color: '#999', interval: 5 }
      }
    ],
    yAxis: [
      {
        type: 'value',
        gridIndex: 0,
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f0f0f0', type: 'dashed' } },
        axisLabel: { color: '#999' }
      },
      {
        type: 'value',
        gridIndex: 1,
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false }
      }
    ],
    series: [
      {
        type: 'candlestick',
        data: data,
        xAxisIndex: 0,
        yAxisIndex: 0,
        itemStyle: {
          color: '#4CAF50',
          color0: '#F44336',
          borderColor: '#4CAF50',
          borderColor0: '#F44336'
        }
      },
      {
        type: 'bar',
        data: volumes,
        xAxisIndex: 1,
        yAxisIndex: 1,
        itemStyle: {
          color: function(params) {
            const dataIndex = params.dataIndex
            return data[dataIndex][1] >= data[dataIndex][0] ? '#4CAF50' : '#F44336'
          }
        }
      }
    ],
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    }
  }
  
  chart.setOption(option)
}
</script>

<style lang="scss" scoped>
.trade-page {
  width: 100%;
  height: 100%;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  animation: fadeInPage 0.8s ease-out;
}

@keyframes fadeInPage {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.trade-grid {
  display: grid;
  grid-template-columns: 1fr 380px;
  height: 100%;
}

.left-section {
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e0e0e0;
  overflow-y: auto;
}

.right-section {
  background: white;
  overflow-y: auto;
}

// 币种信息栏
.coin-info-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
  background: white;
  
  .coin-header {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .coin-icon {
      width: 36px;
      height: 36px;
      border-radius: 50%;
    }
    
    .coin-name {
      font-size: 18px;
      font-weight: 700;
      margin: 0;
      
      .coin-symbol {
        color: #999;
        font-weight: 500;
      }
    }
  }
  
  .coin-stats {
    display: flex;
    gap: 32px;
    
    .stat-item {
      .stat-label {
        color: #999;
        font-size: 12px;
        margin-bottom: 4px;
      }
      
      .stat-value {
        font-size: 14px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
        
        &.price {
          font-size: 16px;
        }
      }
    }
  }
  
  .favorite-icon {
    font-size: 24px;
    color: #FFB300;
    cursor: pointer;
  }
}

// 图表工具栏
.chart-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  background: white;
  
  .chart-tabs {
    display: flex;
    gap: 8px;
    
    .chart-tab {
      padding: 8px 16px;
      border: none;
      background: transparent;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      color: #666;
      cursor: pointer;
      transition: all 0.3s;
      
      &:hover {
        background: #f5f5f5;
      }
      
      &.active {
        background: #4CAF50;
        color: white;
      }
    }
  }
  
  .time-range {
    display: flex;
    gap: 4px;
    
    .time-btn {
      padding: 6px 12px;
      border: 1px solid #e0e0e0;
      background: white;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s;
      
      &:hover {
        border-color: #4CAF50;
      }
      
      &.active {
        background: #4CAF50;
        color: white;
        border-color: #4CAF50;
      }
    }
  }
}

// 价格数据行
.price-data-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  border-bottom: 1px solid #f0f0f0;
  background: #fafafa;
  
  .date-info {
    font-size: 13px;
    color: #666;
    font-weight: 600;
  }
  
  .ohlc-data {
    display: flex;
    gap: 24px;
    
    .data-item {
      font-size: 12px;
      color: #999;
      
      strong {
        color: #1a1a1a;
        margin-left: 4px;
      }
    }
  }
}

// 订单类型标签
.order-type-tabs {
  display: flex;
  gap: 8px;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
  
  .order-type-tab {
    padding: 8px 16px;
    border: 1px solid #e0e0e0;
    background: white;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      border-color: #4CAF50;
    }
    
    &.active {
      background: #4CAF50;
      color: white;
      border-color: #4CAF50;
    }
  }
}

// 下单表单
.order-form-section {
  padding: 24px;
  
  .order-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
    
    .order-tab {
      flex: 1;
      padding: 10px;
      border: 1px solid #e0e0e0;
      background: white;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s;
      
      &:hover {
        border-color: #4CAF50;
      }
      
      &.active {
        background: #E8F5E9;
        color: #4CAF50;
        border-color: #4CAF50;
      }
    }
  }
  
  .order-inputs {
    display: flex;
    flex-direction: column;
    gap: 16px;
    
    .input-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }
    
    .input-group {
      label {
        display: block;
        color: #666;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
      }
      
      .input-wrapper {
        position: relative;
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 16px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background: white;
        
        .currency-icon {
          width: 20px;
          height: 20px;
          border-radius: 50%;
        }
        
        .currency-label {
          font-size: 13px;
          font-weight: 600;
        }
        
        input {
          flex: 1;
          border: none;
          outline: none;
          font-size: 14px;
          font-weight: 600;
          text-align: right;
        }
        
        .el-icon {
          color: #999;
          font-size: 16px;
          cursor: pointer;
        }
      }
    }
  }
}

// 订单簿
.order-book {
  padding: 24px;
  
  .order-book-title {
    font-size: 16px;
    font-weight: 700;
    margin: 0 0 16px 0;
  }
  
  .order-book-header {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    padding: 8px 12px;
    color: #999;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    border-bottom: 1px solid #f0f0f0;
    
    .col {
      text-align: right;
      
      &:first-child {
        text-align: left;
      }
    }
  }
  
  .order-book-list {
    position: relative;
    
    .order-row {
      position: relative;
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      padding: 6px 12px;
      font-size: 12px;
      cursor: pointer;
      
      &::before {
        content: '';
        position: absolute;
        right: 0;
        top: 0;
        bottom: 0;
        width: var(--progress);
        opacity: 0.1;
        z-index: 0;
      }
      
      &.sell::before {
        background: #F44336;
      }
      
      &.buy::before {
        background: #4CAF50;
      }
      
      .col {
        position: relative;
        z-index: 1;
        text-align: right;
        
        &:first-child {
          text-align: left;
        }
        
        &.price {
          font-weight: 600;
        }
      }
      
      &.sell .price {
        color: #F44336;
      }
      
      &.buy .price {
        color: #4CAF50;
      }
      
      &:hover {
        background: #f8f8f8;
      }
    }
  }
  
  .current-price-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px;
    margin: 8px 0;
    background: #f5f5f5;
    border-radius: 8px;
    
    .current-price {
      font-size: 18px;
      font-weight: 700;
    }
    
    .price-arrow {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 14px;
      font-weight: 600;
      color: #666;
    }
  }
}

// 通用样式
.text-up {
  color: #4CAF50;
}

.text-down {
  color: #F44336;
}

.change-icon {
  font-size: 12px;
}
</style>
