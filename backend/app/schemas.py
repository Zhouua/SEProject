# backend/app/schemas.py

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


# ======= 基础数据模型 =======

class BinanceDataBase(BaseModel):
    id: Optional[int] = Field(None, description="记录ID")
    time_align: datetime = Field(..., description="时间戳")
    price: float = Field(..., description="Binance价格（USDT）")
    eth_vol: float = Field(..., description="ETH交易量")
    usdt_vol: float = Field(..., description="USDT交易量")

    model_config = ConfigDict(from_attributes=True)


class UniswapDataBase(BaseModel):
    id: Optional[int] = Field(None, description="记录ID")
    time_align: datetime = Field(..., description="时间戳")
    price: float = Field(..., description="Uniswap价格（USDT）")
    eth_vol: float = Field(..., description="ETH交易量")
    usdt_vol: float = Field(..., description="USDT交易量")

    model_config = ConfigDict(from_attributes=True)


class ArbitrageDataBase(BaseModel):
    id: Optional[int] = Field(None, description="记录ID")
    time_align: datetime = Field(..., description="时间戳")
    binance_id: int = Field(..., description="关联Binance数据ID")
    uniswap_id: int = Field(..., description="关联Uniswap数据ID")
    arbitrage_profit: Optional[float] = Field(None, description="套利利润（USDT）")
    is_arbitrage_opportunity: bool = Field(False, description="是否为套利机会")
    profit_percentage: Optional[float] = Field(None, description="获利百分比(%)")  # 🆕
    opportunity_score: Optional[float] = Field(None, description="套利机会评分")  # 🆕

    model_config = ConfigDict(from_attributes=True)





# ======= 价格相关模型 =======

class ExchangePriceData(BaseModel):
    price: float = Field(..., description="价格（USDT）")
    eth_volume: float = Field(..., description="ETH交易量")
    usdt_volume: float = Field(..., description="USDT交易量")


class PriceDataItem(BaseModel):
    time: str = Field(..., description="时间戳（ISO格式）")
    binance: ExchangePriceData = Field(..., description="Binance数据")
    uniswap: ExchangePriceData = Field(..., description="Uniswap数据")
    price_diff: float = Field(..., description="价格差（Binance - Uniswap）")
    price_diff_percent: float = Field(..., description="价格差百分比")


class PriceListResponse(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    count: int = Field(..., description="返回记录数量")
    data: List[PriceDataItem] = Field(..., description="价格数据列表")


class LatestPriceData(BaseModel):
    time: str = Field(..., description="时间戳（ISO格式）")
    binance: ExchangePriceData = Field(..., description="Binance数据")
    uniswap: ExchangePriceData = Field(..., description="Uniswap数据")
    price_diff: float = Field(..., description="价格差")


class LatestPriceResponse(BaseModel):
    success: bool = Field(..., description="请求是否成功")
    message: Optional[str] = Field(None, description="错误消息")
    data: Optional[LatestPriceData] = Field(None, description="最新价格数据")


# ======= 套利相关模型 =======

class ArbitrageOpportunityItem(BaseModel):
    time: str = Field(..., description="时间戳（ISO格式）")
    binance_price: float = Field(..., description="Binance价格")
    uniswap_price: float = Field(..., description="Uniswap价格")
    price_diff: float = Field(..., description="价格差")
    price_diff_percent: float = Field(..., description="价格差百分比")
    eth_volume_uniswap: float = Field(..., description="Uniswap ETH交易量")
    potential_profit_usdt: float = Field(..., description="潜在利润（USDT）")
    profit_percentage: Optional[float] = Field(None, description="获利百分比(%)")  # 🆕
    opportunity_score: Optional[float] = Field(None, description="套利机会评分")  # 🆕
    strategy: str = Field(..., description="套利策略描述")


class ArbitrageOpportunitiesResponse(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    count: int = Field(..., description="返回记录数量")
    data: List[ArbitrageOpportunityItem] = Field(..., description="套利机会列表")


class TopArbitrageItem(BaseModel):
    rank: int = Field(..., description="排名")
    time: str = Field(..., description="时间戳（ISO格式）")
    binance_price: float = Field(..., description="Binance价格")
    uniswap_price: float = Field(..., description="Uniswap价格")
    price_diff: float = Field(..., description="价格差")
    eth_volume: float = Field(..., description="ETH交易量")
    potential_profit_usdt: float = Field(..., description="潜在利润（USDT）")
    profit_percentage: Optional[float] = Field(None, description="获利百分比(%)")  # 🆕
    opportunity_score: Optional[float] = Field(None, description="套利机会评分")  # 🆕


class TopArbitrageResponse(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    count: int = Field(..., description="返回记录数量")
    data: List[TopArbitrageItem] = Field(..., description="Top套利机会列表")


# ======= 统计相关模型 =======

class ArbitrageStatistics(BaseModel):
    count: int = Field(..., description="套利机会数量")
    percentage: float = Field(..., description="套利机会占比（%）")
    min_profit: float = Field(..., description="最小利润（USDT）")
    max_profit: float = Field(..., description="最大利润（USDT）")
    avg_profit: float = Field(..., description="平均利润（USDT）")
    total_potential_profit: float = Field(..., description="总潜在利润（USDT）")


class ExchangePriceStatistics(BaseModel):
    min: float = Field(..., description="最低价格")
    max: float = Field(..., description="最高价格")
    avg: float = Field(..., description="平均价格")


class PriceStatistics(BaseModel):
    binance: ExchangePriceStatistics = Field(..., description="Binance价格统计")
    uniswap: ExchangePriceStatistics = Field(..., description="Uniswap价格统计")


class TimeRange(BaseModel):
    start: Optional[str] = Field(None, description="开始时间（ISO格式）")
    end: Optional[str] = Field(None, description="结束时间（ISO格式）")


class StatisticsOverviewData(BaseModel):
    total_records: int = Field(..., description="总记录数")
    arbitrage_opportunities: ArbitrageStatistics = Field(..., description="套利机会统计")
    price_statistics: PriceStatistics = Field(..., description="价格统计")
    time_range: TimeRange = Field(..., description="时间范围")


class StatisticsOverviewResponse(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    data: StatisticsOverviewData = Field(..., description="统计数据")


# ======= 通用响应模型 =======


class ErrorResponse(BaseModel):
    success: bool = Field(False, description="请求失败")
    message: str = Field(..., description="错误消息")
    error_code: Optional[str] = Field(None, description="错误代码")


class SuccessResponse(BaseModel):
    success: bool = Field(True, description="请求成功")
    message: str = Field(..., description="成功消息")


# ======= 查询参数模型 =======

class TimeRangeQuery(BaseModel):
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")


class PaginationQuery(BaseModel):
    limit: int = Field(100, ge=1, le=1000, description="返回记录数量")
    offset: int = Field(0, ge=0, description="跳过记录数量")


class ArbitrageQuery(TimeRangeQuery, PaginationQuery):
    min_profit: float = Field(0, ge=0, description="最小获利金额（USDT）")
    sort_by: str = Field("profit_desc", description="排序方式")
