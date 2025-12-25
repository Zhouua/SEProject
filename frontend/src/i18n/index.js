import { createI18n } from 'vue-i18n'

const messages = {
  zh: {
    common: {
      startDate: '开始日期',
      endDate: '结束日期'
    },
    chart: {
      candlestickInfo: 'K线图与成交量指标'
    },
    header: {
      search: '搜索交易对、数据或分析...',
      notifications: '通知'
    },
    sidebar: {
      dashboard: '数据概览',
      priceComparison: {
        title: '价格对比'
      },
      arbitrage: {
        title: '套利分析'
      },
      volumeComparison: '交易量对比',
      liquidityAnalysis: '流动性分析',
      markets: '市场数据',
      transactions: '交易记录',
      buyCrypto: 'Uniswap V3 数据',
      sellCrypto: 'Binance 数据',
      convert: '数据导出',
      referral: '关于项目',
      helpCenter: '帮助中心',
      settings: '设置'
    },
    dashboard: {
      welcome: '欢迎使用套利分析系统！',
      subtitle: 'Uniswap V3 vs Binance 套利机会分析',
      dateRange: '数据时间范围：2025年9月1日 - 9月30日',
      tradingPair: 'USDT/ETH',
      uniswapPool: 'Uniswap V3 池地址',
      poolAddress: '0x11b815efB8f581194ae79006d24E0d814B7697F6',
      walletBalance: '潜在套利收益',
      revenue: '本月收益',
      deposit: '刷新数据',
      withdraw: '导出报告',
      quickActions: '快速操作',
      manageInvestments: '分析 Uniswap V3 与 Binance 之间的套利机会',
      buy: 'Uniswap 数据',
      sell: 'Binance 数据',
      send: '价格对比',
      receive: '套利分析',
      topMovers: '最大价差记录',
      more: '更多',
      coin: '交易对',
      price: '价格',
      volume24h: '24小时交易量',
      watchlist: '套利机会监控',
      actions: '操作',
      priceDiff: '价差',
      arbitrageProfit: '套利收益 (USDT)',
      exportDialog: {
        title: '导出报告',
        selectType: '选择导出类型：',
        pdfReport: 'PDF 报告',
        pdfDesc: '导出 Dashboard 所有图表为 PDF 文件',
        csvData: 'CSV 数据',
        arbitrageCSV: '套利机会 CSV',
        arbitrageDesc: '导出所有套利机会数据',
        priceCSV: '价格数据 CSV',
        priceDesc: '导出所有价格数据',
        allDataCSV: '完整数据 CSV',
        allDataDesc: '导出完整数据（价格+套利）',
        statsCSV: '统计数据 CSV',
        statsDesc: '导出统计数据概览',
        close: '关闭'
      }
    },
    notification: {
      title: '通知中心',
      close: '关闭',
      markAllRead: '全部标记为已读',
      noNotifications: '暂无通知',
      new: '新',
      timeAgo: {
        justNow: '刚刚',
        minutesAgo: '{n} 分钟前',
        hoursAgo: '{n} 小时前',
        daysAgo: '{n} 天前'
      }
    },
    routes: {
      dashboard: '数据概览',
      trade: '价格对比',
      wallet: '套利分析',
      markets: '市场数据',
      transactions: '交易记录',
      buyCrypto: 'Uniswap V3 数据',
      sellCrypto: 'Binance 数据',
      convert: '数据导出',
      referral: '关于项目',
      assets: '资产',
      cryptoDetails: '交易详情'
    },
    trade: {
      title: 'Uniswap V3 vs Binance 价格对比',
      uniswap: 'Uniswap V3',
      binance: 'Binance',
      orderBook: '交易记录',
      price: '价格',
      amount: '数量',
      total: '总计',
      change24h: '24小时变化',
      high24h: '24小时最高',
      low24h: '24小时最低',
      volume24hBTC: '24小时成交量 (BTC)',
      volume24hUSD: '24小时成交量 (USD)',
      chart: '图表',
      info: '信息',
      tradingData: '交易数据',
      tradingAnalysis: '套利分析',
      square: '数据源',
      spot: '现货',
      cross: '全仓',
      isolated: '逐仓',
      grid: '网格',
      market: '市价',
      limit: '限价',
      stopLimit: '止损限价',
      stop: '止损',
      open: '开盘',
      high: '最高',
      low: '最低',
      close: '收盘',
      change: '变化',
      priceDifference: '价差',
      arbitrageOpportunity: '套利机会'
    },
    markets: {
      saveTime: '节省买家时间',
      adoptionRate: '采用参考率',
      profitMargin: '增强卖家私有域',
      efficiency: 'AOB 升级'
    },
    welcome: {
      dataAccuracy: '数据准确性',
      timeCoverage: '7x24小时覆盖率',
      endToEndLatency: '端到端延迟',
      apiResponseTime: 'API响应时间(P95)',
      scrollDown: '向下滚动或点击查看更多'
    },
    volumeComparison: {
      binanceVolume: 'Binance 交易量',
      uniswapVolume: 'Uniswap 交易量',
      volumeRatio: '交易量比率',
      binanceUniswap: 'Binance / Uniswap',
      ethVolumeComparison: 'ETH 交易量对比',
      usdtVolumeComparison: 'USDT 交易量对比',
      volumeCorrelation: '交易量相关性 (ETH vs USDT)',
      volumeCorrelationDesc: '交易规模与价值的相关性',
      ethVolume: 'ETH 交易量',
      usdtVolume: 'USDT 交易量',
      binance: 'Binance',
      uniswap: 'Uniswap'
    },
    liquidityAnalysis: {
      avgVolumePerMin: '每分钟平均交易量',
      totalVolume: '总交易量',
      liquidityScore: '流动性评分',
      cex: 'CEX',
      dex: 'DEX',
      liquidityTrend: '流动性趋势 (USDT)',
      liquidityTrendDesc: '随时间变化的总流动性价值',
      hourlyVolumeComparison: '每小时交易量对比',
      liquidityDistribution: '流动性分布',
      priceVolatilityAnalysis: '价格波动分析',
      priceVolatilityDesc: '每小时价格变化百分比',
      binance: 'Binance',
      uniswap: 'Uniswap'
    },
    arbitrageAnalysis: {
      totalOpportunities: '总机会数',
      totalPotentialProfit: '总潜在收益',
      avgProfitPerTrade: '平均每笔收益',
      dailyProfitTrend: '每日收益趋势',
      profitDistribution: '收益分布',
      opportunityLog: '机会记录',
      time: '时间',
      strategy: '策略',
      volumeEth: '交易量 (ETH)',
      profitUsdt: '收益 (USDT)',
      triangularArbitrage: '三角套利',
      profitRange: '收益范围'
    }
  },
  en: {
    common: {
      startDate: 'Start Date',
      endDate: 'End Date'
    },
    chart: {
      candlestickInfo: 'Candlestick chart with volume indicators'
    },
    header: {
      search: 'Search pairs, data, or analysis...',
      notifications: 'Notifications'
    },
    sidebar: {
      dashboard: 'Data Overview',
      priceComparison: {
        title: 'Price Comparison'
      },
      arbitrage: {
        title: 'Arbitrage Analysis'
      },
      volumeComparison: 'Volume Comparison',
      liquidityAnalysis: 'Liquidity Analysis',
      markets: 'Market Data',
      transactions: 'Transactions',
      buyCrypto: 'Uniswap V3 Data',
      sellCrypto: 'Binance Data',
      convert: 'Export Data',
      referral: 'About Project',
      helpCenter: 'Help Center',
      settings: 'Settings'
    },
    dashboard: {
      welcome: 'Welcome to Arbitrage Analysis System!',
      subtitle: 'Uniswap V3 vs Binance Arbitrage Opportunities',
      dateRange: 'Data Period: Sep 1, 2025 - Sep 30, 2025',
      tradingPair: 'USDT/ETH',
      uniswapPool: 'Uniswap V3 Pool Address',
      poolAddress: '0x11b815efB8f581194ae79006d24E0d814B7697F6',
      walletBalance: 'Potential Arbitrage Profit',
      revenue: 'Monthly Revenue',
      deposit: 'Refresh Data',
      withdraw: 'Export Report',
      quickActions: 'Quick Actions',
      manageInvestments: 'Analyze arbitrage opportunities between Uniswap V3 and Binance',
      buy: 'Uniswap Data',
      sell: 'Binance Data',
      send: 'Price Compare',
      receive: 'Arbitrage Analysis',
      topMovers: 'Largest Price Differences',
      more: 'More',
      coin: 'Trading Pair',
      price: 'Price',
      volume24h: '24h Volume',
      watchlist: 'Arbitrage Opportunities',
      actions: 'Actions',
      priceDiff: 'Price Diff',
      arbitrageProfit: 'Arbitrage Profit (USDT)'
    },
    notification: {
      title: 'Notification Center',
      close: 'Close',
      markAllRead: 'Mark all as read',
      noNotifications: 'No notifications',
      new: 'NEW',
      timeAgo: {
        justNow: 'Just now',
        minutesAgo: '{n} minutes ago',
        hoursAgo: '{n} hours ago',
        daysAgo: '{n} days ago'
      }
    },
    routes: {
      dashboard: 'Data Overview',
      trade: 'Price Comparison',
      wallet: 'Arbitrage Analysis',
      markets: 'Market Data',
      transactions: 'Transactions',
      buyCrypto: 'Uniswap V3 Data',
      sellCrypto: 'Binance Data',
      convert: 'Export Data',
      referral: 'About Project',
      assets: 'Assets',
      cryptoDetails: 'Transaction Details'
    },
    trade: {
      title: 'Uniswap V3 vs Binance Price Comparison',
      uniswap: 'Uniswap V3',
      binance: 'Binance',
      orderBook: 'Transaction Records',
      price: 'Price',
      amount: 'Amount',
      total: 'Total',
      change24h: '24h Change',
      high24h: '24h High',
      low24h: '24h Low',
      volume24hBTC: '24h Volume (BTC)',
      volume24hUSD: '24h Volume (USD)',
      chart: 'Chart',
      info: 'Info',
      tradingData: 'Trading Data',
      tradingAnalysis: 'Arbitrage Analysis',
      square: 'Data Source',
      spot: 'Spot',
      cross: 'Cross',
      isolated: 'Isolated',
      grid: 'Grid',
      market: 'Market',
      limit: 'Limit',
      stopLimit: 'Stop Limit',
      stop: 'Stop',
      open: 'Open',
      high: 'High',
      low: 'Low',
      close: 'Close',
      change: 'Change',
      priceDifference: 'Price Diff',
      arbitrageOpportunity: 'Arbitrage Opportunity'
    },
    markets: {
      saveTime: 'Save buyer time',
      adoptionRate: 'Adoption reference rate',
      profitMargin: 'Enhance seller\'s private domain',
      efficiency: 'AOB Upgrade'
    },
    welcome: {
      dataAccuracy: 'Data Accuracy',
      timeCoverage: '7x24h Coverage',
      endToEndLatency: 'End-to-End Latency',
      apiResponseTime: 'API Response Time (P95)',
      scrollDown: 'Scroll down or click for more'
    },
    volumeComparison: {
      binanceVolume: 'Binance Volume',
      uniswapVolume: 'Uniswap Volume',
      volumeRatio: 'Volume Ratio',
      binanceUniswap: 'Binance / Uniswap',
      ethVolumeComparison: 'ETH Volume Comparison',
      usdtVolumeComparison: 'USDT Volume Comparison',
      volumeCorrelation: 'Volume Correlation (ETH vs USDT)',
      volumeCorrelationDesc: 'Correlation between trade size and value',
      ethVolume: 'ETH Volume',
      usdtVolume: 'USDT Volume',
      binance: 'Binance',
      uniswap: 'Uniswap'
    },
    liquidityAnalysis: {
      avgVolumePerMin: 'Avg. Volume / Min',
      totalVolume: 'Total Volume',
      liquidityScore: 'Liquidity Score',
      cex: 'CEX',
      dex: 'DEX',
      liquidityTrend: 'Liquidity Trend (USDT)',
      liquidityTrendDesc: 'Total liquidity value over time',
      hourlyVolumeComparison: 'Hourly Volume Comparison',
      liquidityDistribution: 'Liquidity Distribution',
      priceVolatilityAnalysis: 'Price Volatility Analysis',
      priceVolatilityDesc: 'Hourly price change percentage',
      binance: 'Binance',
      uniswap: 'Uniswap'
    },
    arbitrageAnalysis: {
      totalOpportunities: 'Total Opportunities',
      totalPotentialProfit: 'Total Potential Profit',
      avgProfitPerTrade: 'Avg. Profit / Trade',
      dailyProfitTrend: 'Daily Profit Trend',
      profitDistribution: 'Profit Distribution',
      opportunityLog: 'Opportunity Log',
      time: 'Time',
      strategy: 'Strategy',
      volumeEth: 'Volume (ETH)',
      profitUsdt: 'Profit (USDT)',
      triangularArbitrage: 'Triangular Arbitrage',
      profitRange: 'Profit Range'
    }
  }
}

const i18n = createI18n({
  legacy: false,
  locale: 'zh',
  fallbackLocale: 'en',
  messages
})

export default i18n
