# scripts/check_arbitrage_direction.py

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, func
from app.database import AsyncSessionLocal
from app.models import ArbitrageData, BinanceData, UniswapData


async def check_arbitrage_direction():
    """
    检查套利机会的方向分布
    """
    async with AsyncSessionLocal() as session:
        # 查询所有套利机会
        result = await session.execute(
            select(ArbitrageData, BinanceData, UniswapData)
            .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
            .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
            .where(ArbitrageData.is_arbitrage_opportunity == True)
        )
        
        records = result.all()
        
        if not records:
            print("⚠️  没有找到套利机会记录")
            return
        
        # 统计方向
        uniswap_buy_binance_sell = 0  # Uniswap价格低，在Uniswap买入，Binance卖出
        binance_buy_uniswap_sell = 0  # Binance价格低，在Binance买入，Uniswap卖出
        equal_price = 0  # 价格相等（理论上不应该存在）
        
        # 详细记录（前10个示例）
        examples_uniswap_buy = []
        examples_binance_buy = []
        
        for arb, binance, uniswap in records:
            price_diff = binance.price - uniswap.price
            
            if price_diff > 0:
                # Binance价格高，Uniswap价格低 -> 在Uniswap买入，Binance卖出
                uniswap_buy_binance_sell += 1
                if len(examples_uniswap_buy) < 10:
                    examples_uniswap_buy.append({
                        'time': arb.time_align.strftime('%Y-%m-%d %H:%M'),
                        'binance_price': binance.price,
                        'uniswap_price': uniswap.price,
                        'price_diff': price_diff,
                        'profit': arb.arbitrage_profit
                    })
            elif price_diff < 0:
                # Binance价格低，Uniswap价格高 -> 在Binance买入，Uniswap卖出
                binance_buy_uniswap_sell += 1
                if len(examples_binance_buy) < 10:
                    examples_binance_buy.append({
                        'time': arb.time_align.strftime('%Y-%m-%d %H:%M'),
                        'binance_price': binance.price,
                        'uniswap_price': uniswap.price,
                        'price_diff': price_diff,
                        'profit': arb.arbitrage_profit
                    })
            else:
                equal_price += 1
        
        total = len(records)
        
        # 打印结果
        print("\n" + "=" * 100)
        print("🔍 套利方向分析报告")
        print("=" * 100)
        print(f"\n📊 总套利机会数: {total:,}\n")
        
        print("📈 方向分布:")
        print("-" * 100)
        print(f"🟢 Uniswap买入 → Binance卖出 (Uniswap价格更低):")
        print(f"   数量: {uniswap_buy_binance_sell:,}")
        print(f"   占比: {uniswap_buy_binance_sell / total * 100:.2f}%")
        print()
        print(f"🔵 Binance买入 → Uniswap卖出 (Binance价格更低):")
        print(f"   数量: {binance_buy_uniswap_sell:,}")
        print(f"   占比: {binance_buy_uniswap_sell / total * 100:.2f}%")
        
        if equal_price > 0:
            print()
            print(f"⚪ 价格相等:")
            print(f"   数量: {equal_price:,}")
            print(f"   占比: {equal_price / total * 100:.2f}%")
        
        print("-" * 100)
        
        # 结论
        print("\n💡 结论:")
        if uniswap_buy_binance_sell == total:
            print("   ✅ 所有套利机会都是: Uniswap买入 → Binance卖出")
            print("   ℹ️  这意味着Uniswap价格始终低于Binance价格")
        elif binance_buy_uniswap_sell == total:
            print("   ✅ 所有套利机会都是: Binance买入 → Uniswap卖出")
            print("   ℹ️  这意味着Binance价格始终低于Uniswap价格")
        else:
            print("   ⚠️  套利方向存在双向情况")
            print(f"   主要方向: {'Uniswap买入→Binance卖出' if uniswap_buy_binance_sell > binance_buy_uniswap_sell else 'Binance买入→Uniswap卖出'}")
        
        # 显示示例
        if examples_uniswap_buy:
            print("\n" + "=" * 100)
            print("📋 Uniswap买入→Binance卖出 示例 (前10个):")
            print("=" * 100)
            print(f"{'时间':<20} {'Binance价格':>15} {'Uniswap价格':>15} {'价格差':>15} {'利润':>15}")
            print("-" * 100)
            for ex in examples_uniswap_buy:
                print(f"{ex['time']:<20} ${ex['binance_price']:>14,.2f} ${ex['uniswap_price']:>14,.2f} "
                      f"${ex['price_diff']:>14,.2f} ${ex['profit']:>14,.2f}")
        
        if examples_binance_buy:
            print("\n" + "=" * 100)
            print("📋 Binance买入→Uniswap卖出 示例 (前10个):")
            print("=" * 100)
            print(f"{'时间':<20} {'Binance价格':>15} {'Uniswap价格':>15} {'价格差':>15} {'利润':>15}")
            print("-" * 100)
            for ex in examples_binance_buy:
                print(f"{ex['time']:<20} ${ex['binance_price']:>14,.2f} ${ex['uniswap_price']:>14,.2f} "
                      f"${ex['price_diff']:>14,.2f} ${ex['profit']:>14,.2f}")
        
        print("\n" + "=" * 100)
        
        # 额外分析：价格差统计
        print("\n📊 价格差统计:")
        print("-" * 100)
        
        if uniswap_buy_binance_sell > 0:
            avg_diff_u2b = sum(ex['price_diff'] for ex in examples_uniswap_buy) / len(examples_uniswap_buy)
            print(f"Uniswap买入方向平均价格差: ${avg_diff_u2b:.2f}")
        
        if binance_buy_uniswap_sell > 0:
            avg_diff_b2u = sum(abs(ex['price_diff']) for ex in examples_binance_buy) / len(examples_binance_buy)
            print(f"Binance买入方向平均价格差: ${avg_diff_b2u:.2f}")
        
        print("=" * 100 + "\n`")


async def main():
    """
    主函数
    """
    print("\n" + "🚀" * 50)
    print("🔍 套利方向检查工具")
    print("🚀" * 50)
    
    try:
        await check_arbitrage_direction()
        
        print("✅ 检查完成！\n")
        
    except Exception as e:
        print(f"\n❌ 检查过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
