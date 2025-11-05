<template>
  <div class="dashboard">
    <div class="dashboard-layout">
      <!-- 左侧栏 -->
      <div class="left-panel">
        <div class="left-top-group">
          <!-- 套利收益卡片 -->
          <div class="profit-card">
            <div class="profit-header">
              <div class="profit-info">
                <p class="profit-label">{{ t('dashboard.walletBalance') }}</p>
                <h2 class="profit-amount">${{ walletBalance.toLocaleString() }}</h2>
                <div class="profit-change">
                  <el-icon class="change-icon" :class="walletChange >= 0 ? 'up' : 'down'">
                    <CaretTop v-if="walletChange >= 0" />
                    <CaretBottom v-else />
                  </el-icon>
                  <span :class="walletChange >= 0 ? 'text-up' : 'text-down'">{{ walletChange }}%</span>
                </div>
                <p class="revenue-text">{{ t('dashboard.revenue') }} ${{ revenue.toLocaleString() }}</p>
              </div>
              <div class="profit-right">
                <el-select v-model="selectedCurrency" class="currency-select" size="small">
                  <el-option label="USDT" value="USDT" />
                  <el-option label="USD" value="USD" />
                </el-select>
                <div class="mini-chart">
                  <div ref="miniChartRef" style="width: 140px; height: 60px;"></div>
                </div>
              </div>
            </div>
            
            <div class="profit-actions">
              <button class="btn btn-dark">{{ t('dashboard.deposit') }}</button>
              <button class="btn btn-primary">{{ t('dashboard.withdraw') }}</button>
            </div>
          </div>

          <!-- 快速操作 -->
          <div class="quick-actions">
            <div class="section-header-simple">
              <h3 class="section-title">{{ t('dashboard.quickActions') }}</h3>
              <p class="section-subtitle">{{ t('dashboard.manageInvestments') }}</p>
            </div>
            <div class="action-grid">
              <div class="action-item" @click="$router.push('/buy-crypto')">
                <div class="action-icon"><el-icon><Plus /></el-icon></div>
                <span>{{ t('dashboard.buy') }}</span>
              </div>
              <div class="action-item" @click="$router.push('/sell-crypto')">
                <div class="action-icon"><el-icon><Minus /></el-icon></div>
                <span>{{ t('dashboard.sell') }}</span>
              </div>
              <div class="action-item" @click="$router.push('/trade')">
                <div class="action-icon"><el-icon><TopRight /></el-icon></div>
                <span>{{ t('dashboard.send') }}</span>
              </div>
              <div class="action-item" @click="$router.push('/wallet')">
                <div class="action-icon"><el-icon><BottomLeft /></el-icon></div>
                <span>{{ t('dashboard.receive') }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 最大价差记录 -->
        <div class="top-movers">
          <div class="section-header">
            <h3 class="section-title">{{ t('dashboard.topMovers') }}</h3>
            <router-link to="/markets" class="more-link">
              {{ t('dashboard.more') }}
              <el-icon><DArrowRight /></el-icon>
            </router-link>
          </div>
          <div class="compact-table">
            <div class="table-header">
              <div class="col">#</div>
              <div class="col">{{ t('dashboard.coin') }}</div>
              <div class="col">{{ t('dashboard.price') }}</div>
              <div class="col">{{ t('dashboard.volume24h') }}</div>
            </div>
            <div 
              v-for="(coin, index) in topMovers.slice(0, 4)" 
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
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧栏 -->
      <div class="right-panel">
        <!-- 价格图表 -->
        <div class="chart-card">
          <div class="chart-header">
            <el-select v-model="selectedCoin" class="coin-select">
              <el-option label="USDT/ETH" value="USDT/ETH" />
              <el-option label="Bitcoin/BTC" value="Bitcoin/BTC" />
            </el-select>
            <el-select v-model="selectedChartCurrency" class="currency-select-small">
              <el-option label="USD" value="USD" />
              <el-option label="USDT" value="USDT" />
            </el-select>
          </div>
          
          <div class="price-section">
            <div class="price-display">
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
                @click="changeTimeRange(range)"
              >
                {{ range }}
              </button>
            </div>
          </div>
          
          <div class="main-chart">
            <div ref="priceChartRef" style="width: 100%; height: 100%;"></div>
          </div>
        </div>

        <!-- 套利机会监控 -->
        <div class="watchlist">
          <div class="section-header">
            <h3 class="section-title">{{ t('dashboard.watchlist') }}</h3>
            <router-link to="/markets" class="more-link">
              {{ t('dashboard.more') }}
              <el-icon><DArrowRight /></el-icon>
            </router-link>
          </div>
          
          <div class="compact-table">
            <div class="table-header">
              <div class="col">#</div>
              <div class="col">{{ t('dashboard.coin') }}</div>
              <div class="col">{{ t('dashboard.price') }}</div>
              <div class="col">{{ t('dashboard.volume24h') }}</div>
              <div class="col">{{ t('dashboard.actions') }}</div>
            </div>
            <div 
              v-for="(coin, index) in watchlist.slice(0, 5)" 
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
                <button class="btn-buy" @click="$router.push('/buy-crypto')">{{ t('dashboard.buy') }}</button>
                <el-icon class="favorite"><StarFilled /></el-icon>
                <el-icon class="more-icon"><MoreFilled /></el-icon>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
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

const { t } = useI18n()

// 数据
const walletBalance = ref(54496.41)
const walletChange = ref(4.61)
const revenue = ref(4864)
const selectedCurrency = ref('USDT')

const selectedCoin = ref('USDT/ETH')
const selectedChartCurrency = ref('USD')
const currentPrice = ref(114884)
const priceChange = ref(4.61)
const priceChangeAmount = ref(82401.23)
const selectedTimeRange = ref('1D')
const timeRanges = ['1H', '4H', '12H', '1D', '1W', '1M']

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
const priceChartRef = ref(null)
const miniChartRef = ref(null)
let priceChart = null
let miniChart = null

// 生成不同时间范围的模拟数据
const generateChartData = (timeRange) => {
  const dataPoints = {
    '1H': 12,   // 5分钟一个点
    '4H': 16,   // 15分钟一个点
    '12H': 24,  // 30分钟一个点
    '1D': 24,   // 1小时一个点
    '1W': 28,   // 6小时一个点
    '1M': 30    // 1天一个点
  }
  
  const count = dataPoints[timeRange]
  const data = []
  const times = []
  const basePrice = 110000
  let currentPrice = basePrice
  
  for (let i = 0; i < count; i++) {
    // 生成时间标签
    times.push(getTimeLabel(timeRange, i, count))
    
    // 生成价格数据（模拟随机波动）
    const change = (Math.random() - 0.5) * 8000
    currentPrice = Math.max(basePrice * 0.8, Math.min(basePrice * 1.2, currentPrice + change))
    data.push(Math.round(currentPrice))
  }
  
  return { times, data }
}

// 生成时间标签
const getTimeLabel = (timeRange, index, total) => {
  const now = new Date()
  let time
  
  switch(timeRange) {
    case '1H':
      time = new Date(now - (total - index) * 5 * 60 * 1000)
      return time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
    case '4H':
      time = new Date(now - (total - index) * 15 * 60 * 1000)
      return time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
    case '12H':
      time = new Date(now - (total - index) * 30 * 60 * 1000)
      return time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
    case '1D':
      time = new Date(now - (total - index) * 60 * 60 * 1000)
      return time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
    case '1W':
      time = new Date(now - (total - index) * 6 * 60 * 60 * 1000)
      return time.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    case '1M':
      time = new Date(now - (total - index) * 24 * 60 * 60 * 1000)
      return time.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    default:
      return ''
  }
}

// 切换时间范围
const changeTimeRange = (range) => {
  selectedTimeRange.value = range
  updatePriceChart()
}

// 初始化图表
onMounted(() => {
  nextTick(() => {
    initPriceChart()
    initMiniChart()
  })
  
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    if (priceChart) {
      priceChart.resize()
    }
    if (miniChart) {
      miniChart.resize()
    }
  })
})

