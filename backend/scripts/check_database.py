# scripts/query_arbitrage_data.py

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, func
from app.database import AsyncSessionLocal
from app.models import ArbitrageData, BinanceData, UniswapData
from tabulate import tabulate
from datetime import datetime


async def format_arbitrage_record(record: ArbitrageData, binance: BinanceData, uniswap: UniswapData) -> dict:
    """
    格式化套利记录为字典
    """
    direction_text = "U→B" if record.direction == 0 else "B→U"
    
    return {
        "ID": record.id,
        "时间": record.time_align.strftime('%Y-%m-%d %H:%M'),
        "Binance价格": f"${binance.price:,.2f}",
        "Uniswap价格": f"${uniswap.price:,.2f}",
        "价格差": f"${abs(binance.price - uniswap.price):,.2f}",
        "方向": direction_text,
        "利润": f"${record.arbitrage_profit:,.2f}" if record.arbitrage_profit else "$0.00",
        "利润率": f"{record.profit_rate * 100:.4f}%" if record.profit_rate else "0.00%",
        "评分": f"{record.score:.2f}" if record.score else "0.00",
        "套利机会": "✅" if record.is_arbitrage_opportunity else "❌"
    }


async def print_records(title: str, records: list, show_stats: bool = False):
    """
    打印记录表格
    """
    print("\n" + "=" * 150)
    print(f"📊 {title}")
    print("=" * 150)
    
    if not records:
        print("⚠️  没有找到记录")
        return
    
    # 格式化数据
    table_data = []
    for record, binance, uniswap in records:
        formatted = await format_arbitrage_record(record, binance, uniswap)
        table_data.append(formatted)
    
    # 打印表格
    print(tabulate(table_data, headers="keys", tablefmt="grid"))
    
    # 打印统计信息
    if show_stats:
        total_profit = sum(r[0].arbitrage_profit or 0 for r in records)
        avg_profit = total_profit / len(records) if records else 0
        avg_profit_rate = sum(r[0].profit_rate or 0 for r in records) / len(records) if records else 0
        avg_score = sum(r[0].score or 0 for r in records) / len(records) if records else 0
        arb_count = sum(1 for r in records if r[0].is_arbitrage_opportunity)
        direction_u2b = sum(1 for r in records if r[0].direction == 0)
        direction_b2u = sum(1 for r in records if r[0].direction == 1)
        
        print("\n📈 统计信息:")
        print(f"   总利润: ${total_profit:,.2f}")
        print(f"   平均利润: ${avg_profit:,.2f}")
        print(f"   平均利润率: {avg_profit_rate * 100:.4f}%")
        print(f"   平均评分: {avg_score:.2f}")
        print(f"   套利机会数: {arb_count}/{len(records)}")
        print(f"   方向分布: U→B {direction_u2b}次, B→U {direction_b2u}次")


async def query_first_five():
    """
    查询前五个套利记录
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ArbitrageData, BinanceData, UniswapData)
            .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
            .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
            .order_by(ArbitrageData.id.asc())
            .limit(5)
        )
        records = result.all()
        await print_records("前五个套利记录", records)


async def query_last_five():
    """
    查询最后五个套利记录
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ArbitrageData, BinanceData, UniswapData)
            .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
            .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
            .order_by(ArbitrageData.id.desc())
            .limit(5)
        )
        records = result.all()
        # 反转顺序以按时间正序显示
        records = list(reversed(records))
        await print_records("最后五个套利记录", records)


async def query_random_five():
    """
    查询随机五个套利记录
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ArbitrageData, BinanceData, UniswapData)
            .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
            .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
            .order_by(func.random())
            .limit(5)
        )
        records = result.all()
        await print_records("随机五个套利记录", records)


async def query_best_five_by_profit():
    """
    查询最好的五个套利记录（利润最高）
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ArbitrageData, BinanceData, UniswapData)
            .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
            .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
            .order_by(ArbitrageData.arbitrage_profit.desc().nullslast())
            .limit(5)
        )
        records = result.all()
        await print_records("最好的五个套利记录（按利润排序）", records, show_stats=True)


async def query_best_five_by_profit_rate():
    """
    查询最好的五个套利记录（利润率最高）
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ArbitrageData, BinanceData, UniswapData)
            .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
            .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
            .order_by(ArbitrageData.profit_rate.desc().nullslast())
            .limit(5)
        )
        records = result.all()
        await print_records("最好的五个套利记录（按利润率排序）", records, show_stats=True)


async def query_best_five_by_score():
    """
    查询最好的五个套利记录（评分最高）
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ArbitrageData, BinanceData, UniswapData)
            .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
            .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
            .order_by(ArbitrageData.score.desc().nullslast())
            .limit(5)
        )
        records = result.all()
        await print_records("最好的五个套利记录（按评分排序）", records, show_stats=True)


