# backend/app/routers/arbitrage.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models import BinanceData, UniswapData, ArbitrageData, TradeData
from ..schemas import (
    ArbitrageOpportunitiesResponse,
    ArbitrageOpportunityItem,
    TopArbitrageResponse,
    TopArbitrageItem
)

router = APIRouter(prefix="/api/arbitrage", tags=["Arbitrage"])


def get_strategy_description(direction: int) -> str:
    """根据方向返回策略描述"""
    if direction == 0:
        return "Buy on Uniswap → Sell on Binance"
    else:
        return "Buy on Binance → Sell on Uniswap"


@router.get("/opportunities", response_model=ArbitrageOpportunitiesResponse)
async def get_arbitrage_opportunities(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    min_profit: float = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=50000),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("profit_desc"),
    db: AsyncSession = Depends(get_db)
):
    """
    查询满足条件的套利机会 (arbitrage_data 表)
    通过 trade_id 关联 trade_data 表获取价格和交易量
    """
    query = (
        select(ArbitrageData, TradeData)
        .join(TradeData, ArbitrageData.trade_id == TradeData.id)
    )
    if start_time:
        query = query.where(ArbitrageData.time_align >= start_time)
    if end_time:
        query = query.where(ArbitrageData.time_align <= end_time)
    if min_profit > 0:
        query = query.where(ArbitrageData.arbitrage_profit >= min_profit)

    if sort_by == "profit_desc":
        query = query.order_by(ArbitrageData.arbitrage_profit.desc())
    elif sort_by == "profit_asc":
        query = query.order_by(ArbitrageData.arbitrage_profit.asc())
    elif sort_by == "time_desc":
        query = query.order_by(ArbitrageData.time_align.desc())
    elif sort_by == "time_asc":
        query = query.order_by(ArbitrageData.time_align.asc())
    elif sort_by == "score_desc":
        query = query.order_by(ArbitrageData.score.desc())
    elif sort_by == "profit_rate_desc":
        query = query.order_by(ArbitrageData.profit_rate.desc())
    else:
        query = query.order_by(ArbitrageData.arbitrage_profit.desc())

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    records = result.all()

    data = [
        ArbitrageOpportunityItem(
            trade_id=arb.trade_id,
            time=arb.time_align.isoformat(),
            binance_price=round(trade.binance_price, 2),
            uniswap_price=round(trade.uniswap_price, 2),
            price_diff=round(trade.binance_price - trade.uniswap_price, 2),
            price_diff_percent=round((trade.binance_price - trade.uniswap_price) / trade.uniswap_price * 100, 4) if trade.uniswap_price != 0 else 0,
            eth_volume_uniswap=round(trade.uniswap_vol, 4),
            potential_profit_usdt=round(arb.arbitrage_profit or 0, 2),
            profit_rate=round(arb.profit_rate or 0, 6),
            score=round(arb.score or 0, 2),
            direction=arb.direction or 0,
            strategy=get_strategy_description(arb.direction or 0)
        )
        for arb, trade in records
    ]

    return ArbitrageOpportunitiesResponse(
        success=True,
        count=len(data),
        data=data
    )


@router.get("/top", response_model=TopArbitrageResponse)
async def get_top_arbitrage_opportunities(
    top_n: int = Query(10, ge=1, le=100),
    sort_by: str = Query("profit", description="排序依据: profit, profit_rate, score"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取Top N套利机会
    
    sort_by参数:
    - profit: 按利润排序（默认）
    - profit_rate: 按利润率排序
    - score: 按评分排序
    """
    query = (
        select(ArbitrageData, TradeData)
        .join(TradeData, ArbitrageData.trade_id == TradeData.id)
    )
    
    # 根据sort_by参数选择排序字段
    if sort_by == "profit_rate":
        query = query.order_by(ArbitrageData.profit_rate.desc())
    elif sort_by == "score":
        query = query.order_by(ArbitrageData.score.desc())
    else:  # 默认按利润排序
        query = query.order_by(ArbitrageData.arbitrage_profit.desc())
    
    query = query.limit(top_n)
    result = await db.execute(query)
    records = result.all()

    data = [
        TopArbitrageItem(
            rank=idx + 1,
            time=arb.time_align.isoformat(),
            binance_price=round(trade.binance_price, 2),
            uniswap_price=round(trade.uniswap_price, 2),
            price_diff=round(trade.binance_price - trade.uniswap_price, 2),
            eth_volume=round(trade.uniswap_vol, 4),
            potential_profit_usdt=round(arb.arbitrage_profit or 0, 2),
            profit_rate=round(arb.profit_rate or 0, 6),
            score=round(arb.score or 0, 2),
            direction=arb.direction or 0
        )
        for idx, (arb, trade) in enumerate(records)
    ]

    return TopArbitrageResponse(
        success=True,
        count=len(data),
        data=data
    )


@router.get("/stats/daily")
async def get_daily_arbitrage_stats(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import func, cast, Date

    query = (
        select(
            cast(ArbitrageData.time_align, Date).label("date"),
            func.sum(ArbitrageData.arbitrage_profit).label("total_profit"),
            func.count(ArbitrageData.id).label("count")
        )
        .group_by(cast(ArbitrageData.time_align, Date))
        .order_by(cast(ArbitrageData.time_align, Date))
    )
    if start_time:
        query = query.where(ArbitrageData.time_align >= start_time)
    if end_time:
        query = query.where(ArbitrageData.time_align <= end_time)
    result = await db.execute(query)
    records = result.all()

    data = [
        {
            "date": rec.date.isoformat(),
            "total_profit": round(rec.total_profit or 0, 2),
            "count": rec.count,
        }
        for rec in records
    ]

    return {"success": True, "data": data}
