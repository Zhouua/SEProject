# scripts/import_csv_to_db_fixed.py

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from sqlalchemy import select
from app.database import AsyncSessionLocal, create_tables
from app.models import BinanceData, UniswapData, ArbitrageData
from datetime import datetime
from tqdm import tqdm

# 手续费常量
UNISWAP_FEE = 0.003  # 0.3%
BINANCE_FEE = 0.001  # 0.1%
GAS_FEE = 20  # 固定gas费
LIQUIDITY_ESTIMATE = 1_000_000  # 流动性估计值

# 多因子评分权重
WEIGHTS = {
    "price_diff": 0.4,
    "volume": 0.3,
    "liquidity": 0.2,
    "gas_fee": 0.1
}


def calculate_apamm(price_u, eth_vol_u):
    """
    受滑点影响的PAMM价格计算
    """
    slippage_factor = 1 + eth_vol_u / LIQUIDITY_ESTIMATE
    apamm_price = price_u * slippage_factor
    return apamm_price


def calculate_multifactor_score(price_diff, eth_vol_u):
    """
    多因子评分计算
    """
    volume = eth_vol_u
    liquidity = LIQUIDITY_ESTIMATE
    gas_fee = -GAS_FEE

    score = (
        WEIGHTS["price_diff"] * price_diff +
        WEIGHTS["volume"] * volume +
        WEIGHTS["liquidity"] * liquidity +
        WEIGHTS["gas_fee"] * gas_fee
    )
    return score


def calculate_arbitrage_profit_bidirectional(price_b: float, price_u: float, eth_vol_u: float) -> tuple[bool, float, str]:
    """
    双向计算套利利润，选择最优方向
    
    返回：(是否为套利机会, 套利利润, 套利方向)
    套利方向: "U2B" (Uniswap买入Binance卖出) 或 "B2U" (Binance买入Uniswap卖出)
    """
    apamm_price = calculate_apamm(price_u, eth_vol_u)
    
    # 方向1: Uniswap买入 -> Binance卖出
    # 在Uniswap买入需要支付手续费，在Binance卖出也需要支付手续费
    buy_price_u = apamm_price * (1 + UNISWAP_FEE)  # Uniswap买入价（含手续费）
    sell_price_b = price_b * (1 - BINANCE_FEE)      # Binance卖出价（扣除手续费）
    profit_u2b = eth_vol_u * (sell_price_b - buy_price_u) - GAS_FEE
    
    # 方向2: Binance买入 -> Uniswap卖出
    # 在Binance买入需要支付手续费，在Uniswap卖出也需要支付手续费
    buy_price_b = price_b * (1 + BINANCE_FEE)       # Binance买入价（含手续费）
    sell_price_u = apamm_price * (1 - UNISWAP_FEE)  # Uniswap卖出价（扣除手续费）
    profit_b2u = eth_vol_u * (sell_price_u - buy_price_b) - GAS_FEE
    
    # 选择利润更高的方向
    if profit_u2b > profit_b2u:
        best_profit = profit_u2b
        direction = "U2B"
        price_diff = sell_price_b - buy_price_u
    else:
        best_profit = profit_b2u
        direction = "B2U"
        price_diff = sell_price_u - buy_price_b
    
    # 多因子评分
    score = calculate_multifactor_score(price_diff, eth_vol_u)
    
    # 判断是否为套利机会
    is_arbitrage = (best_profit > 0) and (score > 0)
    
    return is_arbitrage, best_profit if is_arbitrage else 0.0, direction


