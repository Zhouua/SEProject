// Mock API service
// In a real application, this would fetch data from the backend

export const api = {
  // Fetch historical prices for comparison
  // start, end: Date strings or timestamps
  async getHistoricalPrices(start, end) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Generate mock data for Sept 2025
    const data = [];
    const startDate = new Date('2025-09-01');
    const endDate = new Date('2025-09-30');
    
    for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
      const dateStr = d.toISOString().split('T')[0];
      // Base price around 2000-3000 for ETH
      const basePrice = 2500 + Math.random() * 500;
      
      data.push({
        date: dateStr,
        uniswap: basePrice + (Math.random() - 0.5) * 20, // Slight difference
        binance: basePrice + (Math.random() - 0.5) * 20
      });
    }
    
    return data;
  },

  // Fetch arbitrage opportunities
  async getArbitrageOpportunities(start, end) {
    await new Promise(resolve => setTimeout(resolve, 500));

    const opportunities = [];
    const startDate = new Date('2025-09-01');
    const endDate = new Date('2025-09-30');

    for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
        // Randomly generate 0-3 opportunities per day
        const count = Math.floor(Math.random() * 4);
        for(let i=0; i<count; i++) {
            const profit = Math.random() * 100 + 10; // 10 - 110 USDT
            opportunities.push({
                id: Math.random().toString(36).substr(2, 9),
                timestamp: new Date(d.getTime() + Math.random() * 86400000).toISOString(),
                profit: parseFloat(profit.toFixed(2)),
                path: Math.random() > 0.5 ? 'Uniswap -> Binance' : 'Binance -> Uniswap',
                amount: parseFloat((Math.random() * 10 + 1).toFixed(4)) // 1 - 11 ETH
            });
        }
    }
    
    return opportunities.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  }
};
