"""
调试CSV导出问题
"""
import asyncio
from sqlalchemy import select
from datetime import datetime
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import AsyncSessionLocal
from app.models import BinanceData, UniswapData, ArbitrageData


async def check_data():
    """检查数据库中的数据"""
    
    print("=" * 60)
    print("检查数据库数据")
    print("=" * 60)
    
    async with AsyncSessionLocal() as db:
        # 检查Binance数据
        bn_query = select(BinanceData).limit(5)
        bn_result = await db.execute(bn_query)
        bn_records = bn_result.scalars().all()
        
        print(f"\nBinance数据记录数: {len(bn_records)}")
        if bn_records:
            print("前5条记录:")
            for r in bn_records:
                print(f"  时间: {r.time_align}, 价格: {r.price}, ETH量: {r.eth_vol}")
        
        # 检查Uniswap数据
        uni_query = select(UniswapData).limit(5)
        uni_result = await db.execute(uni_query)
        uni_records = uni_result.scalars().all()
        
        print(f"\nUniswap数据记录数: {len(uni_records)}")
        if uni_records:
            print("前5条记录:")
            for r in uni_records:
                print(f"  时间: {r.time_align}, 价格: {r.price}, ETH量: {r.eth_vol}")
        
        # 检查套利数据
        arb_query = select(ArbitrageData).limit(5)
        arb_result = await db.execute(arb_query)
        arb_records = arb_result.scalars().all()
        
        print(f"\n套利数据记录数: {len(arb_records)}")
        if arb_records:
            print("前5条记录:")
            for r in arb_records:
                print(f"  时间: {r.time_align}, 是否套利: {r.is_arbitrage_opportunity}, 收益: {r.arbitrage_profit}")
        
        # 检查套利机会（带join）
        query = (
            select(ArbitrageData, BinanceData, UniswapData)
            .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
            .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
            .where(ArbitrageData.is_arbitrage_opportunity == True)
            .limit(5)
        )
        
        result = await db.execute(query)
        records = result.all()
        
        print(f"\n套利机会（带价格）记录数: {len(records)}")
        if records:
            print("前5条套利机会:")
            for arb, bn, uni in records:
                print(f"  时间: {arb.time_align}")
                print(f"    Binance价格: {bn.price}, Uniswap价格: {uni.price}")
                print(f"    价差: {bn.price - uni.price}, 收益: {arb.arbitrage_profit}")
        
        # 检查2025年9月的数据
        start_time = datetime(2025, 9, 1)
        end_time = datetime(2025, 9, 30, 23, 59, 59)
        
        query_sept = (
            select(ArbitrageData)
            .where(ArbitrageData.time_align >= start_time)
            .where(ArbitrageData.time_align <= end_time)
        )
        
        result_sept = await db.execute(query_sept)
        records_sept = result_sept.scalars().all()
        
        print(f"\n2025年9月数据记录数: {len(records_sept)}")
        
        # 检查套利机会数量
        query_arb = (
            select(ArbitrageData)
            .where(ArbitrageData.time_align >= start_time)
            .where(ArbitrageData.time_align <= end_time)
            .where(ArbitrageData.is_arbitrage_opportunity == True)
        )
        
        result_arb = await db.execute(query_arb)
        records_arb = result_arb.scalars().all()
        
        print(f"2025年9月套利机会数: {len(records_arb)}")
        
    print("\n" + "=" * 60)
    print("检查完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(check_data())
