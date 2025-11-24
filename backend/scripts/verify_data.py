import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import select, func
from app.database import AsyncSessionLocal, engine
from app.models import TradeData

async def verify_database():
    """
    验证数据库数据的完整性和正确性
    """
    print("=" * 60)
    print("🔍 Database Data Verification Report")
    print("=" * 60)
    
    async with AsyncSessionLocal() as session:
        try:
            # 1. 总记录数
            result = await session.execute(select(func.count(TradeData.id)))
            total_count = result.scalar()
            print(f"\n📊 Total Records: {total_count}")
            
            # 2. 套利机会统计
            result = await session.execute(
                select(func.count(TradeData.id)).where(TradeData.is_arbitrage_opportunity == True)
            )
            arbitrage_count = result.scalar()
            arbitrage_percentage = (arbitrage_count / total_count * 100) if total_count > 0 else 0
            print(f"💰 Arbitrage Opportunities: {arbitrage_count} ({arbitrage_percentage:.2f}%)")
            
            # 3. 时间范围
            result = await session.execute(
                select(func.min(TradeData.time_align), func.max(TradeData.time_align))
            )
            time_range = result.first()
            print(f"📅 Time Range: {time_range[0]} to {time_range[1]}")
            
            # 4. 价格统计
            result = await session.execute(
                select(
                    func.min(TradeData.price_b),
                    func.max(TradeData.price_b),
                    func.avg(TradeData.price_b),
                    func.min(TradeData.price_u),
                    func.max(TradeData.price_u),
                    func.avg(TradeData.price_u)
                )
            )
            price_stats = result.first()
            print(f"\n💵 Binance Price - Min: {price_stats[0]:.2f}, Max: {price_stats[1]:.2f}, Avg: {price_stats[2]:.2f}")
            print(f"💵 Uniswap Price - Min: {price_stats[3]:.2f}, Max: {price_stats[4]:.2f}, Avg: {price_stats[5]:.2f}")
            
            # 5. 套利获利统计
            result = await session.execute(
                select(
                    func.min(TradeData.arbitrage_profit),
                    func.max(TradeData.arbitrage_profit),
                    func.avg(TradeData.arbitrage_profit)
                ).where(TradeData.is_arbitrage_opportunity == True)
            )
            profit_stats = result.first()
            if profit_stats[0] is not None:
                print(f"💎 Arbitrage Profit (USDT) - Min: {profit_stats[0]:.2f}, Max: {profit_stats[1]:.2f}, Avg: {profit_stats[2]:.2f}")
            
            # 6. 检查是否有NULL值
            result = await session.execute(
                select(func.count(TradeData.id)).where(
                    (TradeData.price_b == None) | 
                    (TradeData.price_u == None) |
                    (TradeData.eth_vol_b == None) |
                    (TradeData.eth_vol_u == None)
                )
            )
            null_count = result.scalar()
            print(f"⚠️  Records with NULL values: {null_count}")
            
            # 7. 显示前5条数据样本
            print(f"📋 Sample Data (First 5 records):")
            print("-" * 60)
            result = await session.execute(
                select(TradeData).order_by(TradeData.time_align).limit(5)
            )
            samples = result.scalars().all()
            
            for i, record in enumerate(samples, 1):
                print(f"\n{i}. Time: {record.time_align}")
                print(f"   Binance: Price={record.price_b:.2f}, ETH_Vol={record.eth_vol_b:.4f}")
                print(f"   Uniswap: Price={record.price_u:.2f}, ETH_Vol={record.eth_vol_u:.4f}")
                print(f"   Arbitrage: Profit={record.arbitrage_profit:.2f} USDT, Opportunity={record.is_arbitrage_opportunity}")
            
            # 8. 显示最大套利机会
            print(f"🏆 Top 5 Arbitrage Opportunities:")
            print("-" * 60)
            result = await session.execute(
                select(TradeData)
                .where(TradeData.is_arbitrage_opportunity == True)
                .order_by(TradeData.arbitrage_profit.desc())
                .limit(5)
            )
            top_opportunities = result.scalars().all()
            
            for i, record in enumerate(top_opportunities, 1):
                print(f"{i}. Time: {record.time_align}")
                print(f"   Price Diff: Binance={record.price_b:.2f}, Uniswap={record.price_u:.2f}")
                print(f"   ETH Volume (Uniswap): {record.eth_vol_u:.4f}")
                print(f"   💰 Potential Profit: {record.arbitrage_profit:.2f} USDT")
            
            # 9. 验证套利计算公式
            print(f"🧮 Verifying Arbitrage Calculation (First arbitrage opportunity):")
            print("-" * 60)
            result = await session.execute(
                select(TradeData)
                .where(TradeData.is_arbitrage_opportunity == True)
                .limit(1)
            )
            test_record = result.scalar_one_or_none()
            
            if test_record:
                AMM_FEE = 0.003
                CEX_FEE = 0.001
                calculated_profit = test_record.eth_vol_u * (
                    (1 - AMM_FEE) * (1 - CEX_FEE) * test_record.price_b - test_record.price_u
                )
                print(f"   Stored Profit: {test_record.arbitrage_profit:.6f} USDT")
                print(f"   Recalculated: {calculated_profit:.6f} USDT")
                print(f"   Match: {'✅ YES' if abs(test_record.arbitrage_profit - calculated_profit) < 0.01 else '❌ NO'}")
            
            print("\n" + "=" * 60)
            print("✅ Verification Complete!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Error during verification: {str(e)}")
            import traceback
            traceback.print_exc()
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(verify_database())
