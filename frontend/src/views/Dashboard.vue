<template>
  <div class="dashboard">
    <!-- <Transition name="fade">
      <TruckLoader v-if="loading" :show="true" text="加载数据中..." key="dashboard-loader" />
    </Transition> -->
    <div class="dashboard-layout">
      <!-- 左侧栏 -->
      <div class="left-panel">
        <div class="left-top-group">
          <!-- 套利收益卡片 -->
          <div class="profit-card">
            <div class="profit-header">
              <div class="profit-info">
                <p class="profit-label">Total Volume (ETH)</p>
                <h2 class="profit-amount">${{ walletBalance.toLocaleString() }}</h2>
                <div class="profit-change">
                  <el-icon class="change-icon" :class="walletChange >= 0 ? 'up' : 'down'">
                    <CaretTop v-if="walletChange >= 0" />
                    <CaretBottom v-else />
                  </el-icon>
                  <span :class="walletChange >= 0 ? 'text-up' : 'text-down'">{{ walletChange }}%</span>
                </div>
                <p class="revenue-text">Total Potential Profit ${{ revenue.toLocaleString() }}</p>
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
            <h3 class="section-title">Top Arbitrage Opportunities</h3>
          </div>
          <div class="compact-table">
            <div class="table-header">
              <div class="col">#</div>
              <div class="col">{{ t('dashboard.coin') }}</div>
              <div class="col">Profit (USDT)</div>
              <div class="col">Price Diff</div>
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
                {{ priceChange >= 0 ? '+' : '' }}${{ Math.abs(priceChangeAmount).toLocaleString() }} ({{ priceChange }}%)
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
            <h3 class="section-title">Recent Arbitrage Opportunities</h3>
          </div>
          
          <div class="compact-table">
            <div class="table-header">
              <div class="col">Time</div>
              <div class="col">DEX (Uniswap)</div>
              <div class="col">CEX (Binance)</div>
              <div class="col">Profit (USDT)</div>
              <div class="col">{{ t('dashboard.actions') }}</div>
            </div>
            <div 
              v-for="(coin, index) in watchlist.slice(0, 5)" 
              :key="index"
              class="table-row"
            >
              <div class="col time-col">
                {{ new Date(coin.time).toLocaleString() }}
              </div>
              <div class="col">
                <div class="price">${{ coin.uniswap_price?.toFixed(2) }}</div>
                <div class="sub-text">Vol: {{ coin.eth_volume?.toFixed(4) }} ETH</div>
              </div>
              <div class="col">
                <div class="price">${{ coin.binance_price?.toFixed(2) }}</div>
              </div>
              <div class="col">
                <span class="text-up">
                  +${{ coin.price?.toFixed(2) }}
                </span>
              </div>
              <div class="col actions">
                <button class="btn-buy" @click="$router.push('/arbitrage-analysis')">Analyze</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts'
import { api } from '@/api'
import { store } from '@/store'
import TruckLoader from '@/components/TruckLoader.vue'
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
const walletBalance = ref(0) // Total Volume (ETH)
const walletChange = ref(0) // Placeholder
const revenue = ref(0) // Total Potential Profit
const selectedCurrency = ref('USDT')

const selectedCoin = ref('USDT/ETH')
const selectedChartCurrency = ref('USD')
const currentPrice = ref(0)
const priceChange = ref(0)
const priceChangeAmount = ref(0)
const selectedTimeRange = ref('1D') // Default to 1D, but we load full month data anyway
const timeRanges = ['1H', '4H', '12H', '1D', '1W', '1M']

const topMovers = ref([]) // Top Arbitrage Opportunities
const watchlist = ref([]) // Recent Arbitrage Opportunities

// 图表引用
const priceChartRef = ref(null)
const miniChartRef = ref(null)
let priceChart = null
let miniChart = null

const loading = ref(false)
const loadingCount = ref(0)  // 防止重复加载

