# backend/app/routers/arbitrage.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime

# 导入数据库和模型
from ..database import get_db
from ..models import TradeData
# 🆕 导入 schemas
from ..schemas import (
    ArbitrageOpportunitiesResponse,
    ArbitrageOpportunityItem,
    TopArbitrageResponse,
    TopArbitrageItem
)

router = APIRouter(prefix="/api/arbitrage", tags=["Arbitrage"])


@router.get("/opportunities", response_model=ArbitrageOpportunitiesResponse)  # 🆕
async def get_arbitrage_opportunities(
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    min_profit: float = Query(0, ge=0, description="最小获利金额（USDT）"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数量"),
    offset: int = Query(0, ge=0, description="跳过记录数量"),
    sort_by: str = Query("profit_desc", description="排序方式: profit_desc, profit_asc, time_desc, time_asc"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取套利机会列表
    """
    
    # 构建查询 - 只查询套利机会
    query = select(TradeData).where(TradeData.is_arbitrage_opportunity == True)
    
    # 添加时间范围过滤
    if start_time:
        query = query.where(TradeData.time_align >= start_time)
    if end_time:
        query = query.where(TradeData.time_align <= end_time)
    
    # 添加最小获利过滤
    if min_profit > 0:
        query = query.where(TradeData.arbitrage_profit >= min_profit)
    
    # 添加排序
    if sort_by == "profit_desc":
        query = query.order_by(TradeData.arbitrage_profit.desc())
    elif sort_by == "profit_asc":
        query = query.order_by(TradeData.arbitrage_profit.asc())
    elif sort_by == "time_desc":
        query = query.order_by(TradeData.time_align.desc())
    elif sort_by == "time_asc":
        query = query.order_by(TradeData.time_align.asc())
    else:
        query = query.order_by(TradeData.arbitrage_profit.desc())
    
    # 添加分页
    query = query.offset(offset).limit(limit)
    
    # 执行查询
    result = await db.execute(query)
    records = result.scalars().all()
    
    # 🆕 使用 Pydantic 模型构建响应
    data = [
        ArbitrageOpportunityItem(
            time=record.time_align.isoformat(),
            binance_price=round(record.price_b, 2),
            uniswap_price=round(record.price_u, 2),
            price_diff=round(record.price_b - record.price_u, 2),
            price_diff_percent=round((record.price_b - record.price_u) / record.price_u * 100, 4) if record.price_u != 0 else 0,
            eth_volume_uniswap=round(record.eth_vol_u, 4),
            potential_profit_usdt=round(record.arbitrage_profit, 2),
            strategy="Buy on Uniswap → Sell on Binance"
        )
        for record in records
    ]
    
    # 🆕 返回符合 schema 的响应
    return ArbitrageOpportunitiesResponse(
        success=True,
        count=len(data),
        data=data
    )


@router.get("/top", response_model=TopArbitrageResponse)  # 🆕
async def get_top_arbitrage_opportunities(
    top_n: int = Query(10, ge=1, le=100, description="返回前N个最佳机会"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取Top N最佳套利机会
    """
    query = (
        select(TradeData)
        .where(TradeData.is_arbitrage_opportunity == True)
        .order_by(TradeData.arbitrage_profit.desc())
        .limit(top_n)
    )
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    # 🆕 使用 Pydantic 模型构建响应
    data = [
        TopArbitrageItem(
            rank=idx + 1,
            time=record.time_align.isoformat(),
            binance_price=round(record.price_b, 2),
            uniswap_price=round(record.price_u, 2),
            price_diff=round(record.price_b - record.price_u, 2),
            eth_volume=round(record.eth_vol_u, 4),
            potential_profit_usdt=round(record.arbitrage_profit, 2)
        )
        for idx, record in enumerate(records)
    ]
    
    # 🆕 返回符合 schema 的响应
    return TopArbitrageResponse(
        success=True,
        count=len(data),
        data=data
    )
