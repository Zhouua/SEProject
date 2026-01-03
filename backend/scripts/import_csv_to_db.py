# scripts/import_csv_to_db.py

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from sqlalchemy import select
from app.database import AsyncSessionLocal, create_tables
from app.models import BinanceData, UniswapData, ArbitrageData, TradeData
from datetime import datetime
from tqdm import tqdm

# 手续费常量
UNISWAP_FEE = 0.003  # 0.3%
BINANCE_FEE = 0.001  # 0.1%
GAS_FEE = 20  # 固定gas费
LIQUIDITY_ESTIMATE = 1_000_000  # 流动性估计值

# 多因子评分权重
WEIGHTS = {
    "price_diff": 0.8,
    "volume": 0.3,
    "liquidity": 0.0,
    "gas_fee": -0.1  # 负权重
}


def calculate_apamm(price_u, eth_vol_u):
    """
    受滑点影响的PAMM价格计算
    """
    slippage_factor = 1 + eth_vol_u / LIQUIDITY_ESTIMATE
    apamm_price = price_u * slippage_factor
    return apamm_price


def calculate_multifactor_score(price_b, apamm_price, eth_vol_u, eth_vol_b):
    """
    多因子评分计算（归一化处理）
    
    为了统一量纲，将各因子归一化到相似的数量级：
    - 价格差：直接使用（美元）
    - 交易量：使用平均值（ETH）
    - 流动性：归一化到千为单位
    - gas费：直接使用（美元）
    """
    # 价格差（绝对值）
    price_diff = abs(price_b - apamm_price)
    
    # 交易量（使用平均值）
    volume = (eth_vol_u + eth_vol_b) / 2
    
    # 流动性（归一化到千为单位，使其与其他因子量级相近）
    liquidity_normalized = LIQUIDITY_ESTIMATE / 1000
    
    # gas费
    gas_fee = GAS_FEE
    
    # 加权求和
    score = (
        WEIGHTS["price_diff"] * price_diff +
        WEIGHTS["volume"] * volume +
        WEIGHTS["liquidity"] * liquidity_normalized +
        WEIGHTS["gas_fee"] * gas_fee  # 权重已经是负的
    )
    score = score / 40  # 归一化处理
    return score


