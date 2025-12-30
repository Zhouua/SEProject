<template>
  <div class="page-container">
    <div class="help-content">
      <div class="doc-section">
        <h1 class="doc-title">区块链非原子套利交易识别</h1>
        
        <div class="doc-block">
          <h2>项目背景</h2>
          <p>本项目以 Uniswap V3 和 Binance 之间的 USDT/ETH 交易对为研究对象，通过对两边的价格数据进行分析，尝试识别其中可能存在的非原子套利行为。</p>
        </div>

        <div class="doc-block">
          <h2>项目需求</h2>
          <p>实现一个Web应用，完成如下两个核心功能:</p>
          <ol>
            <li>展示 2025 年 9 月 1 日至 9 月 30 日期间，Ethereum上Uniswap V3（USDT/ETH池）与 Binance（USDT/ETH 交易对）的历史成交数据，并对两者价格变化进行可视化对比。</li>
            <li>对 Uniswap V3与Binance之间的USDT/ETH交易数据进行分析，探索并实现识别非原子套利行为的方法，可结合启发式规则、统计分析或其他可行手段，计算潜在获利金额（以 USDT 为单位）。</li>
          </ol>
        </div>

        <div class="doc-block">
          <h2>数据来源</h2>
          <ul>
            <li>
              <strong>Uniswap V3 (USDT/ETH池)</strong>
              <p>以太坊合约地址：<a href="https://goto.etherscan.com/address/0x11b815efb8f581194ae79006d24e0d814b7697f6" target="_blank">0x11b815efB8f581194ae79006d24E0d814B7697F6</a></p>
            </li>
            <li>
              <strong>API参考文档</strong>
              <p>
                <a href="https://dune.com/home" target="_blank">Dune Analytics</a>, 
                <a href="https://thegraph.com/docs/zh/" target="_blank">The Graph</a>, 
                <a href="https://github.com/binance/binance-spot-api-docs" target="_blank">Binance API</a>, 
                <a href="https://docs.etherscan.io/" target="_blank">Etherscan</a>
              </p>
            </li>
          </ul>
        </div>

        <div class="doc-block">
          <h2>数据结构说明</h2>
          
          <h3>1. binance_data 表</h3>
          <el-table :data="binanceTableData" border style="width: 100%" class="doc-table">
            <el-table-column prop="field" label="字段名" width="120" />
            <el-table-column prop="type" label="类型" width="100" />
            <el-table-column prop="constraint" label="约束" width="180" />
            <el-table-column prop="desc" label="说明" />
          </el-table>

          <h3>2. uniswap_data 表</h3>
          <el-table :data="uniswapTableData" border style="width: 100%" class="doc-table">
            <el-table-column prop="field" label="字段名" width="120" />
            <el-table-column prop="type" label="类型" width="100" />
            <el-table-column prop="constraint" label="约束" width="180" />
            <el-table-column prop="desc" label="说明" />
          </el-table>

          <h3>3. trade_data 表</h3>
          <el-table :data="tradeTableData" border style="width: 100%" class="doc-table">
            <el-table-column prop="field" label="字段名" width="120" />
            <el-table-column prop="type" label="类型" width="100" />
            <el-table-column prop="constraint" label="约束" width="180" />
            <el-table-column prop="desc" label="说明" />
          </el-table>

          <h3>4. arbitrage_data 表</h3>
          <el-table :data="arbitrageTableData" border style="width: 100%" class="doc-table">
            <el-table-column prop="field" label="字段名" width="120" />
            <el-table-column prop="type" label="类型" width="100" />
            <el-table-column prop="constraint" label="约束" width="180" />
            <el-table-column prop="desc" label="说明" />
          </el-table>
        </div>

        <div class="doc-block">
          <h2>项目优点</h2>
          <div class="feature-grid">
            <div class="feature-item">
              <h3>🎯 核心优势</h3>
              <ul>
                <li>基于真实历史交易数据（2025年9月1-30日）进行分析</li>
                <li>实时计算 CEX（Binance）与 DEX（Uniswap V3）之间的价格差异</li>
                <li>自动识别潜在套利机会并计算收益（USDT计价）</li>
              </ul>
            </div>
            <div class="feature-item">
              <h3>🏗 全栈架构</h3>
              <ul>
                <li><strong>前端</strong>：Vue 3 + Vite 构建现代化单页应用</li>
                <li><strong>后端</strong>：FastAPI 高性能异步框架</li>
                <li><strong>数据库</strong>：PostgreSQL 存储海量交易数据</li>
              </ul>
            </div>
            <div class="feature-item">
              <h3>📊 可视化分析</h3>
              <ul>
                <li><strong>价格对比</strong>：K线图展示价格走势</li>
                <li><strong>套利分析</strong>：时间序列图展示利润趋势</li>
                <li><strong>流动性分析</strong>：多维度分析市场深度</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const binanceTableData = [
  { field: 'id', type: 'Integer', constraint: '主键、自增、单字段索引', desc: '表唯一标识' },
  { field: 'time_align', type: 'DateTime', constraint: '非空、单字段索引', desc: '对齐后的交易时间戳（格式：YYYY-MM-DD HH:MM）' },
  { field: 'price', type: 'Float', constraint: '非空', desc: 'Binance 平台 ETH 价格（USDT 计价）' },
  { field: 'eth_vol', type: 'Float', constraint: '非空', desc: 'Binance 平台 ETH 交易量（数量单位）' },
  { field: 'usdt_vol', type: 'Float', constraint: '非空', desc: 'Binance 平台 USDT 交易量（金额单位）' },
]

