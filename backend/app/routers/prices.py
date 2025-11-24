# backend/app/routers/prices.py
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
    PriceListResponse,
    LatestPriceResponse,
    PriceDataItem,
    LatestPriceData,
    ExchangePriceData
)

router = APIRouter(prefix="/api/prices", tags=["Prices"])


@router.get("/", response_model=PriceListResponse)  # 🆕 添加 response_model
async def get_prices(
    start_time: Optional[datetime] = Query(None, description="开始时间 (YYYY-MM-DD HH:MM:SS)"),
    end_time: Optional[datetime] = Query(None, description="结束时间 (YYYY-MM-DD HH:MM:SS)"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数量"),
    offset: int = Query(0, ge=0, description="跳过记录数量"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取价格数据
    
    - **start_time**: 开始时间（可选）
    - **end_time**: 结束时间（可选）
    - **limit**: 返回记录数量（默认100，最大1000）
    - **offset**: 分页偏移量（默认0）
    """
    
    # 构建查询
    query = select(TradeData).order_by(TradeData.time_align)
    
    # 添加时间范围过滤
    if start_time:
        query = query.where(TradeData.time_align >= start_time)
    if end_time:
        query = query.where(TradeData.time_align <= end_time)
    
    # 添加分页
    query = query.offset(offset).limit(limit)
    
    # 执行查询
    result = await db.execute(query)
    records = result.scalars().all()
    
    # 🆕 使用 Pydantic 模型构建响应
    data = [
        PriceDataItem(
            time=record.time_align.isoformat(),
            binance=ExchangePriceData(
                price=round(record.price_b, 2),
                eth_volume=round(record.eth_vol_b, 4),
                usdt_volume=round(record.usdt_vol_b, 2)
            ),
            uniswap=ExchangePriceData(
                price=round(record.price_u, 2),
                eth_volume=round(record.eth_vol_u, 4),
                usdt_volume=round(record.usdt_vol_u, 2)
            ),
            price_diff=round(record.price_b - record.price_u, 2),
            price_diff_percent=round((record.price_b - record.price_u) / record.price_u * 100, 4) if record.price_u != 0 else 0
        )
        for record in records
    ]
    
    # 🆕 返回符合 schema 的响应
    return PriceListResponse(
        success=True,
        count=len(data),
        data=data
    )


@router.get("/latest", response_model=LatestPriceResponse)  # 🆕 添加 response_model
async def get_latest_price(db: AsyncSession = Depends(get_db)):
    """
    获取最新的价格数据
    """
    query = select(TradeData).order_by(TradeData.time_align.desc()).limit(1)
    result = await db.execute(query)
    record = result.scalar_one_or_none()
    
    if not record:
        # 🆕 使用 schema 返回错误响应
        return LatestPriceResponse(
            success=False,
            message="No data available",
            data=None
        )
    
    # 🆕 使用 Pydantic 模型构建响应
    return LatestPriceResponse(
        success=True,
        data=LatestPriceData(
            time=record.time_align.isoformat(),
            binance=ExchangePriceData(
                price=round(record.price_b, 2),
                eth_volume=round(record.eth_vol_b, 4),
                usdt_volume=round(record.usdt_vol_b, 2)
            ),
            uniswap=ExchangePriceData(
                price=round(record.price_u, 2),
                eth_volume=round(record.eth_vol_u, 4),
                usdt_volume=round(record.usdt_vol_u, 2)
            ),
            price_diff=round(record.price_b - record.price_u, 2)
        )
    )
