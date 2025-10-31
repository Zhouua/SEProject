<template>
  <div class="assets-page">
    <div class="assets-grid">
      <!-- 左侧内容 -->
      <div class="left-section">
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

        <!-- My Assets -->
        <div class="my-assets">
          <div class="section-header">
            <h3 class="section-title">My Assets</h3>
            <router-link to="/markets" class="more-link">
              More
              <el-icon><DArrowRight /></el-icon>
            </router-link>
          </div>
          
          <div class="assets-table">
            <div class="table-header">
              <div class="col">#</div>
              <div class="col">Assets</div>
              <div class="col">Holdings</div>
              <div class="col">Price</div>
              <div class="col">Value (USD)</div>
              <div class="col">24h Change</div>
              <div class="col">Allocation</div>
              <div class="col">Actions</div>
            </div>
            
            <div 
              v-for="(asset, index) in myAssets" 
              :key="asset.symbol"
              class="table-row"
            >
              <div class="col">{{ index + 1 }}</div>
              <div class="col asset-info">
                <img :src="asset.icon" :alt="asset.name" class="asset-icon" />
                <div>
                  <div class="asset-name">{{ asset.name }}</div>
                  <div class="asset-symbol">{{ asset.symbol }}</div>
                </div>
              </div>
              <div class="col holdings">{{ asset.holdings }}</div>
              <div class="col price">${{ asset.price }}</div>
              <div class="col value">${{ asset.value }}</div>
              <div class="col">
                <span :class="asset.change >= 0 ? 'text-up' : 'text-down'" class="change">
                  <el-icon class="change-icon">
                    <CaretTop v-if="asset.change >= 0" />
                    <CaretBottom v-else />
                  </el-icon>
                  {{ Math.abs(asset.change) }}%
                </span>
              </div>
              <div class="col allocation">{{ asset.allocation }}%</div>
              <div class="col">
                <button class="trade-btn" @click="$router.push('/trade')">Trade</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧内容 -->
      <div class="right-section">
        <!-- Portfolio Overview -->
        <div class="portfolio-card">
          <div class="section-header">
            <h3 class="section-title">Your Portfolio</h3>
            <router-link to="/markets" class="more-link">
              More
              <el-icon><DArrowRight /></el-icon>
            </router-link>
          </div>
          
          <div class="portfolio-items">
            <div 
              v-for="asset in portfolioAssets" 
              :key="asset.symbol"
              class="portfolio-item"
            >
              <img :src="asset.icon" :alt="asset.name" class="portfolio-icon" />
              <div class="portfolio-info">
                <div class="portfolio-name">{{ asset.name }}</div>
                <div class="portfolio-symbol">{{ asset.symbol }}</div>
              </div>
              <div class="portfolio-stats">
                <div class="portfolio-price">${{ asset.price }}</div>
                <div class="portfolio-chart">
                  <svg width="60" height="24" viewBox="0 0 60 24">
                    <path 
                      :d="generateSparkline(asset.trend)" 
                      fill="none" 
                      :stroke="asset.change >= 0 ? '#4CAF50' : '#F44336'" 
                      stroke-width="2"
                    />
                  </svg>
                </div>
                <div :class="asset.change >= 0 ? 'text-up' : 'text-down'" class="portfolio-change">
                  <el-icon class="change-icon">
                    <CaretTop v-if="asset.change >= 0" />
                    <CaretBottom v-else />
                  </el-icon>
                  {{ Math.abs(asset.change) }}%
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
import * as echarts from 'echarts'
import { 
  CaretTop, 
  CaretBottom,
  DArrowRight
} from '@element-plus/icons-vue'

// 钱包数据
const walletBalance = ref(54496.41)
const walletChange = ref(4.61)
const revenue = ref(4864)
const selectedCurrency = ref('USDT')

