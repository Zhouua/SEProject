import { createI18n } from 'vue-i18n'

const messages = {
  zh: {
    header: {
      search: '搜索币种、市场或投资组合...',
      notifications: '通知'
    },
    sidebar: {
      dashboard: '仪表盘',
      trade: '交易',
      wallet: '钱包',
      markets: '市场',
      transactions: '交易记录',
      buyCrypto: '购买加密货币',
      sellCrypto: '出售加密货币',
      convert: '兑换',
      referral: '推荐',
      helpCenter: '帮助中心',
      settings: '设置'
    },
    dashboard: {
      welcome: '欢迎回来，Michael！',
      walletBalance: '钱包余额',
      revenue: '本周收益',
      deposit: '存款',
      withdraw: '提款',
      quickActions: '快速操作',
      manageInvestments: '管理您的加密货币投资',
      buy: '购买',
      sell: '出售',
      send: '发送',
      receive: '接收',
      topMovers: '涨幅榜',
      more: '更多',
      coin: '币种',
      price: '价格',
      volume24h: '24小时交易量',
      watchlist: '观察列表',
      actions: '操作'
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
      dashboard: '仪表盘',
      trade: '交易',
      wallet: '钱包',
      markets: '市场',
      transactions: '交易记录',
      buyCrypto: '购买加密货币',
      sellCrypto: '出售加密货币',
      convert: '兑换',
      referral: '推荐',
      assets: '资产',
      cryptoDetails: '加密货币详情'
    },
    trade: {
      orderBook: '订单簿',
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
      tradingAnalysis: '交易分析',
      square: '广场',
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
      change: '变化'
    }
  },
  en: {
    header: {
      search: 'Search coins, markets, or portfolio...',
      notifications: 'Notifications'
    },
    sidebar: {
      dashboard: 'Dashboard',
      trade: 'Trade',
      wallet: 'Wallet',
      markets: 'Markets',
      transactions: 'Transactions',
      buyCrypto: 'Buy Crypto',
      sellCrypto: 'Sell Crypto',
      convert: 'Convert',
      referral: 'Referral',
      helpCenter: 'Help Center',
      settings: 'Settings'
    },
    dashboard: {
      welcome: 'Welcome back, Michael!',
      walletBalance: 'Wallet Balance',
      revenue: 'Your revenue is ${amount} this week',
      deposit: 'Deposit',
      withdraw: 'Withdraw',
      quickActions: 'Quick Actions',
      manageInvestments: 'Manage your crypto investments',
      buy: 'Buy',
      sell: 'Sell',
      send: 'Send',
      receive: 'Receive',
      topMovers: 'Top Movers',
      more: 'More',
      coin: 'Coin',
      price: 'Price',
      volume24h: '24h Volume',
      watchlist: 'Watchlist',
      actions: 'Actions'
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
      dashboard: 'Dashboard',
      trade: 'Trade',
      wallet: 'Wallet',
      markets: 'Markets',
      transactions: 'Transactions',
      buyCrypto: 'Buy Crypto',
      sellCrypto: 'Sell Crypto',
      convert: 'Convert',
      referral: 'Referral',
      assets: 'Assets',
      cryptoDetails: 'Crypto Details'
    },
    trade: {
      orderBook: 'Order Book',
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
      tradingAnalysis: 'Trading Analysis',
      square: 'Square',
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
      change: 'Change'
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
