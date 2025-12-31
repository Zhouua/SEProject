# scripts/query_arbitrage_data.py

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, func
from app.database import AsyncSessionLocal
from app.models import ArbitrageData, TradeData  # 修改了引用模型
from tabulate import tabulate
from datetime import datetime


async def format_arbitrage_record(record: ArbitrageData, trade: TradeData) -> dict:
    """
    格式化套利记录为字典 (对应新表结构)
    """
    direction_text = "U→B" if record.direction == 0 else "B→U"
    
    return {
        "ID": record.id,
        "时间": record.time_align.strftime('%Y-%m-%d %H:%M'),
        "Binance价格": f"${trade.binance_price:,.2f}",
        "Uniswap价格": f"${trade.uniswap_price:,.2f}",
        "价格差": f"${abs(trade.binance_price - trade.uniswap_price):,.2f}",
        "方向": direction_text,
        "利润": f"${record.arbitrage_profit:,.2f}",
        "利润率": f"{record.profit_rate * 100:.4f}%",
        "评分": f"{record.score:.2f}",
        "套利机会": "✅" if trade.is_arbitrage_opportunity else "❌"
    }


async def print_records(title: str, records: list, show_stats: bool = False):
    """
    打印记录表格
    """
    print("\n" + "=" * 155)
    print(f"📊 {title}")
    print("=" * 155)
    
    if not records:
        print("⚠️  没有找到记录")
        return
    
    # 格式化数据
    table_data = []
    for arb_rec, trade_rec in records:
        formatted = await format_arbitrage_record(arb_rec, trade_rec)
        table_data.append(formatted)
    
    # 打印表格
    print(tabulate(table_data, headers="keys", tablefmt="grid"))
    
    if show_stats:
        total_profit = sum(r[0].arbitrage_profit for r in records)
        avg_score = sum(r[0].score for r in records) / len(records)
        print(f"\n📈 本组统计: 总利润: ${total_profit:,.2f} | 平均评分: {avg_score:.2f} | 记录数: {len(records)}")


async def query_top_8(order_by_col, title, desc=True):
    """
    通用查询函数，获取前8个记录
    """
    async with AsyncSessionLocal() as session:
        order_stmt = order_by_col.desc() if desc else order_by_col.asc()
        result = await session.execute(
            select(ArbitrageData, TradeData)
            .join(TradeData, ArbitrageData.trade_id == TradeData.id)
            .order_by(order_stmt.nullslast())
            .limit(8)
        )
        records = result.all()
        await print_records(title, records, show_stats=True)


async def query_overall_stats():
    """
    查询总体统计信息
    """
    async with AsyncSessionLocal() as session:
        # 总套利机会数 (从 ArbitrageData 表统计)
        arb_count = await session.scalar(select(func.count(ArbitrageData.id))) or 0
        
        # 方向统计
        direction_u2b = await session.scalar(
            select(func.count(ArbitrageData.id)).where(ArbitrageData.direction == 0)
        ) or 0
        direction_b2u = await session.scalar(
            select(func.count(ArbitrageData.id)).where(ArbitrageData.direction == 1)
        ) or 0
        
        # 利润与评分
        stats = await session.execute(
            select(
                func.sum(ArbitrageData.arbitrage_profit),
                func.avg(ArbitrageData.arbitrage_profit),
                func.max(ArbitrageData.arbitrage_profit),
                func.avg(ArbitrageData.profit_rate),
                func.avg(ArbitrageData.score),
                func.max(ArbitrageData.score)
            )
        )
        total_p, avg_p, max_p, avg_r, avg_s, max_s = stats.fetchone()

        print("\n" + "=" * 155)
        print("📊 套利数据总体统计 (ArbitrageData 表)")
        print("=" * 155)
        print(f"💰 总套利机会数: {arb_count:,}")
        if arb_count > 0:
            print(f"🔄 方向分布: U→B: {direction_u2b} ({direction_u2b/arb_count*100:.1f}%) | B→U: {direction_b2u} ({direction_b2u/arb_count*100:.1f}%)")
            print(f"💵 利润统计: 总额: ${total_p:,.2f} | 平均: ${avg_p:,.2f} | 最大: ${max_p:,.2f}")
            print(f"📈 利润率:   平均: {avg_r*100:.4f}%")
            print(f"⭐ 评分统计: 平均: {avg_s:.2f} | 最高: {max_s:.2f}")
        print("=" * 155)


async def main():
    print("\n" + "🚀" * 40)
    print("🔍 套利数据深度查询工具 (Top 8 模式)")
    print("🚀" * 40)
    
    try:
        # 1. 总体统计
        await query_overall_stats()
        
        # 2. 最早的 8 个
        await query_top_8(ArbitrageData.time_align, "最早出现的 8 个套利机会", desc=False)
        
        # 3. 最新的 8 个
        await query_top_8(ArbitrageData.time_align, "最近出现的 8 个套利机会", desc=True)
        
        # 4. 利润最高的 8 个
        await query_top_8(ArbitrageData.arbitrage_profit, "利润最高的 Top 8", desc=True)
        
        # 5. 评分最高/低的 8 个
        await query_top_8(ArbitrageData.score, "评分最高的 Top 8", desc=True)
        await query_top_8(ArbitrageData.score, "评分最低的 Top 8", desc=False)

        
        # 6. 利润率最高的 8 个
        await query_top_8(ArbitrageData.profit_rate, "利润率最高的 Top 8", desc=True)

        print("\n" + "✅" * 40)
        print("查询完成！")
        print("✅" * 40 + "\n")
        
    except Exception as e:
        print(f"\n❌ 查询出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
