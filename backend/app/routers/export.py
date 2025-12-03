from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime
import csv
import io

from ..database import get_db
from ..models import BinanceData, UniswapData, ArbitrageData

router = APIRouter(prefix="/api/export", tags=["Export"])


@router.get("/arbitrage-opportunities/csv")
async def export_arbitrage_opportunities_csv(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    min_profit: float = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    导出套利机会数据为CSV文件
    """
    # 查询套利机会
    query = (
        select(ArbitrageData, BinanceData, UniswapData)
        .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
        .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
        .where(ArbitrageData.is_arbitrage_opportunity == True)
    )
    
    if start_time:
        query = query.where(ArbitrageData.time_align >= start_time)
    if end_time:
        query = query.where(ArbitrageData.time_align <= end_time)
    if min_profit > 0:
        query = query.where(ArbitrageData.arbitrage_profit >= min_profit)
    
    query = query.order_by(ArbitrageData.time_align)
    
    result = await db.execute(query)
    records = result.all()
    
    # 创建CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入BOM以支持Excel显示中文
    output.write('\ufeff')
    
    # 写入表头
    writer.writerow([
        'Time',
        'Binance Price (USDT)',
        'Uniswap Price (USDT)',
        'Price Diff (USDT)',
        'Price Diff (%)',
        'ETH Volume (Uniswap)',
        'USDT Volume (Uniswap)',
        'Potential Profit (USDT)',
        'Strategy'
    ])
    
    # 写入数据
    for arb, bn, uni in records:
        price_diff = bn.price - uni.price
        price_diff_percent = (price_diff / uni.price * 100) if uni.price != 0 else 0
        
        writer.writerow([
            arb.time_align.isoformat(),
            round(bn.price, 4),
            round(uni.price, 4),
            round(price_diff, 4),
            round(price_diff_percent, 4),
            round(uni.eth_vol, 6),
            round(uni.usdt_vol, 2),
            round(arb.arbitrage_profit or 0, 4),
            'Buy on Uniswap → Sell on Binance'
        ])
    
    # 返回CSV文件
    output.seek(0)
    content = output.getvalue()
    
    return StreamingResponse(
        iter([content.encode('utf-8-sig')]),
        media_type="text/csv;charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename=arbitrage_opportunities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "Content-Type": "text/csv;charset=utf-8"
        }
    )


@router.get("/price-data/csv")
async def export_price_data_csv(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    limit: int = Query(50000, ge=1, le=100000),
    db: AsyncSession = Depends(get_db)
):
    """
    导出价格数据为CSV文件
    """
    # 查询Binance数据
    bn_query = select(BinanceData)
    if start_time:
        bn_query = bn_query.where(BinanceData.time_align >= start_time)
    if end_time:
        bn_query = bn_query.where(BinanceData.time_align <= end_time)
    bn_query = bn_query.order_by(BinanceData.time_align).limit(limit)
    
    # 查询Uniswap数据
    uni_query = select(UniswapData)
    if start_time:
        uni_query = uni_query.where(UniswapData.time_align >= start_time)
    if end_time:
        uni_query = uni_query.where(UniswapData.time_align <= end_time)
    uni_query = uni_query.order_by(UniswapData.time_align).limit(limit)
    
    bn_result = await db.execute(bn_query)
    uni_result = await db.execute(uni_query)
    
    bn_records = {r.time_align: r for r in bn_result.scalars().all()}
    uni_records = {r.time_align: r for r in uni_result.scalars().all()}
    
    # 合并数据（按时间对齐）
    all_times = sorted(set(bn_records.keys()) | set(uni_records.keys()))
    
    # 创建CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入BOM
    output.write('\ufeff')
    
    # 写入表头
    writer.writerow([
        'Time',
        'Binance Price (USDT)',
        'Binance ETH Volume',
        'Binance USDT Volume',
        'Uniswap Price (USDT)',
        'Uniswap ETH Volume',
        'Uniswap USDT Volume',
        'Price Diff (USDT)',
        'Price Diff (%)'
    ])
    
    # 写入数据
    for time in all_times:
        bn = bn_records.get(time)
        uni = uni_records.get(time)
        
        if bn and uni:
            price_diff = bn.price - uni.price
            price_diff_percent = (price_diff / uni.price * 100) if uni.price != 0 else 0
            
            writer.writerow([
                time.isoformat(),
                round(bn.price, 4) if bn else '',
                round(bn.eth_vol, 6) if bn else '',
                round(bn.usdt_vol, 2) if bn else '',
                round(uni.price, 4) if uni else '',
                round(uni.eth_vol, 6) if uni else '',
                round(uni.usdt_vol, 2) if uni else '',
                round(price_diff, 4),
                round(price_diff_percent, 4)
            ])
    
    # 返回CSV文件
    output.seek(0)
    content = output.getvalue()
    
    return StreamingResponse(
        iter([content.encode('utf-8-sig')]),
        media_type="text/csv;charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename=price_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "Content-Type": "text/csv;charset=utf-8"
        }
    )


@router.get("/all-data/csv")
async def export_all_data_csv(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    导出所有数据（价格+套利机会）为CSV文件
    """
    # 查询所有套利数据（包含关联的价格数据）
    query = (
        select(ArbitrageData, BinanceData, UniswapData)
        .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
        .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
    )
    
    if start_time:
        query = query.where(ArbitrageData.time_align >= start_time)
    if end_time:
        query = query.where(ArbitrageData.time_align <= end_time)
    
    query = query.order_by(ArbitrageData.time_align)
    
    result = await db.execute(query)
    records = result.all()
    
    # 创建CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入BOM
    output.write('\ufeff')
    
    # 写入表头
    writer.writerow([
        'Time',
        'Binance Price (USDT)',
        'Binance ETH Volume',
        'Binance USDT Volume',
        'Uniswap Price (USDT)',
        'Uniswap ETH Volume',
        'Uniswap USDT Volume',
        'Price Diff (USDT)',
        'Price Diff (%)',
        'Is Arbitrage Opportunity',
        'Potential Profit (USDT)'
    ])
    
    # 写入数据
    for arb, bn, uni in records:
        price_diff = bn.price - uni.price
        price_diff_percent = (price_diff / uni.price * 100) if uni.price != 0 else 0
        
        writer.writerow([
            arb.time_align.isoformat(),
            round(bn.price, 4),
            round(bn.eth_vol, 6),
            round(bn.usdt_vol, 2),
            round(uni.price, 4),
            round(uni.eth_vol, 6),
            round(uni.usdt_vol, 2),
            round(price_diff, 4),
            round(price_diff_percent, 4),
            'Yes' if arb.is_arbitrage_opportunity else 'No',
            round(arb.arbitrage_profit or 0, 4)
        ])
    
    # 返回CSV文件
    output.seek(0)
    content = output.getvalue()
    
    return StreamingResponse(
        iter([content.encode('utf-8-sig')]),
        media_type="text/csv;charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename=all_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "Content-Type": "text/csv;charset=utf-8"
        }
    )
