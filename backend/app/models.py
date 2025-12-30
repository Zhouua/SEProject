# app/models.py

from sqlalchemy import Column, Integer, Float, DateTime, Boolean, Index, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class BinanceData(Base):
    """
    Binance交易数据表
    """
    __tablename__ = "binance_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_align = Column(DateTime, nullable=False, index=True)

    price = Column(Float, nullable=False)
    eth_vol = Column(Float, nullable=False)
    usdt_vol = Column(Float, nullable=False)

    def __repr__(self):
        return f"<BinanceData(time={self.time_align}, price={self.price})>"


class UniswapData(Base):
    """
    Uniswap交易数据表
    """
    __tablename__ = "uniswap_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_align = Column(DateTime, nullable=False, index=True)

    price = Column(Float, nullable=False)
    eth_vol = Column(Float, nullable=False)
    usdt_vol = Column(Float, nullable=False)

    def __repr__(self):
        return f"<UniswapData(time={self.time_align}, price={self.price})>"


class ArbitrageData(Base):
    """
    套利数据表 - 仅存储套利机会
    """
    __tablename__ = "arbitrage_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_align = Column(DateTime, nullable=False, index=True)

    trade_id = Column(Integer, ForeignKey("trade_data.id"), nullable=False)

    arbitrage_profit = Column(Float, nullable=True)
    profit_rate = Column(Float, nullable=True)  # 利润率
    score = Column(Float, nullable=True)  # 多因子评分
    direction = Column(Integer, nullable=True)  # 0: U2B, 1: B2U

    trade_data = relationship("TradeData", back_populates="arbitrage_records")

    __table_args__ = (
        Index('idx_arbitrage_time_profit', 'time_align', 'arbitrage_profit'),
        Index('idx_arbitrage_score', 'score'),
        Index('idx_arbitrage_direction', 'direction'),
        Index('idx_arbitrage_trade_id', 'trade_id'),
    )

    def __repr__(self):
        return f"<ArbitrageData(time={self.time_align}, profit={self.arbitrage_profit}, rate={self.profit_rate}, score={self.score}, dir={self.direction})>"


class TradeData(Base):
    """
    交易数据表 - 直接存储价格和交易量数据
    """
    __tablename__ = "trade_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_align = Column(DateTime, nullable=False, index=True)

    binance_price = Column(Float, nullable=False)
    binance_vol = Column(Float, nullable=False)
    uniswap_price = Column(Float, nullable=False)
    uniswap_vol = Column(Float, nullable=False)
    is_arbitrage_opportunity = Column(Boolean, nullable=False, default=False, index=True)
    score = Column(Float, nullable=True)  # 多因子评分

    arbitrage_records = relationship("ArbitrageData", back_populates="trade_data")

    __table_args__ = (
        Index('idx_trade_time', 'time_align'),
        Index('idx_trade_arbitrage', 'is_arbitrage_opportunity'),
        Index('idx_trade_score', 'score'),
    )

    def __repr__(self):
        return f"<TradeData(time={self.time_align}, binance_price={self.binance_price}, uniswap_price={self.uniswap_price}, is_arb={self.is_arbitrage_opportunity}, score={self.score})>"