def calculate_arbitrage_profit_bidirectional(price_b: float, price_u: float, eth_vol_u: float, eth_vol_b: float) -> tuple[bool, float, float, float, int]:
    """
    双向计算套利利润，选择最优方向
    
    返回：(是否为套利机会, 套利利润, 利润率, 评分, 方向)
    方向: 0 = U2B (Uniswap买Binance卖), 1 = B2U (Binance买Uniswap卖)
    """
    apamm_price = calculate_apamm(price_u, eth_vol_u)
    
    # 使用平均交易量
    avg_eth_vol = (eth_vol_u + eth_vol_b) / 2
    
    # 方向1: Uniswap买入 -> Binance卖出 (direction = 0)
    buy_price_u = apamm_price * (1 + UNISWAP_FEE)  # 买入成本
    sell_price_b = price_b * (1 - BINANCE_FEE)      # 卖出收入
    
    # 投入：买入ETH的总成本
    investment_u2b = avg_eth_vol * buy_price_u
    # 收入：卖出ETH的总收入
    revenue_u2b = avg_eth_vol * sell_price_b
    # 利润：收入 - 投入 - gas费
    profit_u2b = revenue_u2b - investment_u2b - GAS_FEE
    # 利润率：利润 / 投入
    profit_rate_u2b = profit_u2b / investment_u2b if investment_u2b > 0 else 0
    
    # 方向2: Binance买入 -> Uniswap卖出 (direction = 1)
    buy_price_b = price_b * (1 + BINANCE_FEE)       # 买入成本
    sell_price_u = apamm_price * (1 - UNISWAP_FEE)  # 卖出收入
    
    # 投入：买入ETH的总成本
    investment_b2u = avg_eth_vol * buy_price_b
    # 收入：卖出ETH的总收入
    revenue_b2u = avg_eth_vol * sell_price_u
    # 利润：收入 - 投入 - gas费
    profit_b2u = revenue_b2u - investment_b2u - GAS_FEE
    # 利润率：利润 / 投入
    profit_rate_b2u = profit_b2u / investment_b2u if investment_b2u > 0 else 0
    
    # 选择利润更高的方向
    if profit_u2b > profit_b2u:
        best_profit = profit_u2b
        best_profit_rate = profit_rate_u2b
        direction = 0  # U2B
    else:
        best_profit = profit_b2u
        best_profit_rate = profit_rate_b2u
        direction = 1  # B2U
    
    # 多因子评分（使用原始价格，不考虑方向）
    score = calculate_multifactor_score(price_b, apamm_price, eth_vol_u, eth_vol_b)
    
    # 判断是否为套利机会
    is_arbitrage = (best_profit > 0) and (score > 0)
    
    return is_arbitrage, best_profit if is_arbitrage else 0.0, best_profit_rate if is_arbitrage else 0.0, score, direction


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
        trade_exist = (await session.execute(select(TradeData).limit(1))).scalar_one_or_none()
        arb_exist = (await session.execute(select(ArbitrageData).limit(1))).scalar_one_or_none()
        if bn_exist or uni_exist or trade_exist or arb_exist:
            print("⚠️  数据库已有数据，跳过导入")
            return

        batch_size = 1000
        total_imported = 0
        arbitrage_count = 0
        direction_stats = {0: 0, 1: 0}  # 统计套利方向

        binance_list = []
        uniswap_list = []
        trade_list = []
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
                is_arbitrage, arbitrage_profit, profit_rate, score, direction = calculate_arbitrage_profit_bidirectional(
                    row['price_b'], row['price_u'], row['eth_vol_u'], row['eth_vol_b']
                )
                
                # 创建 trade_data 记录（所有交易对都存储score）
                trade = TradeData(
                    time_align=time_align,
                    binance_price=row['price_b'],
                    binance_vol=row['eth_vol_b'],
                    uniswap_price=row['price_u'],
                    uniswap_vol=row['eth_vol_u'],
                    is_arbitrage_opportunity=is_arbitrage,
                    score=score  # 所有记录都存储score
                )
                trade_list.append(trade)
                
                if is_arbitrage:
                    arbitrage_count += 1
                    direction_stats[direction] += 1

                if (idx + 1) % batch_size == 0 or (idx + 1) == len(df):
                    # 插入 binance、uniswap 和 trade 数据
                    session.add_all(binance_list)
                    session.add_all(uniswap_list)
                    session.add_all(trade_list)
                    await session.commit()

                    # 获取当前批次的时间戳
                    times = [datetime.strptime(t, '%Y-%m-%d %H:%M') if isinstance(t, str) else t 
                            for t in df.loc[idx+1-len(binance_list):idx, 'time_align']]

                    # 查询已插入的 trade_data（用于 arbitrage_data）
                    result_trade = await session.execute(select(TradeData).where(TradeData.time_align.in_(times)))
                    inserted_trade = {}
                    for item in result_trade.scalars():
                        inserted_trade[item.time_align] = item

                    # 只为套利机会创建 arbitrage_data
                    for t_time in inserted_trade:
                        trade_obj = inserted_trade[t_time]
                        
                        # 只处理套利机会
                        if not trade_obj.is_arbitrage_opportunity:
                            continue
                        
                        row_idx = times.index(t_time)
                        row_data = df.iloc[idx+1-len(binance_list)+row_idx]

                        is_arbitrage, arbitrage_profit, profit_rate, score, direction = calculate_arbitrage_profit_bidirectional(
                            row_data['price_b'], row_data['price_u'], row_data['eth_vol_u'], row_data['eth_vol_b']
                        )
                        
                        # 创建 arbitrage_data 记录
                        if is_arbitrage:
                            arbitrage = ArbitrageData(
                                time_align=t_time,
                                trade_id=trade_obj.id,
                                arbitrage_profit=arbitrage_profit,
                                profit_rate=profit_rate,
                                score=score,
                                direction=direction
                            )
                            arbitrage_list.append(arbitrage)

                    session.add_all(arbitrage_list)
                    await session.commit()

                    total_imported += len(binance_list)
                    pbar.update(len(binance_list))

                    binance_list.clear()
                    uniswap_list.clear()
                    trade_list.clear()
                    arbitrage_list.clear()

        print("\n" + "=" * 60)
        print("导入完成！")
        print("=" * 60)
        print(f"📊 总记录数: {total_imported:,}")
        print(f"💰 套利机会数: {arbitrage_count:,}")
        print(f"📈 套利机会占比: {arbitrage_count / total_imported * 100:.2f}%")
        if arbitrage_count > 0:
            print(f"🔄 套利方向分布:")
            print(f"   Uniswap买→Binance卖 (0): {direction_stats[0]:,} ({direction_stats[0]/arbitrage_count*100:.2f}%)")
            print(f"   Binance买→Uniswap卖 (1): {direction_stats[1]:,} ({direction_stats[1]/arbitrage_count*100:.2f}%)")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(import_csv_data())