const uniswapTableData = [
  { field: 'id', type: 'Integer', constraint: '主键、自增、单字段索引', desc: '表唯一标识' },
  { field: 'time_align', type: 'DateTime', constraint: '非空、单字段索引', desc: '对齐后的交易时间戳（格式：YYYY-MM-DD HH:MM）' },
  { field: 'price', type: 'Float', constraint: '非空', desc: 'Uniswap 平台 ETH 价格（USDT 计价）' },
  { field: 'eth_vol', type: 'Float', constraint: '非空', desc: 'Uniswap 平台 ETH 交易量（数量单位）' },
  { field: 'usdt_vol', type: 'Float', constraint: '非空', desc: 'Uniswap 平台 USDT 交易量（金额单位）' },
]

const tradeTableData = [
  { field: 'id', type: 'Integer', constraint: '主键、自增、单字段索引', desc: '表唯一标识' },
  { field: 'time_align', type: 'DateTime', constraint: '非空、单字段索引', desc: '对齐后的交易时间戳（格式：YYYY-MM-DD HH:MM）' },
  { field: 'binance_id', type: 'Integer', constraint: '外键、非空', desc: '关联 binance_data 表的 id' },
  { field: 'uniswap_id', type: 'Integer', constraint: '外键、非空', desc: '关联 uniswap_data 表的 id' },
]

const arbitrageTableData = [
  { field: 'id', type: 'Integer', constraint: '主键、自增、单字段索引', desc: '表唯一标识' },
  { field: 'time_align', type: 'DateTime', constraint: '非空、单字段索引', desc: '对齐后的交易时间戳（格式：YYYY-MM-DD HH:MM）' },
  { field: 'binance_id', type: 'Integer', constraint: '外键、非空', desc: '关联 binance_data 表的 id' },
  { field: 'uniswap_id', type: 'Integer', constraint: '外键、非空', desc: '关联 uniswap_data 表的 id' },
  { field: 'trade_id', type: 'Integer', constraint: '外键、非空、单字段索引', desc: '关联 trade_data 表的 id' },
  { field: 'arbitrage_profit', type: 'Float', constraint: '可空', desc: '潜在套利利润（USDT）' },
  { field: 'profit_rate', type: 'Float', constraint: '可空', desc: '利润率' },
  { field: 'score', type: 'Float', constraint: '可空', desc: '多因子评分' },
  { field: 'direction', type: 'Integer', constraint: '可空', desc: '套利方向（0=U2B, 1=B2U）' },
]
</script>

<style lang="scss" scoped>
.page-container {
  padding: var(--spacing-lg) var(--spacing-xl);
  max-width: 1200px;
  margin: 0 auto;
}

.help-content {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.doc-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-border);
}

.doc-block {
  margin-bottom: 40px;
  
  h2 {
    font-size: 20px;
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    
    &::before {
      content: '';
      display: block;
      width: 4px;
      height: 20px;
      background: #4CAF50;
      margin-right: 12px;
      border-radius: 2px;
    }
  }
  
  p {
    font-size: 15px;
    line-height: 1.6;
    color: var(--color-text-secondary);
    margin-bottom: 12px;
  }
  
  ul, ol {
    padding-left: 24px;
    margin-bottom: 16px;
    
    li {
      margin-bottom: 8px;
      color: var(--color-text-secondary);
      line-height: 1.6;
    }
  }
  
  a {
    color: #4CAF50;
    text-decoration: none;
    font-weight: 500;
    
    &:hover {
      text-decoration: underline;
    }
  }
}

.doc-table {
  margin-top: 16px;
  margin-bottom: 24px;
}

h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 24px 0 12px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  
  .feature-item {
    background: var(--color-bg-tertiary);
    padding: 24px;
    border-radius: 12px;
    
    h3 {
      margin-top: 0;
      color: var(--color-text-primary);
    }
    
    ul {
      margin-bottom: 0;
    }
  }
}
</style>
