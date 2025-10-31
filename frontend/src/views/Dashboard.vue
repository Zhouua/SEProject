<template>
  <div class="dashboard">
    <div class="dashboard-grid">
      <!-- 左侧内容 -->
      <div class="left-column">
        <!-- 钱包余额卡片 -->
        <div class="wallet-card">
          <div class="wallet-header">
            <div>
              <p class="wallet-label">Wallet Balance</p>
              <h2 class="wallet-balance">${{ walletBalance.toLocaleString() }}</h2>
              <div class="wallet-change">
                <el-icon class="change-icon" :class="walletChange >= 0 ? 'up' : 'down'">
                  <CaretTop v-if="walletChange >= 0" />
                  <CaretBottom v-else />
                </el-icon>
                <span :class="walletChange >= 0 ? 'text-up' : 'text-down'">{{ walletChange }}%</span>
                <span class="wallet-revenue">Your revenue is ${{ revenue.toLocaleString() }} this week</span>
              </div>
            </div>
            <el-select v-model="selectedCurrency" class="currency-select">
              <el-option label="USDT" value="USDT" />
              <el-option label="USD" value="USD" />
              <el-option label="EUR" value="EUR" />
            </el-select>
          </div>
          
          <div class="wallet-chart">
            <div ref="walletChartRef" style="width: 100%; height: 100px;"></div>
          </div>
          
          <div class="wallet-actions">
            <button class="btn btn-dark">Deposit</button>
            <button class="btn btn-primary">Withdraw</button>
          </div>
        </div>

        <!-- 快速操作 -->
        <div class="quick-actions">
          <h3 class="section-title">Quick Actions</h3>
          <p class="section-subtitle">Manage your crypto investments</p>
          <div class="action-buttons">
            <div class="action-btn" @click="$router.push('/buy-crypto')">
              <div class="action-icon buy">
                <el-icon><Plus /></el-icon>
              </div>
              <span>Buy</span>
            </div>
            <div class="action-btn" @click="$router.push('/sell-crypto')">
              <div class="action-icon sell">
                <el-icon><Minus /></el-icon>
              </div>
              <span>Sell</span>
            </div>
            <div class="action-btn">
              <div class="action-icon send">
                <el-icon><TopRight /></el-icon>
              </div>
              <span>Send</span>
            </div>
            <div class="action-btn">
              <div class="action-icon receive">
                <el-icon><BottomLeft /></el-icon>
              </div>
              <span>Receive</span>
            </div>
          </div>
        </div>

        <!-- 涨幅榜 -->
        <div class="top-movers">
          <div class="section-header">
            <h3 class="section-title">Top Movers</h3>
            <router-link to="/markets" class="more-link">
              More
              <el-icon><DArrowRight /></el-icon>
            </router-link>
          </div>
          <div class="movers-table">
            <div class="table-header">
              <div class="col">#</div>
              <div class="col">Coin</div>
              <div class="col">Price</div>
              <div class="col">24h Volume</div>
            </div>
            <div 
              v-for="(coin, index) in topMovers" 
              :key="coin.symbol"
              class="table-row"
              @click="$router.push(`/crypto/${coin.symbol}`)"
            >
              <div class="col">{{ index + 1 }}</div>
              <div class="col coin-info">
                <img :src="coin.icon" :alt="coin.name" class="coin-icon" />
                <div>
                  <div class="coin-name">{{ coin.name }}</div>
                  <div class="coin-symbol">{{ coin.symbol }}</div>
                </div>
              </div>
              <div class="col">
                <div class="price">${{ coin.price }}</div>
              </div>
              <div class="col">
                <span :class="coin.change >= 0 ? 'text-up' : 'text-down'">
                  <el-icon class="change-icon">
                    <CaretTop v-if="coin.change >= 0" />
                    <CaretBottom v-else />
                  </el-icon>
                  {{ Math.abs(coin.change) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧内容 -->
      <div class="right-column">
        <!-- 币种选择器和图表 -->
        <div class="chart-card">
          <div class="chart-header">
            <el-select v-model="selectedCoin" class="coin-select">
              <el-option 
                v-for="coin in coins" 
                :key="coin.value"
                :label="coin.label" 
                :value="coin.value"
              />
            </el-select>
            <el-select v-model="selectedChartCurrency" class="currency-select-small">
              <el-option label="USD" value="USD" />
              <el-option label="USDT" value="USDT" />
            </el-select>
          </div>
          
          <div class="price-info">
            <h2 class="current-price">${{ currentPrice.toLocaleString() }}</h2>
            <span :class="priceChange >= 0 ? 'text-up' : 'text-down'">
              <el-icon class="change-icon">
                <CaretTop v-if="priceChange >= 0" />
                <CaretBottom v-else />
              </el-icon>
              +${{ Math.abs(priceChangeAmount).toLocaleString() }} ({{ priceChange }}%)
            </span>
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
          
          <div class="chart-container">
            <div ref="priceChartRef" style="width: 100%; height: 300px;"></div>
          </div>
        </div>

        <!-- 观察列表 -->
        <div class="watchlist">
          <div class="section-header">
            <h3 class="section-title">Watchlist</h3>
            <router-link to="/markets" class="more-link">
              More
              <el-icon><DArrowRight /></el-icon>
            </router-link>
          </div>
          
          <div class="watchlist-table">
            <div class="table-header">
              <div class="col">#</div>
              <div class="col">Coin</div>
              <div class="col">Price</div>
              <div class="col">24h Volume</div>
              <div class="col">Actions</div>
            </div>
            <div 
              v-for="(coin, index) in watchlist" 
              :key="coin.symbol"
              class="table-row"
            >
              <div class="col">{{ index + 1 }}</div>
              <div class="col coin-info">
                <img :src="coin.icon" :alt="coin.name" class="coin-icon" />
                <div>
                  <div class="coin-name">{{ coin.name }}</div>
                  <div class="coin-symbol">{{ coin.symbol }}</div>
                </div>
              </div>
              <div class="col">
                <div class="price">${{ coin.price }}</div>
              </div>
              <div class="col">
                <span :class="coin.change >= 0 ? 'text-up' : 'text-down'">
                  <el-icon class="change-icon">
                    <CaretTop v-if="coin.change >= 0" />
                    <CaretBottom v-else />
                  </el-icon>
                  {{ Math.abs(coin.change) }}%
                </span>
              </div>
              <div class="col actions">
                <button class="btn-buy" @click="$router.push('/buy-crypto')">Buy</button>
                <el-icon class="favorite"><StarFilled /></el-icon>
                <el-icon class="more"><MoreFilled /></el-icon>
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
import * as echarts from 'echarts'
import { 
  CaretTop, 
  CaretBottom, 
  Plus, 
  Minus, 
  TopRight, 
  BottomLeft,
  DArrowRight,
  StarFilled,
  MoreFilled
} from '@element-plus/icons-vue'

// 数据
const walletBalance = ref(54496.41)
const walletChange = ref(4.61)
const revenue = ref(4864)
const selectedCurrency = ref('USDT')

const selectedCoin = ref('Bitcoin/BTC')
const selectedChartCurrency = ref('USD')
const currentPrice = ref(114884)
const priceChange = ref(4.61)
const priceChangeAmount = ref(82401.23)
const selectedTimeRange = ref('1D')
const timeRanges = ['1H', '4H', '12H', '1D', '1W', '1M']

const coins = [
  { label: 'Bitcoin/BTC', value: 'Bitcoin/BTC' },
  { label: 'Ethereum/ETH', value: 'Ethereum/ETH' },
  { label: 'Cardano/ADA', value: 'Cardano/ADA' },
]

const topMovers = ref([
  { name: 'Metadium', symbol: 'META', price: '0.0205', change: 42.33, icon: 'https://cryptologos.cc/logos/metadium-meta-logo.png?v=029' },
  { name: 'Sylo', symbol: 'SYLO', price: '0.0006', change: 51.33, icon: 'https://cryptologos.cc/logos/sylo-sylo-logo.png?v=029' },
  { name: 'Electroneum', symbol: 'ETN', price: '0.0035', change: 24.80, icon: 'https://cryptologos.cc/logos/electroneum-etn-logo.png?v=029' },
  { name: 'Utrust', symbol: 'UTK', price: '0.0353', change: 24.62, icon: 'https://cryptologos.cc/logos/utrust-utk-logo.png?v=029' },
])

const watchlist = ref([
  { name: 'Bitcoin', symbol: 'BTC', price: '114,884', change: -0.73, icon: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=029' },
  { name: 'Ethereum', symbol: 'ETH', price: '4,231', change: -1.06, icon: 'https://cryptologos.cc/logos/ethereum-eth-logo.png?v=029' },
  { name: 'XRP', symbol: 'XRP', price: '3.01', change: 1.23, icon: 'https://cryptologos.cc/logos/xrp-xrp-logo.png?v=029' },
  { name: 'Solana', symbol: 'SOL', price: '180.12', change: -0.60, icon: 'https://cryptologos.cc/logos/solana-sol-logo.png?v=029' },
  { name: 'Cardano', symbol: 'ADA', price: '0.9326', change: 0.99, icon: 'https://cryptologos.cc/logos/cardano-ada-logo.png?v=029' },
])

// 图表引用
const walletChartRef = ref(null)
const priceChartRef = ref(null)

// 初始化图表
onMounted(() => {
  initWalletChart()
  initPriceChart()
})

const initWalletChart = () => {
  const chart = echarts.init(walletChartRef.value)
  const option = {
    grid: { top: 5, right: 0, bottom: 5, left: 0 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false },
    series: [{
      data: [42000, 43500, 42800, 44200, 45000, 43800, 46000, 47500, 46800, 48500, 50000, 49500, 51000, 52500, 54496],
      type: 'line',
      smooth: true,
      symbol: 'none',
      lineStyle: { color: '#4CAF50', width: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(76, 175, 80, 0.3)' },
          { offset: 1, color: 'rgba(76, 175, 80, 0.05)' }
        ])
      }
    }]
  }
  chart.setOption(option)
}

const initPriceChart = () => {
  const chart = echarts.init(priceChartRef.value)
  const option = {
    grid: { top: 20, right: 30, bottom: 30, left: 50 },
    xAxis: {
      type: 'category',
      data: ['10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM', '01:00 PM'],
      axisLine: { lineStyle: { color: '#e0e0e0' } },
      axisLabel: { color: '#999' }
    },
    yAxis: {
      type: 'value',
      min: 15000,
      max: 35000,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f0f0f0', type: 'dashed' } },
      axisLabel: { color: '#999', formatter: '{value}k' }
    },
    series: [{
      data: [18000, 22000, 20000, 25000, 23000, 28000, 26000],
      type: 'line',
      smooth: true,
      symbol: 'none',
      lineStyle: { color: '#4CAF50', width: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(76, 175, 80, 0.3)' },
          { offset: 1, color: 'rgba(76, 175, 80, 0.05)' }
        ])
      }
    }]
  }
  chart.setOption(option)
}
</script>

