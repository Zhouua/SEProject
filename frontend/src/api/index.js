import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

export const api = {
  // 获取历史价格数据
  async getHistoricalPrices(start, end, limit = 1000) {
    try {
      const params = { limit }
      if (start) params.start_time = start
      if (end) params.end_time = end
      
      const response = await axios.get(`${API_BASE_URL}/api/prices/`, { params })
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
  async getArbitrageOpportunities(start, end, minProfit = 0, limit = 100) {
    try {
      const params = { limit, min_profit: minProfit, sort_by: 'profit_desc' }
      if (start) params.start_time = start
      if (end) params.end_time = end
      
      const response = await axios.get(`${API_BASE_URL}/api/arbitrage/opportunities`, { params })
      return response.data.data
    } catch (error) {
      console.error('获取套利机会失败:', error)
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
      const params = {}
      if (start) params.start_time = start
      if (end) params.end_time = end
      
      const response = await axios.get(`${API_BASE_URL}/api/statistics/summary`, { params })
      return response.data.data
    } catch (error) {
      console.error('获取统计数据失败:', error)
      return null
    }
  }
};
