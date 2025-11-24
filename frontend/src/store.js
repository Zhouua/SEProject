import { reactive } from 'vue'

export const store = reactive({
    priceDataCache: {
        data: [],
        startTime: null,
        endTime: null
    },

    setPriceData(data, start, end) {
        this.priceDataCache.data = data
        this.priceDataCache.startTime = start
        this.priceDataCache.endTime = end
    },

    getCachedPriceData(start, end) {
        if (
            this.priceDataCache.data.length > 0 &&
            this.priceDataCache.startTime === start &&
            this.priceDataCache.endTime === end
        ) {
            return this.priceDataCache.data
        }
        return null
    },

    clearCache() {
        this.priceDataCache.data = []
        this.priceDataCache.startTime = null
        this.priceDataCache.endTime = null
    }
})
