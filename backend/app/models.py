from sqlalchemy import Column, Integer, Float, DateTime, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TradeData(Base):
    """
    交易数据表：存储Binance和Uniswap的对齐历史数据
    """
    __tablename__ = "trade_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # 时间戳（对齐后的时间）
    time_align = Column(DateTime, nullable=False, index=True)
    
    # Binance价格和交易量
    price_b = Column(Float, nullable=False)  # Binance价格
    eth_vol_b = Column(Float, nullable=False)  # Binance ETH交易量
    usdt_vol_b = Column(Float, nullable=False)  # Binance USDT交易量
    
    # Uniswap价格和交易量
    price_u = Column(Float, nullable=False)  # Uniswap价格
    eth_vol_u = Column(Float, nullable=False)  # Uniswap ETH交易量
    usdt_vol_u = Column(Float, nullable=False)  # Uniswap USDT交易量
    
    # 套利相关计算字段（可以在导入时预计算，提高查询效率）
    arbitrage_profit = Column(Float, nullable=True)  # 潜在套利获利金额（USDT）
    is_arbitrage_opportunity = Column(Boolean, default=False)  # 是否为套利机会
    
    # 创建复合索引，优化时间范围查询
    __table_args__ = (
        Index('idx_time_arbitrage', 'time_align', 'is_arbitrage_opportunity'),
        Index('idx_arbitrage_profit', 'arbitrage_profit'),
    )

    def __repr__(self):
        return f"<TradeData(time={self.time_align}, price_b={self.price_b}, price_u={self.price_u}, profit={self.arbitrage_profit})>"
