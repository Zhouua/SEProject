from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional, List
from datetime import datetime

from ..database import get_db
from ..models import TradeData
from pydantic import BaseModel

router = APIRouter(prefix="/api/liquidity", tags=["Liquidity"])

class LiquidityPoint(BaseModel):
    time: str
    binance_liquidity: float
    uniswap_liquidity: float
    total_liquidity: float

class LiquidityAnalysisResponse(BaseModel):
    success: bool
    data: List[LiquidityPoint]

@router.get("/analysis", response_model=LiquidityAnalysisResponse)
async def get_liquidity_analysis(
    start_time: Optional[datetime] = Query(None, description="Start time"),
    end_time: Optional[datetime] = Query(None, description="End time"),
    interval: str = Query("1h", description="Aggregation interval: 1h, 4h, 1d"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get liquidity analysis data based on volume.
    Liquidity is approximated by the sum of ETH and USDT volume.
    """
    
    # Determine time grouping based on interval
    # Note: SQLite (which might be used locally) has different date functions than PostgreSQL
    # Assuming PostgreSQL for now based on readme, but will try to write generic SQL or use Python aggregation if needed.
    # For simplicity and compatibility, let's fetch data and aggregate in Python for now, 
    # or use simple grouping if the dataset is large. 
    # Given the requirements, let's try to return raw data points if the range is small, 
    # or aggregate if it's large. 
    # Let's stick to a simple query first.
    
    query = select(TradeData).order_by(TradeData.time_align)
    
    if start_time:
        query = query.where(TradeData.time_align >= start_time)
    if end_time:
        query = query.where(TradeData.time_align <= end_time)
        
    # Limit to avoid fetching too much data if no time range
    if not start_time and not end_time:
        query = query.limit(1000)

    result = await db.execute(query)
    records = result.scalars().all()
    
    data = []
    for record in records:
        # Approximate liquidity as (ETH volume * Price) + USDT volume
        # Or just sum of volumes if we want a rough indicator. 
        # Let's use USDT volume + (ETH volume * Price) for total value locked/traded approximation.
        
        binance_liq = record.usdt_vol_b + (record.eth_vol_b * record.price_b)
        uniswap_liq = record.usdt_vol_u + (record.eth_vol_u * record.price_u)
        
        data.append(LiquidityPoint(
            time=record.time_align.isoformat(),
            binance_liquidity=round(binance_liq, 2),
            uniswap_liquidity=round(uniswap_liq, 2),
            total_liquidity=round(binance_liq + uniswap_liq, 2)
        ))
        
    return LiquidityAnalysisResponse(
        success=True,
        data=data
    )