// Fetch Dashboard Data
const fetchDashboardData = async () => {
  // 防止重复调用
  if (loadingCount.value > 0) {
    console.log('Already loading, skipping duplicate call')
    return
  }
  
  loadingCount.value++
  loading.value = true
  
  try {
    const start = '2025-09-01 00:00:00'
    const end = '2025-09-30 23:59:59'
    
    // 1. Fetch Statistics Overview
    const stats = await api.getStatistics(start, end)
    if (stats) {
      // Use Total Volume (ETH) as "Wallet Balance" equivalent for display
      // Since we don't have total volume in stats overview, let's sum it up from price data or just use a placeholder
      // Actually, let's use Total Potential Profit as Revenue
      revenue.value = stats.arbitrage_opportunities.total_potential_profit
      
      // For Wallet Balance, let's show Total ETH Volume from Uniswap (approx)
      // We need to fetch price data for this, or just use a placeholder based on stats
      // Let's fetch price data to calculate volumes and for the chart
    }
    
    // 2. Fetch Price Data (using cache)
    let priceData = store.getCachedPriceData(start, end)
    if (!priceData) {
      priceData = await api.getHistoricalPrices(start, end, 50000)
      store.setPriceData(priceData, start, end)
    }
    
    if (priceData && priceData.length > 0) {
      // Calculate Total Volume
      const totalEthVol = priceData.reduce((sum, item) => sum + (item.uniswap?.eth_volume || 0) + (item.binance?.eth_volume || 0), 0)
      walletBalance.value = Math.round(totalEthVol)
      
      // Update Current Price (Last record)
      const lastRecord = priceData[priceData.length - 1]
      currentPrice.value = lastRecord.binance?.price || 0
      
      // Calculate Price Change (vs first record of the month)
      const firstRecord = priceData[0]
      const firstPrice = firstRecord.binance?.price || 0
      priceChangeAmount.value = currentPrice.value - firstPrice
      priceChange.value = ((priceChangeAmount.value / firstPrice) * 100).toFixed(2)
      
      updatePriceChart(priceData)
      updateMiniChart(priceData)
    }
    
    // 3. Fetch Top Arbitrage Opportunities
    const topArb = await api.getTopArbitrage(5)
    topMovers.value = topArb.map(item => ({
      name: 'Arbitrage Opp',
      symbol: 'ETH-USDT',
      price: item.potential_profit_usdt.toFixed(2), // Show profit as price
      change: item.price_diff.toFixed(2), // Show price diff as change
      icon: 'https://cryptologos.cc/logos/ethereum-eth-logo.png?v=029',
      time: item.time
    }))
    
    // 4. Fetch Recent Arbitrage Opportunities (as Watchlist)
    // Use sortBy='time_desc' to get the most recent ones
    const recentArb = await api.getArbitrageOpportunities(start, end, 0, 5, 0, 'time_desc')
    watchlist.value = recentArb.data.map(item => ({
      name: 'Arbitrage Opp',
      symbol: 'ETH-USDT',
      price: item.potential_profit_usdt,
      change: item.price_diff,
      icon: 'https://cryptologos.cc/logos/ethereum-eth-logo.png?v=029',
      time: item.time,
      uniswap_price: item.uniswap_price,
      binance_price: item.binance_price,
      eth_volume: item.eth_volume_uniswap
    }))
    
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  } finally {
    loading.value = false
    loadingCount.value--
  }
}

// 初始化图表
onMounted(() => {
  // 先初始化图表，避免 loading 时渲染问题
  initPriceChart()
  initMiniChart()
  
  // 延迟加载数据，确保组件完全挂载
  nextTick(() => {
    setTimeout(() => {
      fetchDashboardData()
    }, 100)
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
  if (!priceChartRef.value) return
  priceChart = echarts.init(priceChartRef.value)
}

const updatePriceChart = (data) => {
  if (!priceChart || !data) return
  
  // Downsample for performance if needed, but 50k points might be okay for canvas
  // Let's take every 10th point for dashboard chart to be lighter
  const sampledData = data.filter((_, index) => index % 10 === 0)
  
  const times = sampledData.map(item => item.time)
  const prices = sampledData.map(item => item.binance?.price || 0)
  
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
        formatter: (value) => {
           const date = new Date(value)
           return `${date.getMonth() + 1}/${date.getDate()}`
        }
      },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      scale: true,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f0f0f0', type: 'dashed' } },
      axisLabel: { 
        color: '#999',
        fontSize: 11
      }
    },
    series: [{
      data: prices,
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 0,
      lineStyle: { color: '#4CAF50', width: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(76, 175, 80, 0.3)' },
          { offset: 1, color: 'rgba(76, 175, 80, 0.05)' }
        ])
      },
      emphasis: {
        focus: 'series',
        itemStyle: {
          color: '#fff',
          borderColor: '#4CAF50',
          borderWidth: 3,
          shadowBlur: 10,
          shadowColor: 'rgba(76, 175, 80, 0.5)'
        },
        symbolSize: 12
      }
    }],
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      textStyle: {
        color: '#333',
        fontSize: 12
      },
      padding: 12,
      formatter: function(params) {
        const param = params[0]
        const date = new Date(param.axisValue)
        const dateStr = `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`
        const timeStr = `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
        return `
          <div style="font-weight: 600; margin-bottom: 4px;">${dateStr}</div>
          <div style="color: #666; font-size: 11px; margin-bottom: 8px;">${timeStr}</div>
          <div style="font-size: 16px; font-weight: 700; color: #4CAF50;">$${param.value.toLocaleString()}</div>
        `
      },
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#4CAF50',
          opacity: 0.5
        },
        lineStyle: {
          color: '#4CAF50',
          type: 'solid',
          width: 1,
          opacity: 0.5
        }
      }
    }
  }
  
  priceChart.setOption(option)
}

// 初始化小型趋势图
const initMiniChart = () => {
  if (!miniChartRef.value) return
  miniChart = echarts.init(miniChartRef.value)
}

const updateMiniChart = (data) => {
  if (!miniChart || !data) return
  
  // Take last 50 points for mini chart
  const recentData = data.slice(-50).map(item => item.binance?.price || 0)
  
  const option = {
    grid: { top: 5, right: 5, bottom: 5, left: 5 },
    xAxis: { type: 'category', show: false },
    yAxis: { type: 'value', show: false, scale: true },
    series: [{
      data: recentData,
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

// 切换时间范围 (Placeholder for now, as we load full month)
const changeTimeRange = (range) => {
  selectedTimeRange.value = range
  // In a real app, we would filter data based on range
}
</script>

<style lang="scss" scoped>
.dashboard {
  width: 100%;
  margin-top: -8px; // 微调，与侧边栏 Data Overview 按钮顶部对齐
  padding: 0 24px 24px 20px;
  animation: fadeInDashboard 0.8s ease-out;
  position: relative;
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

// Transition 动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
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
      grid-template-columns: 1.5fr 1.2fr 1fr 1fr 0.8fr;
    }
    
    .time-col {
      font-size: 11px;
      color: #666;
    }
    
    .sub-text {
      font-size: 10px;
      color: #999;
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
