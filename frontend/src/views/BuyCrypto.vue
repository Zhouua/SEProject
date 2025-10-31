<template>
  <div class="buy-crypto-page">
    <div class="buy-crypto-grid">
      <!-- 左侧内容 -->
      <div class="left-section">
        <!-- Top Traded Assets -->
        <div class="top-assets">
          <div class="section-header">
            <h3 class="section-title">Top Traded Assets</h3>
            <router-link to="/markets" class="more-link">
              More
              <el-icon><DArrowRight /></el-icon>
            </router-link>
          </div>
          
          <div class="assets-grid">
            <div 
              v-for="(asset, index) in topAssets" 
              :key="asset.symbol"
              class="asset-card"
              @click="selectAsset(asset)"
            >
              <div class="asset-rank">#{{ index + 1 }}</div>
              <img :src="asset.icon" :alt="asset.name" class="asset-icon" />
              <div class="asset-info">
                <div class="asset-name">{{ asset.name }}</div>
                <div class="asset-symbol">{{ asset.symbol }}</div>
              </div>
              <div class="asset-stats">
                <div class="asset-price">${{ asset.price }}</div>
                <div class="asset-chart">
                  <svg width="60" height="24" viewBox="0 0 60 24">
                    <path 
                      :d="generateSparkline(asset.trend)" 
                      fill="none" 
                      :stroke="asset.change >= 0 ? '#4CAF50' : '#F44336'" 
                      stroke-width="2"
                    />
                  </svg>
                </div>
                <div :class="asset.change >= 0 ? 'text-up' : 'text-down'" class="asset-change">
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

        <!-- Transaction History -->
        <div class="transaction-history">
          <div class="section-header">
            <h3 class="section-title">Transaction History</h3>
            <router-link to="/transactions" class="more-link">
              More
              <el-icon><DArrowRight /></el-icon>
            </router-link>
          </div>
          
          <div class="transaction-table">
            <div class="table-header">
              <div class="col">#</div>
              <div class="col">Transaction</div>
              <div class="col">Asset</div>
              <div class="col">Amount</div>
              <div class="col">Fee</div>
              <div class="col">Status</div>
            </div>
            
            <div 
              v-for="(tx, index) in transactions" 
              :key="index"
              class="table-row"
            >
              <div class="col">{{ index + 1 }}</div>
              <div class="col transaction-type">
                <div class="type-icon" :class="tx.type.toLowerCase()">
                  <el-icon>
                    <Bottom v-if="tx.type === 'Deposit'" />
                    <Plus v-if="tx.type === 'Buy'" />
                    <Minus v-if="tx.type === 'Sell'" />
                    <TopRight v-if="tx.type === 'Transfer'" />
                    <Top v-if="tx.type === 'Withdrawal'" />
                  </el-icon>
                </div>
                <div>
                  <div class="transaction-name">{{ tx.type }}</div>
                  <div class="transaction-id">{{ tx.id }}</div>
                </div>
              </div>
              <div class="col asset-info">
                <img :src="tx.assetIcon" :alt="tx.asset" class="asset-icon-small" />
                <div>
                  <div class="asset-name-small">{{ tx.asset }}</div>
                  <div class="asset-symbol-small">{{ tx.assetSymbol }}</div>
                </div>
              </div>
              <div class="col amount">+{{ tx.amount }}</div>
              <div class="col fee">${{ tx.fee }}</div>
              <div class="col">
                <span class="status-badge" :class="tx.status.toLowerCase()">
                  {{ tx.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：购买表单 -->
      <div class="right-section">
        <div class="buy-form-card">
          <h3 class="form-title">Buy Crypto</h3>
          
          <div class="form-group">
            <label class="form-label">I'm Buying</label>
            <div class="input-wrapper">
              <input 
                type="number" 
                class="form-input" 
                v-model="buyForm.amount"
                placeholder="0.01"
              />
              <div class="currency-badge">
                <img :src="selectedAsset.icon" class="badge-icon" />
                <span>{{ selectedAsset.symbol }}</span>
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
                v-model="buyForm.spending"
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
            1 {{ selectedAsset.symbol }} = {{ exchangeRate.toLocaleString() }} USD
          </div>

          <div class="fee-notice">
            <el-icon class="info-icon"><InfoFilled /></el-icon>
            <span><strong>500 USD</strong> is all you pay, fees included.</span>
            <a href="#" class="view-details">View details</a>
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

        <!-- Top Volume -->
        <div class="top-volume">
          <div class="section-header">
            <h3 class="section-title">Top Volume</h3>
            <router-link to="/markets" class="more-link">
              More
              <el-icon><DArrowRight /></el-icon>
            </router-link>
          </div>
          
          <div class="volume-list">
            <div 
              v-for="(coin, index) in topVolume" 
              :key="coin.symbol"
              class="volume-item"
            >
              <div class="volume-rank">{{ index + 1 }}</div>
              <img :src="coin.icon" :alt="coin.name" class="volume-icon" />
              <div class="volume-info">
                <div class="volume-name">{{ coin.name }}</div>
                <div class="volume-symbol">{{ coin.symbol }}</div>
              </div>
              <div class="volume-stats">
                <div class="volume-price">${{ coin.price }}</div>
                <div :class="coin.change >= 0 ? 'text-up' : 'text-down'" class="volume-change">
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
import { ref } from 'vue'
import { 
  CaretTop, 
  CaretBottom,
  DArrowRight,
  ArrowDown,
  ArrowRight,
  InfoFilled,
  Bottom,
  Plus,
  Minus,
  TopRight,
  Top
} from '@element-plus/icons-vue'

// 顶部热门资产
const topAssets = ref([
  { 
    name: 'Bitcoin', 
    symbol: 'BTC', 
    price: '114,884', 
    change: -0.73, 
    icon: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=029',
    trend: [30, 35, 32, 38, 36, 40, 42, 38, 35]
  },
  { 
    name: 'Ethereum', 
    symbol: 'ETH', 
    price: '4,231', 
    change: -1.06, 
    icon: 'https://cryptologos.cc/logos/ethereum-eth-logo.png?v=029',
    trend: [25, 28, 26, 30, 32, 29, 27, 25, 23]
  },
  { 
    name: 'Cardano', 
    symbol: 'ADA', 
    price: '0.9326', 
    change: 0.99, 
    icon: 'https://cryptologos.cc/logos/cardano-ada-logo.png?v=029',
    trend: [15, 17, 20, 22, 25, 28, 30, 32, 35]
  },
])

// 交易历史
const transactions = ref([
  {
    type: 'Deposit',
    id: 'TXN - 001',
    asset: 'Bitcoin',
    assetSymbol: 'BTC',
    assetIcon: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=029',
    amount: '2000.00',
    fee: '0.00',
    status: 'Completed'
  },
  {
    type: 'Buy',
    id: 'TXN - 002',
    asset: 'Tether',
    assetSymbol: 'USDT',
    assetIcon: 'https://cryptologos.cc/logos/tether-usdt-logo.png?v=029',
    amount: '0.0234',
    fee: '0.00',
    status: 'Completed'
  },
  {
    type: 'Sell',
    id: 'TXN - 003',
    asset: 'Ethereum',
    assetSymbol: 'ETH',
    assetIcon: 'https://cryptologos.cc/logos/ethereum-eth-logo.png?v=029',
    amount: '2000.00',
    fee: '1.23',
    status: 'Completed'
  },
  {
    type: 'Deposit',
    id: 'TXN - 004',
    asset: 'Bitcoin',
    assetSymbol: 'BTC',
    assetIcon: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=029',
    amount: '2000.00',
    fee: '0.00',
    status: 'Completed'
  },
  {
    type: 'Transfer',
    id: 'TXN - 005',
    asset: 'USD Coin',
    assetSymbol: 'USDC',
    assetIcon: 'https://cryptologos.cc/logos/usd-coin-usdc-logo.png?v=029',
    amount: '2000.00',
    fee: '0.00',
    status: 'Completed'
  },
  {
    type: 'Withdrawal',
    id: 'TXN - 006',
    asset: 'Bitcoin',
    assetSymbol: 'BTC',
    assetIcon: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=029',
    amount: '2000.00',
    fee: '0.00',
    status: 'Pending'
  },
])

// 购买表单
const selectedAsset = ref({
  name: 'Bitcoin',
  symbol: 'BTC',
  icon: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=029'
})

const buyForm = ref({
  amount: 0.01,
  spending: 432.51
})

const exchangeRate = ref(23876)

// Top Volume
const topVolume = ref([
  { name: 'Utrust', symbol: 'UTK', price: '1.0205', change: 12.24, icon: 'https://cryptologos.cc/logos/utrust-utk-logo.png?v=029' },
  { name: 'Metadium', symbol: 'META', price: '0.0205', change: 42.33, icon: 'https://cryptologos.cc/logos/metadium-meta-logo.png?v=029' },
  { name: 'Electroneum', symbol: 'ETN', price: '0.1406', change: 30.23, icon: 'https://cryptologos.cc/logos/electroneum-etn-logo.png?v=029' },
  { name: 'TRON', symbol: 'TRX', price: '0.2305', change: 56.63, icon: 'https://cryptologos.cc/logos/tron-trx-logo.png?v=029' },
])

// 方法
const selectAsset = (asset) => {
  selectedAsset.value = {
    name: asset.name,
    symbol: asset.symbol,
    icon: asset.icon
  }
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
.buy-crypto-page {
  width: 100%;
  height: 100%;
}

.buy-crypto-grid {
  display: grid;
  grid-template-columns: 1fr 420px;
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

// Top Traded Assets
.top-assets {
  background: white;
  border-radius: 16px;
  padding: 24px;
  
  .assets-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }
  
  .asset-card {
    position: relative;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      border-color: #4CAF50;
      box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
    }
    
    .asset-rank {
      position: absolute;
      top: 12px;
      right: 12px;
      font-size: 12px;
      font-weight: 700;
      color: #999;
      background: #f5f5f5;
      padding: 4px 8px;
      border-radius: 6px;
    }
    
    .asset-icon {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      margin-bottom: 12px;
    }
    
    .asset-info {
      margin-bottom: 16px;
      
      .asset-name {
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 4px;
      }
      
      .asset-symbol {
        color: #999;
        font-size: 13px;
      }
    }
    
    .asset-stats {
      .asset-price {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 8px;
      }
      
      .asset-chart {
        margin-bottom: 8px;
      }
      
      .asset-change {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 14px;
        font-weight: 600;
      }
    }
  }
}

// Transaction History
.transaction-history {
  background: white;
  border-radius: 16px;
  padding: 24px;
  
  .transaction-table {
    .table-header,
    .table-row {
      display: grid;
      grid-template-columns: 40px 2fr 1.5fr 1fr 1fr 1fr;
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
    
    .transaction-type {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .type-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: white;
        
        &.deposit { background: #2196F3; }
        &.buy { background: #4CAF50; }
        &.sell { background: #F44336; }
        &.transfer { background: #FF9800; }
        &.withdrawal { background: #9C27B0; }
      }
      
      .transaction-name {
        font-weight: 600;
        font-size: 14px;
      }
      
      .transaction-id {
        color: #999;
        font-size: 12px;
      }
    }
    
    .asset-info {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .asset-icon-small {
        width: 24px;
        height: 24px;
        border-radius: 50%;
      }
      
      .asset-name-small {
        font-weight: 600;
        font-size: 13px;
      }
      
      .asset-symbol-small {
        color: #999;
        font-size: 11px;
      }
    }
    
    .amount {
      font-weight: 600;
      color: #4CAF50;
    }
    
    .fee {
      color: #666;
    }
    
    .status-badge {
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 600;
      
      &.completed {
        background: #E8F5E9;
        color: #4CAF50;
      }
      
      &.pending {
        background: #FFF3E0;
        color: #FF9800;
      }
    }
  }
}

// Buy Form Card
.buy-form-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  
  .form-title {
    font-size: 20px;
    font-weight: 700;
    margin: 0 0 24px 0;
  }
  
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
  
  .fee-notice {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    background: #E8F5E9;
    border-radius: 12px;
    font-size: 13px;
    margin-bottom: 20px;
    
    .info-icon {
      color: #4CAF50;
      font-size: 18px;
    }
    
    .view-details {
      color: #4CAF50;
      text-decoration: underline;
      margin-left: auto;
    }
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

// Top Volume
.top-volume {
  background: white;
  border-radius: 16px;
  padding: 24px;
  
  .volume-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .volume-item {
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
    
    .volume-rank {
      width: 24px;
      color: #999;
      font-weight: 600;
      font-size: 14px;
    }
    
    .volume-icon {
      width: 36px;
      height: 36px;
      border-radius: 50%;
    }
    
    .volume-info {
      flex: 1;
      
      .volume-name {
        font-weight: 600;
        font-size: 14px;
      }
      
      .volume-symbol {
        color: #999;
        font-size: 12px;
      }
    }
    
    .volume-stats {
      text-align: right;
      
      .volume-price {
        font-weight: 600;
        font-size: 14px;
      }
      
      .volume-change {
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