async def import_csv_data():
    await create_tables()

    csv_path = "app/data/aligned_usdt_eth_complete.csv"
    print(f"📁 正在读取CSV文件: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"✅ CSV文件读取完成，共 {len(df):,} 条记录")

    required_columns = ['time_align', 'price_b', 'price_u', 'eth_vol_b', 'eth_vol_u', 'usdt_vol_b', 'usdt_vol_u']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"CSV文件缺少必需的列: {missing_columns}")

    async with AsyncSessionLocal() as session:
        # 检查数据是否已经导入
        bn_exist = (await session.execute(select(BinanceData).limit(1))).scalar_one_or_none()
        uni_exist = (await session.execute(select(UniswapData).limit(1))).scalar_one_or_none()
        arb_exist = (await session.execute(select(ArbitrageData).limit(1))).scalar_one_or_none()
        if bn_exist or uni_exist or arb_exist:
            print("⚠️  数据库已有数据，跳过导入")
            return

        batch_size = 1000
        total_imported = 0
        arbitrage_count = 0
        direction_stats = {"U2B": 0, "B2U": 0}  # 统计套利方向

        binance_list = []
        uniswap_list = []
        arbitrage_list = []

        print("🚀 开始导入数据...\n")
        with tqdm(total=len(df), desc="导入进度", unit="条", ncols=100,
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]') as pbar:

            for idx, row in df.iterrows():
                time_align = datetime.strptime(row['time_align'], '%Y-%m-%d %H:%M')

                binance = BinanceData(
                    time_align=time_align,
                    price=row['price_b'],
                    eth_vol=row['eth_vol_b'],
                    usdt_vol=row['usdt_vol_b']
                )
                binance_list.append(binance)

                uniswap = UniswapData(
                    time_align=time_align,
                    price=row['price_u'],
                    eth_vol=row['eth_vol_u'],
                    usdt_vol=row['usdt_vol_u']
                )
                uniswap_list.append(uniswap)

                # 双向计算套利
                is_arbitrage, arbitrage_profit, direction = calculate_arbitrage_profit_bidirectional(
                    row['price_b'], row['price_u'], row['eth_vol_u']
                )
                if is_arbitrage:
                    arbitrage_count += 1
                    direction_stats[direction] += 1

                if (idx + 1) % batch_size == 0 or (idx + 1) == len(df):
                    session.add_all(binance_list)
                    session.add_all(uniswap_list)
                    await session.commit()

                    times = [datetime.strptime(t, '%Y-%m-%d %H:%M') if isinstance(t, str) else t 
                            for t in df.loc[idx+1-len(binance_list):idx, 'time_align']]

                    inserted_binance = {}
                    inserted_uniswap = {}

                    result_bn = await session.execute(select(BinanceData).where(BinanceData.time_align.in_(times)))
                    for item in result_bn.scalars():
                        inserted_binance[item.time_align] = item

                    result_uni = await session.execute(select(UniswapData).where(UniswapData.time_align.in_(times)))
                    for item in result_uni.scalars():
                        inserted_uniswap[item.time_align] = item

                    for b_time in inserted_binance:
                        bn_obj = inserted_binance[b_time]
                        uni_obj = inserted_uniswap.get(b_time)
                        if not uni_obj:
                            continue
                        
                        row_idx = times.index(b_time)
                        row_data = df.iloc[idx+1-len(binance_list)+row_idx]

                        is_arbitrage, arbitrage_profit, direction = calculate_arbitrage_profit_bidirectional(
                            row_data['price_b'], row_data['price_u'], row_data['eth_vol_u']
                        )
                        
                        arbitrage = ArbitrageData(
                            time_align=b_time,
                            binance_id=bn_obj.id,
                            uniswap_id=uni_obj.id,
                            arbitrage_profit=arbitrage_profit,
                            is_arbitrage_opportunity=is_arbitrage
                        )
                        arbitrage_list.append(arbitrage)

                    session.add_all(arbitrage_list)
                    await session.commit()

                    total_imported += len(binance_list)
                    pbar.update(len(binance_list))

                    binance_list.clear()
                    uniswap_list.clear()
                    arbitrage_list.clear()

        print("\n" + "=" * 60)
        print("✅ 导入完成！")
        print("=" * 60)
        print(f"📊 总记录数: {total_imported:,}")
        print(f"💰 套利机会数: {arbitrage_count:,}")
        print(f"📈 套利机会占比: {arbitrage_count / total_imported * 100:.2f}%")
        print(f"🔄 套利方向分布:")
        print(f"   Uniswap买→Binance卖: {direction_stats['U2B']:,} ({direction_stats['U2B']/arbitrage_count*100:.2f}%)")
        print(f"   Binance买→Uniswap卖: {direction_stats['B2U']:,} ({direction_stats['B2U']/arbitrage_count*100:.2f}%)")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(import_csv_data())
