import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

export const api = {
  // 获取历史价格数据
  async getHistoricalPrices(start, end, limit = 1000) {
    try {
      const params = new URLSearchParams()
      params.append('limit', limit)
      if (start) params.append('start_time', start)
      if (end) params.append('end_time', end)

      const response = await axios.get(`${API_BASE_URL}/api/prices/?${params.toString()}`)
      return response.data.data
    } catch (error) {
      console.error('获取价格数据失败:', error)
      return []
    }
  },

  // 获取最新价格
  async getLatestPrice() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/prices/latest`)
      return response.data.data
    } catch (error) {
      console.error('获取最新价格失败:', error)
      return null
    }
  },

  // 获取套利机会
  async getArbitrageOpportunities(start, end, minProfit = 0, limit = 100, offset = 0, sortBy = 'profit_desc') {
    try {
      const params = new URLSearchParams()
      params.append('limit', limit)
      params.append('offset', offset)
      params.append('min_profit', minProfit)
      params.append('sort_by', sortBy)
      if (start) params.append('start_time', start)
      if (end) params.append('end_time', end)

      const response = await axios.get(`${API_BASE_URL}/api/arbitrage/opportunities?${params.toString()}`)
      return response.data
    } catch (error) {
      console.error('获取套利机会失败:', error)
      return { data: [], count: 0 }
    }
  },

  // 获取每日套利统计
  async getDailyArbitrageStats(start, end) {
    try {
      const params = new URLSearchParams()
      if (start) params.append('start_time', start)
      if (end) params.append('end_time', end)

      const response = await axios.get(`${API_BASE_URL}/api/arbitrage/stats/daily?${params.toString()}`)
      return response.data.data
    } catch (error) {
      console.error('获取每日套利统计失败:', error)
      return []
    }
  },

  // 获取价格K线数据
  async getPriceCandles(start, end, interval = '1h') {
    try {
      const params = new URLSearchParams()
      params.append('interval', interval)
      if (start) params.append('start_time', start)
      if (end) params.append('end_time', end)

      const response = await axios.get(`${API_BASE_URL}/api/prices/candles?${params.toString()}`)
      return response.data.data
    } catch (error) {
      console.error('获取价格K线数据失败:', error)
      return []
    }
  },

  // 获取Top套利机会
  async getTopArbitrage(topN = 10) {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/arbitrage/top`, {
        params: { top_n: topN }
      })
      return response.data.data
    } catch (error) {
      console.error('获取Top套利机会失败:', error)
      return []
    }
  },

  // 获取统计数据
  async getStatistics(start, end) {
    try {
      const params = new URLSearchParams()
      if (start) params.append('start_time', start)
      if (end) params.append('end_time', end)

      const response = await axios.get(`${API_BASE_URL}/api/statistics/overview?${params.toString()}`)
      return response.data.data
    } catch (error) {
      console.error('获取统计数据失败:', error)
      return null
    }
  },

  // 获取流动性分析数据
  async getLiquidityAnalysis(start, end, interval = '1h') {
    try {
      const params = new URLSearchParams()
      params.append('interval', interval)
      if (start) params.append('start_time', start)
      if (end) params.append('end_time', end)

      const response = await axios.get(`${API_BASE_URL}/api/liquidity/analysis?${params.toString()}`)
      return response.data.data
    } catch (error) {
      console.error('获取流动性分析数据失败:', error)
      return []
    }
  },

  // 获取 Git Commit 通知
  async getCommits(limit = 10) {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/commits/latest`, {
        params: { limit }
      })
      return response.data
    } catch (error) {
      console.error('获取提交记录失败:', error)
      return { success: false, data: [], count: 0 }
    }
  },

  // 获取未读通知数量
  async getUnreadCommitCount() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/commits/count`)
      return response.data
    } catch (error) {
      console.error('获取未读通知数失败:', error)
      return { success: false, unread_count: 0 }
    }
  }
};
