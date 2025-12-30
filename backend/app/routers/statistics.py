from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models import BinanceData, UniswapData, ArbitrageData, TradeData
from ..schemas import (
    StatisticsOverviewResponse,
    StatisticsOverviewData,
    ArbitrageStatistics,
    PriceStatistics,
    ExchangePriceStatistics,
    TimeRange
)

router = APIRouter(prefix="/api/statistics", tags=["Statistics"])

@router.get("/overview", response_model=StatisticsOverviewResponse)
async def get_statistics_overview(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    time_filters_trade = []
    if start_time:
        time_filters_trade.append(TradeData.time_align >= start_time)
    if end_time:
        time_filters_trade.append(TradeData.time_align <= end_time)

    time_filters_arb = []
    if start_time:
        time_filters_arb.append(ArbitrageData.time_align >= start_time)
    if end_time:
        time_filters_arb.append(ArbitrageData.time_align <= end_time)

    # 总记录数：使用 trade_data 表
    total_query = select(func.count(TradeData.id))
    if time_filters_trade:
        total_query = total_query.where(and_(*time_filters_trade))
    total_result = await db.execute(total_query)
    total_records = total_result.scalar() or 0

    # 套利机会数量：使用 arbitrage_data 表
    arb_count_query = select(func.count(ArbitrageData.id))
    if time_filters_arb:
        arb_count_query = arb_count_query.where(and_(*time_filters_arb))
    arb_count_result = await db.execute(arb_count_query)
    arbitrage_count = arb_count_result.scalar() or 0

    # 套利获利统计
    profit_query = select(
        func.min(ArbitrageData.arbitrage_profit),
        func.max(ArbitrageData.arbitrage_profit),
        func.avg(ArbitrageData.arbitrage_profit),
        func.sum(ArbitrageData.arbitrage_profit)
    )
    if time_filters_arb:
        profit_query = profit_query.where(and_(*time_filters_arb))
    profit_result = await db.execute(profit_query)
    profit_stats = profit_result.first()

    # 价格统计 - 从 trade_data 表查询
    price_stats_bn_query = select(
        func.min(TradeData.binance_price),
        func.max(TradeData.binance_price),
        func.avg(TradeData.binance_price)
    )
    if time_filters_trade:
        price_stats_bn_query = price_stats_bn_query.where(and_(*time_filters_trade))
    price_stats_bn_result = await db.execute(price_stats_bn_query)
    price_stats_bn = price_stats_bn_result.first()

    price_stats_uni_query = select(
        func.min(TradeData.uniswap_price),
        func.max(TradeData.uniswap_price),
        func.avg(TradeData.uniswap_price)
    )
    if time_filters_trade:
        price_stats_uni_query = price_stats_uni_query.where(and_(*time_filters_trade))
    price_stats_uni_result = await db.execute(price_stats_uni_query)
    price_stats_uni = price_stats_uni_result.first()

    # 时间范围 - 以 trade_data 表为主
    time_query = select(
        func.min(TradeData.time_align),
        func.max(TradeData.time_align)
    )
    if time_filters_trade:
        time_query = time_query.where(and_(*time_filters_trade))
    time_result = await db.execute(time_query)
    time_range_res = time_result.first()

    return StatisticsOverviewResponse(
        success=True,
        data=StatisticsOverviewData(
            total_records=total_records,
            arbitrage_opportunities=ArbitrageStatistics(
                count=arbitrage_count,
                percentage=round(arbitrage_count / total_records * 100, 2) if total_records > 0 else 0,
                min_profit=round(float(profit_stats[0]) if profit_stats[0] else 0, 2),
                max_profit=round(float(profit_stats[1]) if profit_stats[1] else 0, 2),
                avg_profit=round(float(profit_stats[2]) if profit_stats[2] else 0, 2),
                total_potential_profit=round(float(profit_stats[3]) if profit_stats[3] else 0, 2)
            ),
            price_statistics=PriceStatistics(
                binance=ExchangePriceStatistics(
                    min=round(float(price_stats_bn[0]) if price_stats_bn[0] else 0, 2),
                    max=round(float(price_stats_bn[1]) if price_stats_bn[1] else 0, 2),
                    avg=round(float(price_stats_bn[2]) if price_stats_bn[2] else 0, 2)
                ),
                uniswap=ExchangePriceStatistics(
                    min=round(float(price_stats_uni[0]) if price_stats_uni[0] else 0, 2),
                    max=round(float(price_stats_uni[1]) if price_stats_uni[1] else 0, 2),
                    avg=round(float(price_stats_uni[2]) if price_stats_uni[2] else 0, 2)
                )
            ),
            time_range=TimeRange(
                start=time_range_res[0].isoformat() if time_range_res[0] else None,
                end=time_range_res[1].isoformat() if time_range_res[1] else None
            )
        )
    )
