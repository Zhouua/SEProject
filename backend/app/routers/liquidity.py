from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional, List
from datetime import datetime

from ..database import get_db
from ..models import BinanceData, UniswapData
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
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    interval: str = Query("1h"),
    db: AsyncSession = Depends(get_db)
):
    """
    基于 binance_data 和 uniswap_data 表计算流动性
    """
    query_bn = select(BinanceData).order_by(BinanceData.time_align)
    query_uni = select(UniswapData).order_by(UniswapData.time_align)

    if start_time:
        query_bn = query_bn.where(BinanceData.time_align >= start_time)
        query_uni = query_uni.where(UniswapData.time_align >= start_time)
    if end_time:
        query_bn = query_bn.where(BinanceData.time_align <= end_time)
        query_uni = query_uni.where(UniswapData.time_align <= end_time)

    # 限制防止数据过多，这里示例简单处理
    result_bn = await db.execute(query_bn.limit(5000))
    result_uni = await db.execute(query_uni.limit(5000))

    records_bn = result_bn.scalars().all()
    records_uni = result_uni.scalars().all()

    # 构造时间索引字典
    bn_map = {r.time_align: r for r in records_bn}
    uni_map = {r.time_align: r for r in records_uni}
    time_points = sorted(set(bn_map.keys()).union(uni_map.keys()))

    data = []
    for t in time_points:
        bn_rec = bn_map.get(t)
        uni_rec = uni_map.get(t)

        binance_liq = 0.0
        uniswap_liq = 0.0
        if bn_rec:
            binance_liq = bn_rec.usdt_vol + (bn_rec.eth_vol * bn_rec.price)
        if uni_rec:
            uniswap_liq = uni_rec.usdt_vol + (uni_rec.eth_vol * uni_rec.price)

        data.append(LiquidityPoint(
            time=t.isoformat(),
            binance_liquidity=round(binance_liq, 2),
            uniswap_liquidity=round(uniswap_liq, 2),
            total_liquidity=round(binance_liq + uniswap_liq, 2)
        ))

    return LiquidityAnalysisResponse(success=True, data=data)
