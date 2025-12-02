from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models import BinanceData, UniswapData
from ..schemas import (
    PriceListResponse,
    LatestPriceResponse,
    PriceDataItem,
    LatestPriceData,
    ExchangePriceData
)

router = APIRouter(prefix="/api/prices", tags=["Prices"])

@router.get("/", response_model=PriceListResponse)
async def get_prices(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=100000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    从 binance_data 和 uniswap_data 获取价格数据并时间对齐后响应
    """
    # 先分别获取两边数据
    query_bn = select(BinanceData).order_by(BinanceData.time_align)
    query_uni = select(UniswapData).order_by(UniswapData.time_align)

    if start_time:
        query_bn = query_bn.where(BinanceData.time_align >= start_time)
        query_uni = query_uni.where(UniswapData.time_align >= start_time)
    if end_time:
        query_bn = query_bn.where(BinanceData.time_align <= end_time)
        query_uni = query_uni.where(UniswapData.time_align <= end_time)

    # 限制结果集
    result_bn = await db.execute(query_bn.offset(offset).limit(limit))
    result_uni = await db.execute(query_uni.offset(offset).limit(limit))

    records_bn = result_bn.scalars().all()
    records_uni = result_uni.scalars().all()

    # 简单时间对齐：只匹配相同时间的条目
    bn_map = {r.time_align: r for r in records_bn}
    uni_map = {r.time_align: r for r in records_uni}
    common_times = sorted(set(bn_map.keys()).intersection(set(uni_map.keys())))

    data = []
    for t in common_times:
        bn = bn_map[t]
        uni = uni_map[t]
        price_diff = bn.price - uni.price
        price_diff_percent = ((price_diff) / uni.price * 100) if uni.price != 0 else 0

        data.append(PriceDataItem(
            time=t.isoformat(),
            binance=ExchangePriceData(
                price=round(bn.price, 2),
                eth_volume=round(bn.eth_vol, 4),
                usdt_volume=round(bn.usdt_vol, 2)
            ),
            uniswap=ExchangePriceData(
                price=round(uni.price, 2),
                eth_volume=round(uni.eth_vol, 4),
                usdt_volume=round(uni.usdt_vol, 2)
            ),
            price_diff=round(price_diff, 2),
            price_diff_percent=round(price_diff_percent, 4)
        ))

    return PriceListResponse(
        success=True,
        count=len(data),
        data=data
    )

@router.get("/latest", response_model=LatestPriceResponse)
async def get_latest_price(db: AsyncSession = Depends(get_db)):
    """获取最新价格对，取两个表中最新时间的最新记录"""
    # 查询最新时间
    last_bn = await db.execute(select(BinanceData).order_by(BinanceData.time_align.desc()).limit(1))
    last_uni = await db.execute(select(UniswapData).order_by(UniswapData.time_align.desc()).limit(1))

    bn_rec = last_bn.scalar_one_or_none()
    uni_rec = last_uni.scalar_one_or_none()

    if not bn_rec or not uni_rec:
        return LatestPriceResponse(success=False, message="No data available", data=None)

    # 选取最晚的时间作为最新时间
    latest_time = max(bn_rec.time_align, uni_rec.time_align)
    # 取对应数据（确保时间对齐）
    if bn_rec.time_align != latest_time:
        # 查询时间匹配的binance数据
        bn_res = await db.execute(
            select(BinanceData).where(BinanceData.time_align == latest_time)
        )
        bn_rec = bn_res.scalar_one_or_none()
    if uni_rec.time_align != latest_time:
        uni_res = await db.execute(
            select(UniswapData).where(UniswapData.time_align == latest_time)
        )
        uni_rec = uni_res.scalar_one_or_none()

    if not bn_rec or not uni_rec:
        return LatestPriceResponse(success=False, message="No aligned latest data", data=None)

    price_diff = bn_rec.price - uni_rec.price

    return LatestPriceResponse(
        success=True,
        data=LatestPriceData(
            time=latest_time.isoformat(),
            binance=ExchangePriceData(
                price=round(bn_rec.price, 2),
                eth_volume=round(bn_rec.eth_vol, 4),
                usdt_volume=round(bn_rec.usdt_vol, 2)
            ),
            uniswap=ExchangePriceData(
                price=round(uni_rec.price, 2),
                eth_volume=round(uni_rec.eth_vol, 4),
                usdt_volume=round(uni_rec.usdt_vol, 2)
            ),
            price_diff=round(price_diff, 2)
        )
    )


@router.get("/candles")
async def get_price_candles(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    interval: str = Query("1h"),
    db: AsyncSession = Depends(get_db)
):
    """
    按时间间隔聚合 OHLC 数据，先获取两表数据再合成K线
    """

    query_bn = select(BinanceData).order_by(BinanceData.time_align)
    query_uni = select(UniswapData).order_by(UniswapData.time_align)

    if start_time:
        query_bn = query_bn.where(BinanceData.time_align >= start_time)
        query_uni = query_uni.where(UniswapData.time_align >= start_time)
    if end_time:
        query_bn = query_bn.where(BinanceData.time_align <= end_time)
        query_uni = query_uni.where(UniswapData.time_align <= end_time)

    result_bn = await db.execute(query_bn)
    result_uni = await db.execute(query_uni)

    records_bn = result_bn.scalars().all()
    records_uni = result_uni.scalars().all()

    if not records_bn or not records_uni:
        return {"success": True, "data": []}

    candles = {}
    for record in records_bn:
        dt = record.time_align
        if interval == "1h":
            bucket = dt.replace(minute=0, second=0, microsecond=0)
        elif interval == "4h":
            hour = (dt.hour // 4) * 4
            bucket = dt.replace(hour=hour, minute=0, second=0, microsecond=0)
        elif interval == "1d":
            bucket = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            bucket = dt.replace(minute=0, second=0, microsecond=0)
        key = bucket.isoformat()

        if key not in candles:
            candles[key] = {
                "time": key,
                "binance": {"open": record.price, "high": record.price, "low": record.price, "close": record.price},
                "uniswap": {"open": None, "high": None, "low": None, "close": None}
            }
        else:
            c = candles[key]["binance"]
            c["high"] = max(c["high"], record.price)
            c["low"] = min(c["low"], record.price)
            c["close"] = record.price

    for record in records_uni:
        dt = record.time_align
        if interval == "1h":
            bucket = dt.replace(minute=0, second=0, microsecond=0)
        elif interval == "4h":
            hour = (dt.hour // 4) * 4
            bucket = dt.replace(hour=hour, minute=0, second=0, microsecond=0)
        elif interval == "1d":
            bucket = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            bucket = dt.replace(minute=0, second=0, microsecond=0)
        key = bucket.isoformat()

        if key not in candles:
            candles[key] = {
                "time": key,
                "binance": {"open": None, "high": None, "low": None, "close": None},
                "uniswap": {"open": record.price, "high": record.price, "low": record.price, "close": record.price}
            }
        else:
            c = candles[key]["uniswap"]
            if c["open"] is None:
                # If bucket exists but Uniswap data was empty (initialized by Binance loop)
                c["open"] = record.price
                c["high"] = record.price
                c["low"] = record.price
                c["close"] = record.price
            else:
                c["high"] = max(c["high"], record.price)
                c["low"] = min(c["low"], record.price)
                c["close"] = record.price

    return {"success": True, "data": list(candles.values())}