// 我的资产
const myAssets = ref([
  {
    name: 'Bitcoin',
    symbol: 'BTC',
    icon: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=029',
    holdings: '0.52 BTC',
    price: '114,884',
    value: '59,739',
    change: -1.49,
    allocation: 41.2
  },
  {
    name: 'Ethereum',
    symbol: 'ETH',
    icon: 'https://cryptologos.cc/logos/ethereum-eth-logo.png?v=029',
    holdings: '4.2 ETH',
    price: '4,231',
    value: '17,770',
    change: -1.49,
    allocation: 30.1
  },
  {
    name: 'XRP',
    symbol: 'XRP',
    icon: 'https://cryptologos.cc/logos/xrp-xrp-logo.png?v=029',
    holdings: '1200 XRP',
    price: '3.01',
    value: '3,612',
    change: -4.50,
    allocation: 6.1
  },
  {
    name: 'Tether',
    symbol: 'USDT',
    icon: 'https://cryptologos.cc/logos/tether-usdt-logo.png?v=029',
    holdings: '3000 USDT',
    price: '1.00',
    value: '3,000',
    change: 0.01,
    allocation: 5.1
  },
  {
    name: 'Shiba Inu',
    symbol: 'SHIB',
    icon: 'https://cryptologos.cc/logos/shiba-inu-shib-logo.png?v=029',
    holdings: '5,000,000 SHIB',
    price: '0.000012',
    value: '60',
    change: -2.11,
    allocation: 0.04
  },
  {
    name: 'Polygon',
    symbol: 'MATIC',
    icon: 'https://cryptologos.cc/logos/polygon-matic-logo.png?v=029',
    holdings: '900 MATIC',
    price: '0.72',
    value: '648',
    change: 3.02,
    allocation: 0.9
  },
])

// 投资组合
const portfolioAssets = ref([
  {
    name: 'Bitcoin',
    symbol: 'BTC',
    icon: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=029',
    price: '114,884',
    change: -0.73,
    trend: [30, 32, 28, 35, 33, 38, 36, 34, 32]
  },
  {
    name: 'Ethereum',
    symbol: 'ETH',
    icon: 'https://cryptologos.cc/logos/ethereum-eth-logo.png?v=029',
    price: '4,231',
    change: -1.06,
    trend: [25, 27, 24, 28, 26, 30, 28, 26, 24]
  },
  {
    name: 'Cardano',
    symbol: 'ADA',
    icon: 'https://cryptologos.cc/logos/cardano-ada-logo.png?v=029',
    price: '0.9326',
    change: 0.99,
    trend: [15, 18, 20, 22, 25, 28, 30, 33, 35]
  },
])

// 图表引用
const walletChartRef = ref(null)

// 初始化图表
onMounted(() => {
  initWalletChart()
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

const generateSparkline = (trend) => {
  const width = 60
  const height = 24
  const points = trend.map((value, index) => {
    const x = (index / (trend.length - 1)) * width
    const y = height - (value / 50) * height
    return `${x},${y}`
  }).join(' ')
  return `M ${points}`
}
</script>

<style lang="scss" scoped>
.assets-page {
  width: 100%;
  height: 100%;
}

.assets-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 24px;
  height: 100%;
}

.left-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  overflow-y: auto;
}

.right-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

// 钱包卡片
.wallet-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  
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

// 通用部分
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  
  .section-title {
    font-size: 18px;
    font-weight: 700;
    margin: 0;
  }
  
  .more-link {
    display: flex;
    align-items: center;
    gap: 4px;
    color: #4CAF50;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    
    &:hover {
      opacity: 0.8;
    }
  }
}

// My Assets
.my-assets {
  background: white;
  border-radius: 16px;
  padding: 24px;
  
  .assets-table {
    .table-header,
    .table-row {
      display: grid;
      grid-template-columns: 40px 2fr 1.2fr 1fr 1.2fr 1fr 1fr 1fr;
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
    
    .asset-info {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .asset-icon {
        width: 32px;
        height: 32px;
        border-radius: 50%;
      }
      
      .asset-name {
        font-weight: 600;
        font-size: 14px;
      }
      
      .asset-symbol {
        color: #999;
        font-size: 12px;
      }
    }
    
    .holdings,
    .price,
    .value {
      font-weight: 600;
      font-size: 14px;
    }
    
    .change {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 14px;
      font-weight: 600;
    }
    
    .allocation {
      font-weight: 600;
    }
    
    .trade-btn {
      padding: 6px 16px;
      background: #4CAF50;
      color: white;
      border: none;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.3s;
      
      &:hover {
        background: #45A049;
      }
    }
  }
}

// Portfolio Card
.portfolio-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  
  .portfolio-items {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .portfolio-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      border-color: #4CAF50;
      box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
    }
    
    .portfolio-icon {
      width: 48px;
      height: 48px;
      border-radius: 50%;
    }
    
    .portfolio-info {
      flex: 1;
      
      .portfolio-name {
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 4px;
      }
      
      .portfolio-symbol {
        color: #999;
        font-size: 13px;
      }
    }
    
    .portfolio-stats {
      text-align: right;
      
      .portfolio-price {
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 8px;
      }
      
      .portfolio-chart {
        margin-bottom: 8px;
      }
      
      .portfolio-change {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 4px;
        font-size: 13px;
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