const initPriceChart = () => {
  if (!priceChartRef.value) {
    console.error('priceChartRef is not available')
    return
  }
  
  console.log('Initializing price chart...', priceChartRef.value)
  priceChart = echarts.init(priceChartRef.value)
  updatePriceChart()
}

const updatePriceChart = () => {
  if (!priceChart) return
  
  const { times, data } = generateChartData(selectedTimeRange.value)
  
  const option = {
    grid: { 
      top: 20, 
      right: 30, 
      bottom: 30, 
      left: 60 
    },
    xAxis: {
      type: 'category',
      data: times,
      axisLine: { lineStyle: { color: '#e0e0e0' } },
      axisLabel: { 
        color: '#999',
        fontSize: 11,
        interval: Math.floor(times.length / 6)
      },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f0f0f0', type: 'dashed' } },
      axisLabel: { 
        color: '#999',
        fontSize: 11,
        formatter: (value) => {
          if (value >= 1000) {
            return (value / 1000).toFixed(0) + 'k'
          }
          return value
        }
      }
    },
    series: [{
      data: data,
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
    }],
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'line',
        lineStyle: {
          color: '#4CAF50',
          type: 'dashed'
        }
      },
      formatter: (params) => {
        const item = params[0]
        return `
          <div style="font-size: 12px;">
            <div style="color: #666;">${item.axisValue}</div>
            <div style="color: #1a1a1a; font-weight: 600; margin-top: 4px;">$${item.value.toLocaleString()}</div>
          </div>
        `
      },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      padding: 12,
      textStyle: {
        color: '#1a1a1a'
      }
    }
  }
  
  priceChart.setOption(option)
}

