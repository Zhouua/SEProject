<template>
  <div class="crypto-details">
    <div class="details-grid">
      <!-- 左侧：图表区域 -->
      <div class="left-section">
        <!-- 币种信息头部 -->
        <div class="crypto-header">
          <div class="crypto-info">
            <img :src="cryptoData.icon" :alt="cryptoData.name" class="crypto-icon" />
            <div>
              <h2 class="crypto-name">{{ cryptoData.name }} <span class="crypto-symbol">{{ cryptoData.symbol }}</span></h2>
            </div>
          </div>
        </div>

        <!-- 价格信息 -->
        <div class="price-section">
          <h1 class="current-price">${{ currentPrice.toLocaleString() }}</h1>
          <span :class="priceChange >= 0 ? 'text-up' : 'text-down'" class="price-change">
            <el-icon class="change-icon">
              <CaretTop v-if="priceChange >= 0" />
              <CaretBottom v-else />
            </el-icon>
            +${{ Math.abs(priceChangeAmount).toLocaleString() }} ({{ priceChange }}%)
          </span>
        </div>

        <!-- 时间范围选择 -->
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

        <!-- 价格图表 -->
        <div class="chart-container">
          <div ref="priceChartRef" style="width: 100%; height: 400px;"></div>
        </div>

        <!-- 统计数据 -->
        <div class="stats-section">
          <h3 class="section-title">Stats</h3>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-label">Circulating Supply</div>
              <div class="stat-value">~{{ stats.circulatingSupply }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">Market Cap</div>
              <div class="stat-value">${{ stats.marketCap }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">FDV</div>
              <div class="stat-value">${{ stats.fdv }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">24-Hour Volume</div>
              <div class="stat-value">${{ stats.volume24h }}</div>
            </div>
          </div>
        </div>

        <!-- 关于 -->
        <div class="about-section">
          <h3 class="section-title">About {{ cryptoData.name }}</h3>
          <p class="about-text">{{ cryptoData.description }}</p>
        </div>
      </div>

      <!-- 右侧：交易面板 -->
      <div class="right-section">
        <!-- 交易标签 -->
        <div class="trade-tabs">
          <button 
            v-for="tab in tradeTabs" 
            :key="tab"
            class="trade-tab"
            :class="{ active: selectedTab === tab }"
            @click="selectedTab = tab"
          >
            {{ tab }}
          </button>
        </div>

        <!-- 交易表单 -->
        <div class="trade-form">
          <div class="form-group">
            <label class="form-label">I'm Buying</label>
            <div class="input-wrapper">
              <input 
                type="number" 
                class="form-input" 
                v-model="buyAmount"
                placeholder="0.01"
              />
              <div class="currency-badge">
                <img :src="cryptoData.icon" class="badge-icon" />
                <span>{{ cryptoData.symbol }}</span>
                <el-icon><ArrowDown /></el-icon>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">I'm Spending</label>
            <div class="input-wrapper">
              <input 
                type="number" 
                class="form-input" 
                v-model="spendAmount"
                placeholder="$432.51"
              />
              <div class="currency-badge">
                <img src="https://flagcdn.com/w40/us.png" class="badge-icon" />
                <span>USD</span>
                <el-icon><ArrowDown /></el-icon>
              </div>
            </div>
          </div>

          <div class="exchange-rate">
            1 BTC = {{ exchangeRate.toLocaleString() }} USD
          </div>

          <div class="payment-method">
            <label class="form-label">Pay with</label>
            <div class="payment-card">
              <div class="payment-info">
                <div class="payment-icon">
                  <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                    <rect width="32" height="32" rx="8" fill="#4CAF50"/>
                    <path d="M16 8L22 16L16 24L10 16L16 8Z" fill="white"/>
                  </svg>
                </div>
                <div>
                  <div class="payment-title">Crypto Wallet</div>
                  <div class="payment-account">**** 6602</div>
                </div>
              </div>
              <button class="change-btn">Change</button>
            </div>
          </div>

          <button class="continue-btn">
            Continue
            <el-icon><ArrowRight /></el-icon>
          </button>
        </div>

        <!-- Top Movers -->
        <div class="top-movers">
          <div class="section-header">
            <h3 class="section-title">Top Movers</h3>
            <router-link to="/markets" class="more-link">
              More
              <el-icon><DArrowRight /></el-icon>
            </router-link>
          </div>
          
          <div class="movers-list">
            <div 
              v-for="(coin, index) in topMovers" 
              :key="coin.symbol"
              class="mover-item"
            >
              <div class="mover-rank">{{ index + 1 }}</div>
              <img :src="coin.icon" :alt="coin.name" class="mover-icon" />
              <div class="mover-info">
                <div class="mover-name">{{ coin.name }}</div>
                <div class="mover-symbol">{{ coin.symbol }}</div>
              </div>
              <div class="mover-stats">
                <div class="mover-price">${{ coin.price }}</div>
                <div :class="coin.change >= 0 ? 'text-up' : 'text-down'" class="mover-change">
                  <el-icon class="change-icon">
                    <CaretTop v-if="coin.change >= 0" />
                    <CaretBottom v-else />
                  </el-icon>
                  {{ Math.abs(coin.change) }}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
import { 
  CaretTop, 
  CaretBottom,
  ArrowDown,
  ArrowRight,
  DArrowRight
} from '@element-plus/icons-vue'

const route = useRoute()

// 数据
const cryptoData = ref({
  name: 'Bitcoin',
  symbol: 'BTC',
  icon: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=029',
  description: 'Bitcoin is one of the most popular cryptocurrencies in the market. First introduced in 2009 by Satoshi Nakamoto, Bitcoin continues to be the top cryptocurrency by market capitalization. Bitcoin paved the way for many existing altcoins in the market and marked a pivotal moment for digital payment solutions. Bitcoin recorded a new all-time high of $111,970 in May 2025, pushing the crypto market capitalization to an impressive $3.5 trillion.'
})

const currentPrice = ref(114884)
const priceChange = ref(4.61)
const priceChangeAmount = ref(82401.23)
const selectedTimeRange = ref('1D')
const timeRanges = ['1H', '4H', '12H', '1D', '1W', '1M']

const stats = ref({
  circulatingSupply: '19.91M BTC',
  marketCap: '2.27 T',
  fdv: '2.39 T',
  volume24h: '70.7 B'
})

const tradeTabs = ['Buy', 'Sell', 'Swap']
const selectedTab = ref('Buy')

const buyAmount = ref(0.01)
const spendAmount = ref(432.51)
const exchangeRate = ref(23876)

const topMovers = ref([
  { name: 'Metadium', symbol: 'META', price: '0.0205', change: 42.33, icon: 'https://cryptologos.cc/logos/metadium-meta-logo.png?v=029' },
  { name: 'Electroneum', symbol: 'ETN', price: '0.1406', change: 30.23, icon: 'https://cryptologos.cc/logos/electroneum-etn-logo.png?v=029' },
  { name: 'Utrust', symbol: 'UTK', price: '1.0205', change: 12.24, icon: 'https://cryptologos.cc/logos/utrust-utk-logo.png?v=029' },
  { name: 'Metadium', symbol: 'META', price: '0.2305', change: 56.63, icon: 'https://cryptologos.cc/logos/metadium-meta-logo.png?v=029' },
])

// 图表引用
const priceChartRef = ref(null)

// 初始化图表
onMounted(() => {
  initPriceChart()
})

const initPriceChart = () => {
  const chart = echarts.init(priceChartRef.value)
  
  // 生成模拟K线数据
  const data = []
  const times = []
  let basePrice = 30000
  
  for (let i = 0; i < 50; i++) {
    const hour = Math.floor(i / 4)
    const minute = (i % 4) * 15
    times.push(`${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')} AM`)
    
    const change = (Math.random() - 0.5) * 5000
    basePrice += change
    data.push(Math.round(basePrice))
  }
  
  const option = {
    grid: { 
      top: 40, 
      right: 60, 
      bottom: 50, 
      left: 60 
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: function(params) {
        return `${params[0].axisValue}<br/>$${params[0].data.toLocaleString()}`
      }
    },
    xAxis: {
      type: 'category',
      data: times,
      axisLine: { lineStyle: { color: '#e0e0e0' } },
      axisLabel: { 
        color: '#999',
        interval: 7
      }
    },
    yAxis: {
      type: 'value',
      position: 'right',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { 
        lineStyle: { color: '#f0f0f0', type: 'dashed' } 
      },
      axisLabel: { 
        color: '#999',
        formatter: '{value}k'
      }
    },
    series: [{
      data: data,
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      showSymbol: false,
      lineStyle: { 
        color: '#4CAF50', 
        width: 2 
      },
      itemStyle: {
        color: '#4CAF50'
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(76, 175, 80, 0.3)' },
          { offset: 1, color: 'rgba(76, 175, 80, 0.05)' }
        ])
      }
    }]
  }
  
  chart.setOption(option)
  
  // 添加图表上的悬浮点提示
  chart.on('mousemove', function(params) {
    if (params.componentType === 'series') {
      chart.setOption({
        series: [{
          showSymbol: true
        }]
      })
    }
  })
}
</script>

<style lang="scss" scoped>
.crypto-details {
  width: 100%;
  height: 100%;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 24px;
  height: 100%;
}

.left-section {
  background: white;
  border-radius: 16px;
  padding: 32px;
  overflow-y: auto;
}

.right-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

// 币种头部
.crypto-header {
  margin-bottom: 24px;
}

.crypto-info {
  display: flex;
  align-items: center;
  gap: 16px;
  
  .crypto-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
  }
  
  .crypto-name {
    font-size: 24px;
    font-weight: 700;
    margin: 0;
    
    .crypto-symbol {
      color: #999;
      font-weight: 500;
      font-size: 18px;
    }
  }
}

