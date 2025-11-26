# backend/app/api.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Arbitrage Analysis Backend API"}

async def get_trades(start_date: str, end_date: str):
    # 这里暂时返回模拟数据，后续接数据库或外部API
    sample_data = [
        {"timestamp": "2025-09-01T00:00:00Z", "exchange": "Uniswap V3", "price": 1800.5, "volume": 10.0},
        {"timestamp": "2025-09-01T00:05:00Z", "exchange": "Binance", "price": 1801.0, "volume": 8.0},
    ]
    return sample_data
