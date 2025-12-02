import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import select, func
from app.database import AsyncSessionLocal, engine
from app.models import BinanceData, UniswapData, ArbitrageData

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
            result_bn = await session.execute(select(func.count(BinanceData.id)))
            bn_count = result_bn.scalar()
            result_uni = await session.execute(select(func.count(UniswapData.id)))
            uni_count = result_uni.scalar()
            result_arb = await session.execute(select(func.count(ArbitrageData.id)))
            arb_count = result_arb.scalar()
            
            print(f"\n📊 Total Records:")
            print(f"   Binance Data: {bn_count}")
            print(f"   Uniswap Data: {uni_count}")
            print(f"   Arbitrage Data: {arb_count}")
            
            # 2. 套利机会统计
            result = await session.execute(
                select(func.count(ArbitrageData.id)).where(ArbitrageData.is_arbitrage_opportunity == True)
            )
            arbitrage_count = result.scalar()
            arbitrage_percentage = (arbitrage_count / arb_count * 100) if arb_count > 0 else 0
            print(f"💰 Arbitrage Opportunities: {arbitrage_count} ({arbitrage_percentage:.2f}%)")
            
            # 3. 时间范围
            result_bn = await session.execute(
                select(func.min(BinanceData.time_align), func.max(BinanceData.time_align))
            )
            time_range_bn = result_bn.first()
            result_uni = await session.execute(
                select(func.min(UniswapData.time_align), func.max(UniswapData.time_align))
            )
            time_range_uni = result_uni.first()
            print(f"📅 Time Range:")
            print(f"   Binance: {time_range_bn[0]} to {time_range_bn[1]}")
            print(f"   Uniswap: {time_range_uni[0]} to {time_range_uni[1]}")
            
            # 4. 价格统计
            result_bn = await session.execute(
                select(
                    func.min(BinanceData.price),
                    func.max(BinanceData.price),
                    func.avg(BinanceData.price)
                )
            )
            price_stats_bn = result_bn.first()
            
            result_uni = await session.execute(
                select(
                    func.min(UniswapData.price),
                    func.max(UniswapData.price),
                    func.avg(UniswapData.price)
                )
            )
            price_stats_uni = result_uni.first()
            
            print(f"\n💵 Binance Price - Min: {price_stats_bn[0]:.2f}, Max: {price_stats_bn[1]:.2f}, Avg: {price_stats_bn[2]:.2f}")
            print(f"💵 Uniswap Price - Min: {price_stats_uni[0]:.2f}, Max: {price_stats_uni[1]:.2f}, Avg: {price_stats_uni[2]:.2f}")
            
            # 5. 套利获利统计
            result = await session.execute(
                select(
                    func.min(ArbitrageData.arbitrage_profit),
                    func.max(ArbitrageData.arbitrage_profit),
                    func.avg(ArbitrageData.arbitrage_profit)
                ).where(ArbitrageData.is_arbitrage_opportunity == True)
            )
            profit_stats = result.first()
            if profit_stats[0] is not None:
                print(f"💎 Arbitrage Profit (USDT) - Min: {profit_stats[0]:.2f}, Max: {profit_stats[1]:.2f}, Avg: {profit_stats[2]:.2f}")
            
            # 6. 检查是否有NULL值
            result_bn = await session.execute(
                select(func.count(BinanceData.id)).where(
                    (BinanceData.price == None) | 
                    (BinanceData.eth_vol == None) |
                    (BinanceData.usdt_vol == None)
                )
            )
            null_count_bn = result_bn.scalar()
            
            result_uni = await session.execute(
                select(func.count(UniswapData.id)).where(
                    (UniswapData.price == None) | 
                    (UniswapData.eth_vol == None) |
                    (UniswapData.usdt_vol == None)
                )
            )
            null_count_uni = result_uni.scalar()
            
            print(f"⚠️  Records with NULL values:")
            print(f"   Binance: {null_count_bn}")
            print(f"   Uniswap: {null_count_uni}")
            
            # 7. 显示前5条数据样本（关联查询）
            print(f"\n📋 Sample Data (First 5 records):")
            print("-" * 60)
            result = await session.execute(
                select(ArbitrageData, BinanceData, UniswapData)
                .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
                .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
                .order_by(ArbitrageData.time_align)
                .limit(5)
            )
            samples = result.all()
            
            for i, (arb, bn, uni) in enumerate(samples, 1):
                print(f"\n{i}. Time: {arb.time_align}")
                print(f"   Binance: Price={bn.price:.2f}, ETH_Vol={bn.eth_vol:.4f}")
                print(f"   Uniswap: Price={uni.price:.2f}, ETH_Vol={uni.eth_vol:.4f}")
                print(f"   Arbitrage: Profit={arb.arbitrage_profit:.2f} USDT, Opportunity={arb.is_arbitrage_opportunity}")
            
            # 8. 显示最大套利机会
            print(f"\n🏆 Top 5 Arbitrage Opportunities:")
            print("-" * 60)
            result = await session.execute(
                select(ArbitrageData, BinanceData, UniswapData)
                .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
                .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
                .where(ArbitrageData.is_arbitrage_opportunity == True)
                .order_by(ArbitrageData.arbitrage_profit.desc())
                .limit(5)
            )
            top_opportunities = result.all()
            
            for i, (arb, bn, uni) in enumerate(top_opportunities, 1):
                print(f"\n{i}. Time: {arb.time_align}")
                print(f"   Price Diff: Binance={bn.price:.2f}, Uniswap={uni.price:.2f}")
                print(f"   ETH Volume (Uniswap): {uni.eth_vol:.4f}")
                print(f"   💰 Potential Profit: {arb.arbitrage_profit:.2f} USDT")
            
            # 9. 验证套利计算公式
            print(f"\n🧮 Verifying Arbitrage Calculation (First arbitrage opportunity):")
            print("-" * 60)
            result = await session.execute(
                select(ArbitrageData, BinanceData, UniswapData)
                .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
                .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
                .where(ArbitrageData.is_arbitrage_opportunity == True)
                .limit(1)
            )
            test_record = result.first()
            
            if test_record:
                arb, bn, uni = test_record
                AMM_FEE = 0.003
                CEX_FEE = 0.001
                calculated_profit = uni.eth_vol * (
                    (1 - AMM_FEE) * (1 - CEX_FEE) * bn.price - uni.price
                )
                print(f"   Stored Profit: {arb.arbitrage_profit:.6f} USDT")
                print(f"   Recalculated: {calculated_profit:.6f} USDT")
                print(f"   Match: {'✅ YES' if abs(arb.arbitrage_profit - calculated_profit) < 0.01 else '❌ NO'}")
            
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