// 初始化小型趋势图
const initMiniChart = () => {
  if (!miniChartRef.value) {
    console.error('miniChartRef is not available')
    return
  }
  
  console.log('Initializing mini chart...', miniChartRef.value)
  miniChart = echarts.init(miniChartRef.value)
  const miniData = [42000, 43500, 42800, 44200, 45000, 43800, 46000, 47500, 46800, 48500, 50000, 49500, 51000, 52500, 54496]
  
  const option = {
    grid: { top: 5, right: 5, bottom: 5, left: 5 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false },
    series: [{
      data: miniData,
      type: 'line',
      smooth: true,
      symbol: 'none',
      lineStyle: { color: '#4CAF50', width: 1.5 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(76, 175, 80, 0.3)' },
          { offset: 1, color: 'rgba(76, 175, 80, 0.05)' }
        ])
      }
    }]
  }
  
  miniChart.setOption(option)
}
</script>

<style lang="scss" scoped>
.dashboard {
  width: 100%;
  margin-top: -8px; // 微调，与侧边栏 Data Overview 按钮顶部对齐
  padding: 0 24px 24px 20px;
  animation: fadeInDashboard 0.8s ease-out;
}

@keyframes fadeInDashboard {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dashboard-layout {
  display: grid;
  grid-template-columns: 38% 62%;
  grid-template-rows: auto auto; // 两行：profit+quick-actions 对应 chart, top-movers 对应 watchlist
  gap: 20px;
  align-items: start;
  
  .left-panel {
    display: contents; // 使子元素直接参与 grid 布局
  }
  
  .right-panel {
    display: contents; // 使子元素直接参与 grid 布局
  }
}

// 左侧上部组合（profit + quick-actions）
.left-top-group {
  grid-column: 1;
  grid-row: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

// 左侧下部 top-movers
.top-movers {
  grid-column: 1;
  grid-row: 2;
}

// 右侧上部 chart-card
.chart-card {
  grid-column: 2;
  grid-row: 1;
}

// 右侧下部 watchlist
.watchlist {
  grid-column: 2;
  grid-row: 2;
}

// 卡片通用样式
.profit-card,
.quick-actions,
.top-movers,
.chart-card,
.watchlist {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

// 套利收益卡片
.profit-card {
  .profit-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
  }
  
  .profit-info {
    flex: 1;
  }
  
  .profit-label {
    color: #666;
    font-size: 13px;
    margin: 0 0 6px 0;
  }
  
  .profit-amount {
    font-size: 28px;
    font-weight: 700;
    margin: 0 0 6px 0;
    color: #1a1a1a;
  }
  
  .profit-change {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    margin-bottom: 4px;
    
    .change-icon {
      font-size: 14px;
      
      &.up { color: #4CAF50; }
      &.down { color: #F44336; }
    }
  }
  
  .revenue-text {
    color: #999;
    font-size: 12px;
    margin: 0;
  }
  
  .profit-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 8px;
  }
  
  .currency-select {
    width: 100px;
  }
  
  .mini-chart {
    margin-top: 4px;
  }
  
  .profit-actions {
    display: flex;
    gap: 10px;
    margin-top: 12px;
  }
}

// 按钮样式
.btn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
  
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
  .section-header-simple {
    margin-bottom: 16px;
    
    h3 {
      font-size: 16px;
      font-weight: 600;
      margin: 0 0 4px 0;
    }
    
    p {
      font-size: 12px;
      color: #999;
      margin: 0;
    }
  }
  
  .action-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
  }
  
  .action-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    
    .action-icon {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #4CAF50;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 20px;
      transition: transform 0.3s;
    }
    
    span {
      font-size: 12px;
      color: #666;
      font-weight: 500;
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
  margin-bottom: 12px;
  
  .section-title {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
  }
  
  .more-link {
    display: flex;
    align-items: center;
    gap: 4px;
    color: #4CAF50;
    text-decoration: none;
    font-size: 12px;
    font-weight: 500;
    
    &:hover {
      opacity: 0.8;
    }
  }
}

.compact-table {
  .table-header,
  .table-row {
    display: grid;
    grid-template-columns: 30px 2fr 1.2fr 1.2fr;
    align-items: center;
    padding: 8px 4px;
    gap: 8px;
  }
  
  .table-header {
    color: #999;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 8px;
  }
  
  .table-row {
    border-bottom: 1px solid #fafafa;
    cursor: pointer;
    transition: background 0.2s;
    font-size: 12px;
    
    &:hover {
      background: #f8f8f8;
    }
    
    &:last-child {
      border-bottom: none;
    }
  }
  
  .coin-info {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .coin-icon {
      width: 24px;
      height: 24px;
      border-radius: 50%;
    }
    
    .coin-name {
      font-weight: 600;
      font-size: 12px;
      color: #1a1a1a;
    }
    
    .coin-symbol {
      color: #999;
      font-size: 10px;
    }
  }
  
  .price {
    font-weight: 600;
    color: #1a1a1a;
  }
}

// Watchlist 表格
.watchlist {
  flex: 1;
  
  .compact-table {
    .table-header,
    .table-row {
      grid-template-columns: 30px 2fr 1fr 1fr 1.2fr;
    }
    
    .actions {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .btn-buy {
        padding: 4px 12px;
        min-width: 50px;
        background: #4CAF50;
        color: white;
        border: none;
        border-radius: 16px;
        font-size: 11px;
        font-weight: 600;
        cursor: pointer;
        white-space: nowrap;
        
        &:hover {
          background: #45A049;
        }
      }
      
      .favorite,
      .more-icon {
        font-size: 16px;
        cursor: pointer;
      }
      
      .favorite {
        color: #FFB300;
      }
      
      .more-icon {
        color: #999;
      }
    }
  }
}

// 图表卡片
.chart-card {
  display: flex;
  flex-direction: column;
  // 让图表卡片自动匹配左侧 profit + quick-actions 的总高度
  // Grid 会自动处理同一行元素的高度对齐
  height: 100%;
  
  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    flex-shrink: 0;
    
    .coin-select {
      width: 140px;
    }
    
    .currency-select-small {
      width: 80px;
    }
  }
  
  .price-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    flex-shrink: 0;
  }
  
  .price-display {
    display: flex;
    align-items: baseline;
    gap: 12px;
    
    .current-price {
      font-size: 28px;
      font-weight: 700;
      margin: 0;
      color: #1a1a1a;
    }
  }
  
  .time-range {
    display: flex;
    gap: 6px;
    
    .time-btn {
      padding: 6px 12px;
      border: 1px solid #e0e0e0;
      background: white;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s;
      color: #666;
      
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
  
  .main-chart {
    flex: 1; // 占据剩余所有空间
    min-height: 150px;
    position: relative;
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
