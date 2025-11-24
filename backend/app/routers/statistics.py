# backend/app/routers/statistics.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models import TradeData
# 🆕 导入 schemas
from ..schemas import (
    StatisticsOverviewResponse,
    StatisticsOverviewData,
    ArbitrageStatistics,
    PriceStatistics,
    ExchangePriceStatistics,
    TimeRange
)

router = APIRouter(prefix="/api/statistics", tags=["Statistics"])


@router.get("/overview", response_model=StatisticsOverviewResponse)  # 🆕
async def get_statistics_overview(
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取统计概览 - 优化版本
    """
    
    # 构建时间过滤条件
    time_filters = []
    if start_time:
        time_filters.append(TradeData.time_align >= start_time)
    if end_time:
        time_filters.append(TradeData.time_align <= end_time)
    
    # 1. 总记录数
    total_query = select(func.count(TradeData.id))
    if time_filters:
        total_query = total_query.where(and_(*time_filters))
    
    total_result = await db.execute(total_query)
    total_records = total_result.scalar() or 0
    
    # 2. 套利机会数量
    arb_count_query = select(func.count(TradeData.id)).where(
        TradeData.is_arbitrage_opportunity == True
    )
    if time_filters:
        arb_count_query = arb_count_query.where(and_(*time_filters))
    
    arb_count_result = await db.execute(arb_count_query)
    arbitrage_count = arb_count_result.scalar() or 0
    
    # 3. 套利获利统计
    profit_query = select(
        func.min(TradeData.arbitrage_profit),
        func.max(TradeData.arbitrage_profit),
        func.avg(TradeData.arbitrage_profit),
        func.sum(TradeData.arbitrage_profit)
    ).where(TradeData.is_arbitrage_opportunity == True)
    
    if time_filters:
        profit_query = profit_query.where(and_(*time_filters))
    
    profit_result = await db.execute(profit_query)
    profit_stats = profit_result.first()
    
    # 4. 价格统计
    price_query = select(
        func.min(TradeData.price_b),
        func.max(TradeData.price_b),
        func.avg(TradeData.price_b),
        func.min(TradeData.price_u),
        func.max(TradeData.price_u),
        func.avg(TradeData.price_u)
    )
    if time_filters:
        price_query = price_query.where(and_(*time_filters))
    
    price_result = await db.execute(price_query)
    price_stats = price_result.first()
    
    # 5. 时间范围
    time_query = select(
        func.min(TradeData.time_align),
        func.max(TradeData.time_align)
    )
    if time_filters:
        time_query = time_query.where(and_(*time_filters))
    
    time_result = await db.execute(time_query)
    time_range = time_result.first()
    
    # 🆕 使用 Pydantic 模型构建响应
    return StatisticsOverviewResponse(
        success=True,
        data=StatisticsOverviewData(
            total_records=total_records,
            arbitrage_opportunities=ArbitrageStatistics(
                count=arbitrage_count,
                percentage=round(arbitrage_count / total_records * 100, 2) if total_records > 0 else 0,
                min_profit=round(float(profit_stats[0]), 2) if profit_stats[0] else 0,
                max_profit=round(float(profit_stats[1]), 2) if profit_stats[1] else 0,
                avg_profit=round(float(profit_stats[2]), 2) if profit_stats[2] else 0,
                total_potential_profit=round(float(profit_stats[3]), 2) if profit_stats[3] else 0
            ),
            price_statistics=PriceStatistics(
                binance=ExchangePriceStatistics(
                    min=round(float(price_stats[0]), 2) if price_stats[0] else 0,
                    max=round(float(price_stats[1]), 2) if price_stats[1] else 0,
                    avg=round(float(price_stats[2]), 2) if price_stats[2] else 0
                ),
                uniswap=ExchangePriceStatistics(
                    min=round(float(price_stats[3]), 2) if price_stats[3] else 0,
                    max=round(float(price_stats[4]), 2) if price_stats[4] else 0,
                    avg=round(float(price_stats[5]), 2) if price_stats[5] else 0
                )
            ),
            time_range=TimeRange(
                start=time_range[0].isoformat() if time_range[0] else None,
                end=time_range[1].isoformat() if time_range[1] else None
            )
        )
    )
