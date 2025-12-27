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

    arbitrage_records = relationship("ArbitrageData", back_populates="binance_data")

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

    arbitrage_records = relationship("ArbitrageData", back_populates="uniswap_data")

    def __repr__(self):
        return f"<UniswapData(time={self.time_align}, price={self.price})>"


class ArbitrageData(Base):
    """
    套利数据表
    """
    __tablename__ = "arbitrage_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_align = Column(DateTime, nullable=False, index=True)

    binance_id = Column(Integer, ForeignKey("binance_data.id"), nullable=False)
    uniswap_id = Column(Integer, ForeignKey("uniswap_data.id"), nullable=False)

    arbitrage_profit = Column(Float, nullable=True)
    profit_rate = Column(Float, nullable=True)  # 利润率
    score = Column(Float, nullable=True)  # 多因子评分
    direction = Column(Integer, nullable=True)  # 0: U2B, 1: B2U
    is_arbitrage_opportunity = Column(Boolean, default=False)

    binance_data = relationship("BinanceData", back_populates="arbitrage_records")
    uniswap_data = relationship("UniswapData", back_populates="arbitrage_records")

    __table_args__ = (
        Index('idx_arbitrage_time_profit', 'time_align', 'arbitrage_profit'),
        Index('idx_arbitrage_score', 'score'),
        Index('idx_arbitrage_direction', 'direction'),
    )

    def __repr__(self):
        return f"<ArbitrageData(time={self.time_align}, profit={self.arbitrage_profit}, rate={self.profit_rate}, score={self.score}, dir={self.direction})>"
