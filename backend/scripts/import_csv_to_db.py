import asyncio
import sys
from pathlib import Path

# Add parent directory to path
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
GAS_FEE = 20  # 固定gas费，直接从利润中扣除
LIQUIDITY_ESTIMATE = 1_000_000  # 不动滑点影响的流动性估计值

# 多因子评分权重示例（价格差权重，交易量权重，流动性权重，gas费权重）
WEIGHTS = {
    "price_diff": 0.4,
    "volume": 0.3,
    "liquidity": 0.2,
    "gas_fee": 0.1  # 权重为负值时使用负号处理
}

def calculate_apamm(price_u, eth_vol_u):
    """
    受滑点影响的PAMM价格计算，简化版本（基于liquidity_estimate与交易量估算滑点影响）。
    参考文档中滑点计算，公式示意：
    APAMM = price_u * (1 ± eth_vol_u / liquidity_estimate)
    这里假设买卖滑点方向，根据需求调整。
    由于缺少明确方向，默认向上滑点：
    """
    slippage_factor = 1 + eth_vol_u / LIQUIDITY_ESTIMATE
    apamm_price = price_u * slippage_factor
    return apamm_price


def calculate_multifactor_score(price_b, apamm_price, eth_vol_u):
    """
    多因子评分计算，包含价格差、交易量、流动性和gas费用：
    score = w1*price_diff + w2*volume + w3*liquidity + w4*gas_fee
    gas_fee权重为负，实际用负的常数乘
    """
    price_diff = price_b - apamm_price
    volume = eth_vol_u
    liquidity = LIQUIDITY_ESTIMATE
    gas_fee = -GAS_FEE  # gas费权重为负，这里直接负值

    score = (
        WEIGHTS["price_diff"] * price_diff +
        WEIGHTS["volume"] * volume +
        WEIGHTS["liquidity"] * liquidity +
        WEIGHTS["gas_fee"] * gas_fee
    )
    return score


def calculate_arbitrage_profit(price_b: float, price_u: float, eth_vol_u: float) -> tuple[bool, float]:
    """
    采用改进版算法计算套利利润：
    1. 计算受滑点影响的PAMM价格 (APAMM)
    2. 使用APAMM代替PAMM价格
    3. 手续费叠加，利润计算
    4. 加入gas费用扣除
    5. 结合多因子评分判定是否套利信号

    返回元组：是否为套利机会，套利利润
    """
    apamm_price = calculate_apamm(price_u, eth_vol_u)

    # 手续费调整的有效卖出价格（Binance作为卖出端）
    effective_sell_price = (1 - UNISWAP_FEE) * (1 - BINANCE_FEE) * price_b

    # 理论套利利润：以交易量和价格差计算，减去gas费
    profit = eth_vol_u * (effective_sell_price - apamm_price) - GAS_FEE

    # 多因子评分决定是否真正套利机会
    score = calculate_multifactor_score(price_b, apamm_price, eth_vol_u)

    is_arbitrage = (profit > 0) and (score > 0)

    return is_arbitrage, profit if is_arbitrage else 0.0


async def import_csv_data():
    await create_tables()

    csv_path = "app/data/aligned_usdt_eth_complete.csv"
    print(f"正在读取CSV文件: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"CSV文件读取完成，共 {len(df):,} 条记录")

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
            print("数据库已有数据，跳过导入")
            return

        batch_size = 1000
        total_imported = 0
        arbitrage_count = 0

        binance_list = []
        uniswap_list = []
        arbitrage_list = []

        # 使用tqdm创建进度条
        print("开始导入数据...\n")
        with tqdm(total=len(df), desc="导入进度", unit="条", ncols=100,
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]') as pbar:

            for idx, row in df.iterrows():
                time_align = datetime.strptime(row['time_align'], '%Y-%m-%d %H:%M')

                # 创建Binance数据实例
                binance = BinanceData(
                    time_align=time_align,
                    price=row['price_b'],
                    eth_vol=row['eth_vol_b'],
                    usdt_vol=row['usdt_vol_b']
                )
                binance_list.append(binance)

                # 创建Uniswap数据实例
                uniswap = UniswapData(
                    time_align=time_align,
                    price=row['price_u'],
                    eth_vol=row['eth_vol_u'],
                    usdt_vol=row['usdt_vol_u']
                )
                uniswap_list.append(uniswap)

                # 计算套利（使用改进版）
                is_arbitrage, arbitrage_profit = calculate_arbitrage_profit(row['price_b'], row['price_u'], row['eth_vol_u'])
                if is_arbitrage:
                    arbitrage_count += 1

                if (idx + 1) % batch_size == 0 or (idx + 1) == len(df):
                    # 先插入binance和uniswap数据
                    session.add_all(binance_list)
                    session.add_all(uniswap_list)
                    await session.commit()

                    # 查询对应时间区间
                    times = [datetime.strptime(t, '%Y-%m-%d %H:%M') if isinstance(t, str) else t for t in df.loc[idx+1-len(binance_list):idx, 'time_align']]

                    # 批量查询
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
                        # 使用已插入的binance和uniswap数据ID创建套利记录
                        row_idx = times.index(b_time)
                        row_data = df.iloc[idx+1-len(binance_list)+row_idx]

                        # 计算套利（改进版）
                        is_arbitrage, arbitrage_profit = calculate_arbitrage_profit(
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

                    # 批量插入套利数据
                    session.add_all(arbitrage_list)
                    await session.commit()

                    total_imported += len(binance_list)

                    # 更新进度条
                    pbar.update(len(binance_list))

                    binance_list.clear()
                    uniswap_list.clear()
                    arbitrage_list.clear()

        print("\n" + "=" * 60)
        print("导入完成！")
        print("=" * 60)
        print(f"总记录数: {total_imported:,}")
        print(f"套利机会数: {arbitrage_count:,}")
        print(f"套利机会占比: {arbitrage_count / total_imported * 100:.2f}%")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(import_csv_data())