<style lang="scss" scoped>
.dashboard {
  width: 100%;
  height: 100%;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 24px;
  height: 100%;
}

.left-column,
.right-column {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

// 卡片通用样式
.wallet-card,
.quick-actions,
.top-movers,
.chart-card,
.watchlist {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

// 钱包卡片
.wallet-card {
  .wallet-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
  }
  
  .wallet-label {
    color: #666;
    font-size: 14px;
    margin-bottom: 8px;
  }
  
  .wallet-balance {
    font-size: 32px;
    font-weight: 700;
    margin: 0 0 8px 0;
  }
  
  .wallet-change {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    
    .change-icon {
      font-size: 16px;
      
      &.up { color: #4CAF50; }
      &.down { color: #F44336; }
    }
  }
  
  .wallet-revenue {
    color: #999;
    margin-left: 8px;
  }
  
  .wallet-actions {
    display: flex;
    gap: 12px;
    margin-top: 16px;
  }
}

// 按钮样式
.btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  
  &.btn-dark {
    background: #2C2C2C;
    color: white;
    
    &:hover {
      background: #3C3C3C;
    }
  }
  
  &.btn-primary {
    background: #4CAF50;
    color: white;
    
    &:hover {
      background: #45A049;
    }
  }
}

// 快速操作
.quick-actions {
  .section-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 4px 0;
  }
  
  .section-subtitle {
    color: #999;
    font-size: 14px;
    margin: 0 0 20px 0;
  }
  
  .action-buttons {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
  
  .action-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    
    .action-icon {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      color: white;
      transition: transform 0.3s;
      
      &.buy { background: #4CAF50; }
      &.sell { background: #4CAF50; }
      &.send { background: #4CAF50; }
      &.receive { background: #4CAF50; }
    }
    
    span {
      font-size: 14px;
      color: #666;
    }
    
    &:hover .action-icon {
      transform: scale(1.1);
    }
  }
}

// 表格通用样式
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  
  .section-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
  }
  
  .more-link {
    display: flex;
    align-items: center;
    gap: 4px;
    color: #4CAF50;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    
    &:hover {
      opacity: 0.8;
    }
  }
}

.movers-table,
.watchlist-table {
  .table-header,
  .table-row {
    display: grid;
    grid-template-columns: 40px 2fr 1.5fr 1.5fr;
    align-items: center;
    padding: 12px 8px;
    gap: 16px;
  }
  
  .table-header {
    color: #999;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .table-row {
    border-bottom: 1px solid #f8f8f8;
    cursor: pointer;
    transition: background 0.3s;
    
    &:hover {
      background: #f8f8f8;
    }
  }
  
  .coin-info {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .coin-icon {
      width: 32px;
      height: 32px;
      border-radius: 50%;
    }
    
    .coin-name {
      font-weight: 600;
      font-size: 14px;
    }
    
    .coin-symbol {
      color: #999;
      font-size: 12px;
    }
  }
  
  .price {
    font-weight: 600;
  }
}

.watchlist-table {
  .table-header,
  .table-row {
    grid-template-columns: 40px 2fr 1.2fr 1.2fr 1.5fr;
  }
  
  .actions {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .btn-buy {
      padding: 6px 16px;
      background: #4CAF50;
      color: white;
      border: none;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      
      &:hover {
        background: #45A049;
      }
    }
    
    .favorite,
    .more {
      font-size: 20px;
      color: #FFB300;
      cursor: pointer;
    }
    
    .more {
      color: #999;
    }
  }
}

// 图表卡片
.chart-card {
  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }
  
  .price-info {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 16px;
    
    .current-price {
      font-size: 32px;
      font-weight: 700;
      margin: 0;
    }
  }
  
  .time-range {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    
    .time-btn {
      padding: 6px 12px;
      border: 1px solid #e0e0e0;
      background: white;
      border-radius: 6px;
      font-size: 12px;
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

// 文字颜色
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
