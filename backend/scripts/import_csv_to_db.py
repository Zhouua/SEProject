import asyncio
import pandas as pd
from sqlalchemy import select
from app.database import AsyncSessionLocal, create_tables
from app.models import TradeData
from datetime import datetime

# 手续费常量
UNISWAP_FEE = 0.003  # 0.3%
BINANCE_FEE = 0.001  # 0.1%


def calculate_arbitrage_profit(price_b: float, price_u: float, eth_vol_u: float) -> tuple[bool, float]:
    """计算套利机会和利润"""
    effective_sell_price = (1 - UNISWAP_FEE) * (1 - BINANCE_FEE) * price_b
    profit = eth_vol_u * (effective_sell_price - price_u)
    is_arbitrage = profit > 0
    return is_arbitrage, profit if is_arbitrage else 0.0


async def import_csv_data():
    """从CSV导入数据到数据库"""
    
    # 初始化数据库表
    await create_tables()
    
    # 读取CSV文件
    csv_path = "app/data/aligned_usdt_eth_complete.csv"
    print(f"正在读取CSV文件: {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"CSV文件读取完成，共 {len(df)} 条记录")
    
    # 数据验证
    required_columns = ['time_align', 'price_b', 'price_u', 'eth_vol_b', 'eth_vol_u', 'usdt_vol_b', 'usdt_vol_u']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"CSV文件缺少必需的列: {missing_columns}")
    
    async with AsyncSessionLocal() as session:
        # 检查是否已有数据
        result = await session.execute(select(TradeData).limit(1))
        existing_data = result.scalar_one_or_none()
        
        if existing_data:
            print("数据库中已存在数据，跳过导入")
            return
        
        print("开始导入数据...")
        batch_size = 1000
        total_imported = 0
        arbitrage_count = 0
        
        trade_data_list = []
        
        for idx, row in df.iterrows():
            # 解析时间
            time_align = datetime.strptime(row['time_align'], '%Y-%m-%d %H:%M')
            
            # 计算套利机会
            is_arbitrage, arbitrage_profit = calculate_arbitrage_profit(
                price_b=row['price_b'],
                price_u=row['price_u'],
                eth_vol_u=row['eth_vol_u']
            )
            
            if is_arbitrage:
                arbitrage_count += 1
            
            # 创建数据库记录
            trade_data = TradeData(
                time_align=time_align,
                price_b=row['price_b'],
                price_u=row['price_u'],
                eth_vol_b=row['eth_vol_b'],
                eth_vol_u=row['eth_vol_u'],
                usdt_vol_b=row['usdt_vol_b'],
                usdt_vol_u=row['usdt_vol_u'],
                is_arbitrage_opportunity=is_arbitrage,
                arbitrage_profit=arbitrage_profit
            )
            
            trade_data_list.append(trade_data)
            
            # 批量插入
            if len(trade_data_list) >= batch_size:
                session.add_all(trade_data_list)
                await session.commit()
                total_imported += len(trade_data_list)
                print(f"已导入 {total_imported} 条记录...")
                trade_data_list = []
        
        # 插入剩余数据
        if trade_data_list:
            session.add_all(trade_data_list)
            await session.commit()
            total_imported += len(trade_data_list)
        
        print(f"导入完成！")
        print(f"总记录数: {total_imported}")
        print(f"套利机会数: {arbitrage_count}")
        print(f"套利机会占比: {arbitrage_count/total_imported*100:.2f}%")


if __name__ == "__main__":
    asyncio.run(import_csv_data())