// 价格信息
.price-section {
  display: flex;
  align-items: baseline;
  gap: 16px;
  margin-bottom: 24px;
  
  .current-price {
    font-size: 48px;
    font-weight: 700;
    margin: 0;
  }
  
  .price-change {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 16px;
    font-weight: 600;
  }
}

// 时间范围选择
.time-range {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  
  .time-btn {
    padding: 8px 16px;
    border: 1px solid #e0e0e0;
    background: white;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      border-color: #4CAF50;
      color: #4CAF50;
    }
    
    &.active {
      background: #4CAF50;
      color: white;
      border-color: #4CAF50;
    }
  }
}

// 统计数据
.stats-section {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid #f0f0f0;
  
  .section-title {
    font-size: 20px;
    font-weight: 700;
    margin: 0 0 24px 0;
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
  }
  
  .stat-item {
    .stat-label {
      color: #999;
      font-size: 14px;
      margin-bottom: 8px;
    }
    
    .stat-value {
      font-size: 20px;
      font-weight: 700;
    }
  }
}

// 关于部分
.about-section {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid #f0f0f0;
  
  .section-title {
    font-size: 20px;
    font-weight: 700;
    margin: 0 0 16px 0;
  }
  
  .about-text {
    color: #666;
    line-height: 1.8;
    font-size: 14px;
  }
}