async def query_worst_five():
    """
    查询最差的五个套利记录（利润最低或负值最大）
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ArbitrageData, BinanceData, UniswapData)
            .join(BinanceData, ArbitrageData.binance_id == BinanceData.id)
            .join(UniswapData, ArbitrageData.uniswap_id == UniswapData.id)
            .order_by(ArbitrageData.arbitrage_profit.asc().nullsfirst())
            .limit(5)
        )
        records = result.all()
        await print_records("最差的五个套利记录（利润最低）", records, show_stats=True)


async def query_overall_stats():
    """
    查询总体统计信息
    """
    async with AsyncSessionLocal() as session:
        # 总记录数
        total_count = await session.scalar(select(func.count(ArbitrageData.id)))
        
        # 套利机会数
        arb_count = await session.scalar(
            select(func.count(ArbitrageData.id))
            .where(ArbitrageData.is_arbitrage_opportunity == True)
        )
        
        # 方向统计
        direction_u2b = await session.scalar(
            select(func.count(ArbitrageData.id))
            .where(ArbitrageData.is_arbitrage_opportunity == True)
            .where(ArbitrageData.direction == 0)
        ) or 0
        
        direction_b2u = await session.scalar(
            select(func.count(ArbitrageData.id))
            .where(ArbitrageData.is_arbitrage_opportunity == True)
            .where(ArbitrageData.direction == 1)
        ) or 0
        
        # 总利润
        total_profit = await session.scalar(
            select(func.sum(ArbitrageData.arbitrage_profit))
            .where(ArbitrageData.is_arbitrage_opportunity == True)
        ) or 0
        
        # 平均利润
        avg_profit = await session.scalar(
            select(func.avg(ArbitrageData.arbitrage_profit))
            .where(ArbitrageData.is_arbitrage_opportunity == True)
        ) or 0
        
        # 平均利润率
        avg_profit_rate = await session.scalar(
            select(func.avg(ArbitrageData.profit_rate))
            .where(ArbitrageData.is_arbitrage_opportunity == True)
        ) or 0
        
        # 平均评分
        avg_score = await session.scalar(
            select(func.avg(ArbitrageData.score))
            .where(ArbitrageData.is_arbitrage_opportunity == True)
        ) or 0
        
        # 最大利润
        max_profit = await session.scalar(
            select(func.max(ArbitrageData.arbitrage_profit))
        ) or 0
        
        # 最小利润
        min_profit = await session.scalar(
            select(func.min(ArbitrageData.arbitrage_profit))
        ) or 0
        
        # 最大利润率
        max_profit_rate = await session.scalar(
            select(func.max(ArbitrageData.profit_rate))
        ) or 0
        
        # 最大评分
        max_score = await session.scalar(
            select(func.max(ArbitrageData.score))
        ) or 0
        
        print("\n" + "=" * 150)
        print("📊 套利数据总体统计")
        print("=" * 150)
        print(f"📈 总记录数: {total_count:,}")
        print(f"💰 套利机会数: {arb_count:,}")
        print(f"📊 套利机会占比: {arb_count / total_count * 100:.2f}%" if total_count > 0 else "0%")
        print(f"\n🔄 方向分布:")
        print(f"   U→B (Uniswap买Binance卖): {direction_u2b:,} ({direction_u2b / arb_count * 100:.2f}%)" if arb_count > 0 else "   U→B: 0")
        print(f"   B→U (Binance买Uniswap卖): {direction_b2u:,} ({direction_b2u / arb_count * 100:.2f}%)" if arb_count > 0 else "   B→U: 0")
        print(f"\n💵 利润统计:")
        print(f"   总利润: ${total_profit:,.2f}")
        print(f"   平均利润: ${avg_profit:,.2f}")
        print(f"   最大利润: ${max_profit:,.2f}")
        print(f"   最小利润: ${min_profit:,.2f}")
        print(f"\n📉 利润率统计:")
        print(f"   平均利润率: {avg_profit_rate * 100:.4f}%")
        print(f"   最大利润率: {max_profit_rate * 100:.4f}%")
        print(f"\n⭐ 评分统计:")
        print(f"   平均评分: {avg_score:.2f}")
        print(f"   最大评分: {max_score:.2f}")
        print("=" * 150)


async def main():
    """
    主函数：执行所有查询
    """
    print("\n" + "🚀" * 50)
    print("🔍 套利数据查询工具")
    print("🚀" * 50)
    
    try:
        # 总体统计
        await query_overall_stats()
        
        # 前五个
        await query_first_five()
        
        # 最后五个
        await query_last_five()
        
        # 随机五个
        await query_random_five()
        
        # 最好五个（按利润）
        await query_best_five_by_profit()
        
        # 最好五个（按利润率）
        await query_best_five_by_profit_rate()
        
        # 最好五个（按评分）
        await query_best_five_by_score()
        
        # 最差五个
        await query_worst_five()
        
        print("\n" + "✅" * 50)
        print("✅ 查询完成！")
        print("✅" * 50 + "\n")
        
    except Exception as e:
        print(f"\n❌ 查询过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