// 交易面板
.trade-tabs {
  background: white;
  border-radius: 16px;
  padding: 8px;
  display: flex;
  gap: 8px;
  
  .trade-tab {
    flex: 1;
    padding: 12px;
    border: none;
    background: transparent;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    color: #666;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      background: #f5f5f5;
    }
    
    &.active {
      background: #f5f5f5;
      color: #1a1a1a;
    }
  }
}

.trade-form {
  background: white;
  border-radius: 16px;
  padding: 24px;
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .form-label {
    display: block;
    color: #666;
    font-size: 13px;
    margin-bottom: 8px;
    font-weight: 500;
  }
  
  .input-wrapper {
    position: relative;
    
    .form-input {
      width: 100%;
      padding: 16px;
      padding-right: 120px;
      border: 1px solid #e0e0e0;
      border-radius: 12px;
      font-size: 18px;
      font-weight: 600;
      outline: none;
      
      &:focus {
        border-color: #4CAF50;
      }
    }
    
    .currency-badge {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 12px;
      background: #f5f5f5;
      border-radius: 8px;
      cursor: pointer;
      
      .badge-icon {
        width: 24px;
        height: 24px;
        border-radius: 50%;
      }
      
      span {
        font-size: 14px;
        font-weight: 600;
      }
    }
  }
  
  .exchange-rate {
    text-align: center;
    color: #4CAF50;
    font-size: 14px;
    font-weight: 600;
    margin: 16px 0;
  }
  
  .payment-method {
    margin-top: 24px;
  }
  
  .payment-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    margin-top: 8px;
    
    .payment-info {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .payment-title {
        font-weight: 600;
        font-size: 14px;
      }
      
      .payment-account {
        color: #999;
        font-size: 12px;
      }
    }
    
    .change-btn {
      padding: 6px 16px;
      border: 1px solid #e0e0e0;
      background: white;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      
      &:hover {
        border-color: #4CAF50;
        color: #4CAF50;
      }
    }
  }
  
  .continue-btn {
    width: 100%;
    padding: 16px;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    margin-top: 24px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: background 0.3s;
    
    &:hover {
      background: #45A049;
    }
  }
}

// Top Movers
.top-movers {
  background: white;
  border-radius: 16px;
  padding: 24px;
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    .section-title {
      font-size: 16px;
      font-weight: 700;
      margin: 0;
    }
    
    .more-link {
      display: flex;
      align-items: center;
      gap: 4px;
      color: #4CAF50;
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
    }
  }
  
  .movers-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .mover-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: background 0.3s;
    
    &:hover {
      background: #f8f8f8;
    }
    
    .mover-rank {
      width: 24px;
      color: #999;
      font-weight: 600;
      font-size: 14px;
    }
    
    .mover-icon {
      width: 36px;
      height: 36px;
      border-radius: 50%;
    }
    
    .mover-info {
      flex: 1;
      
      .mover-name {
        font-weight: 600;
        font-size: 14px;
      }
      
      .mover-symbol {
        color: #999;
        font-size: 12px;
      }
    }
    
    .mover-stats {
      text-align: right;
      
      .mover-price {
        font-weight: 600;
        font-size: 14px;
      }
      
      .mover-change {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 2px;
        font-size: 12px;
        font-weight: 600;
      }
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
  font-size: 14px;
}
</style>
