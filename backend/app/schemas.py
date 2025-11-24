# backend/app/schemas.py
"""
Pydantic数据模型定义
用于API请求/响应的数据验证和序列化
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


# ==================== 基础数据模型 ====================

class ExchangePriceData(BaseModel):
    """交易所价格数据"""
    price: float = Field(..., description="价格（USDT）")
    eth_volume: float = Field(..., description="ETH交易量")
    usdt_volume: float = Field(..., description="USDT交易量")


class TradeDataBase(BaseModel):
    """交易数据基础模型"""
    time_align: datetime = Field(..., description="对齐时间戳")
    price_b: float = Field(..., description="Binance价格")
    price_u: float = Field(..., description="Uniswap价格")
    eth_vol_b: float = Field(..., description="Binance ETH交易量")
    eth_vol_u: float = Field(..., description="Uniswap ETH交易量")
    usdt_vol_b: float = Field(..., description="Binance USDT交易量")
    usdt_vol_u: float = Field(..., description="Uniswap USDT交易量")


class TradeDataResponse(TradeDataBase):
    """交易数据完整响应模型（包含数据库字段）"""
    id: int = Field(..., description="记录ID")
    arbitrage_profit: Optional[float] = Field(None, description="套利利润（USDT）")
    is_arbitrage_opportunity: bool = Field(False, description="是否为套利机会")
    
    model_config = ConfigDict(from_attributes=True)


# ==================== 价格相关模型 ====================

class PriceDataItem(BaseModel):
    """单条价格数据项（用于prices路由）"""
    time: str = Field(..., description="时间戳（ISO格式）")
    binance: ExchangePriceData = Field(..., description="Binance数据")
    uniswap: ExchangePriceData = Field(..., description="Uniswap数据")
    price_diff: float = Field(..., description="价格差（Binance - Uniswap）")
    price_diff_percent: float = Field(..., description="价格差百分比")


class PriceListResponse(BaseModel):
    """价格列表响应"""
    success: bool = Field(True, description="请求是否成功")
    count: int = Field(..., description="返回记录数量")
    data: List[PriceDataItem] = Field(..., description="价格数据列表")


class LatestPriceData(BaseModel):
    """最新价格数据"""
    time: str = Field(..., description="时间戳（ISO格式）")
    binance: ExchangePriceData = Field(..., description="Binance数据")
    uniswap: ExchangePriceData = Field(..., description="Uniswap数据")
    price_diff: float = Field(..., description="价格差")


class LatestPriceResponse(BaseModel):
    """最新价格响应"""
    success: bool = Field(..., description="请求是否成功")
    message: Optional[str] = Field(None, description="错误消息")
    data: Optional[LatestPriceData] = Field(None, description="最新价格数据")


# ==================== 套利相关模型 ====================

class ArbitrageOpportunityItem(BaseModel):
    """单个套利机会"""
    time: str = Field(..., description="时间戳（ISO格式）")
    binance_price: float = Field(..., description="Binance价格")
    uniswap_price: float = Field(..., description="Uniswap价格")
    price_diff: float = Field(..., description="价格差")
    price_diff_percent: float = Field(..., description="价格差百分比")
    eth_volume_uniswap: float = Field(..., description="Uniswap ETH交易量")
    potential_profit_usdt: float = Field(..., description="潜在利润（USDT）")
    strategy: str = Field(..., description="套利策略描述")


class ArbitrageOpportunitiesResponse(BaseModel):
    """套利机会列表响应"""
    success: bool = Field(True, description="请求是否成功")
    count: int = Field(..., description="返回记录数量")
    data: List[ArbitrageOpportunityItem] = Field(..., description="套利机会列表")


class TopArbitrageItem(BaseModel):
    """Top套利机会项"""
    rank: int = Field(..., description="排名")
    time: str = Field(..., description="时间戳（ISO格式）")
    binance_price: float = Field(..., description="Binance价格")
    uniswap_price: float = Field(..., description="Uniswap价格")
    price_diff: float = Field(..., description="价格差")
    eth_volume: float = Field(..., description="ETH交易量")
    potential_profit_usdt: float = Field(..., description="潜在利润（USDT）")


class TopArbitrageResponse(BaseModel):
    """Top套利机会响应"""
    success: bool = Field(True, description="请求是否成功")
    count: int = Field(..., description="返回记录数量")
    data: List[TopArbitrageItem] = Field(..., description="Top套利机会列表")


# ==================== 统计相关模型 ====================

class ArbitrageStatistics(BaseModel):
    """套利统计数据"""
    count: int = Field(..., description="套利机会数量")
    percentage: float = Field(..., description="套利机会占比（%）")
    min_profit: float = Field(..., description="最小利润（USDT）")
    max_profit: float = Field(..., description="最大利润（USDT）")
    avg_profit: float = Field(..., description="平均利润（USDT）")
    total_potential_profit: float = Field(..., description="总潜在利润（USDT）")


class ExchangePriceStatistics(BaseModel):
    """交易所价格统计"""
    min: float = Field(..., description="最低价格")
    max: float = Field(..., description="最高价格")
    avg: float = Field(..., description="平均价格")


class PriceStatistics(BaseModel):
    """价格统计数据"""
    binance: ExchangePriceStatistics = Field(..., description="Binance价格统计")
    uniswap: ExchangePriceStatistics = Field(..., description="Uniswap价格统计")


class TimeRange(BaseModel):
    """时间范围"""
    start: Optional[str] = Field(None, description="开始时间（ISO格式）")
    end: Optional[str] = Field(None, description="结束时间（ISO格式）")


class StatisticsOverviewData(BaseModel):
    """统计概览数据"""
    total_records: int = Field(..., description="总记录数")
    arbitrage_opportunities: ArbitrageStatistics = Field(..., description="套利机会统计")
    price_statistics: PriceStatistics = Field(..., description="价格统计")
    time_range: TimeRange = Field(..., description="时间范围")


class StatisticsOverviewResponse(BaseModel):
    """统计概览响应"""
    success: bool = Field(True, description="请求是否成功")
    data: StatisticsOverviewData = Field(..., description="统计数据")


# ==================== 通用响应模型 ====================

class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = Field(False, description="请求失败")
    message: str = Field(..., description="错误消息")
    error_code: Optional[str] = Field(None, description="错误代码")


class SuccessResponse(BaseModel):
    """通用成功响应"""
    success: bool = Field(True, description="请求成功")
    message: str = Field(..., description="成功消息")


# ==================== 查询参数模型 ====================

class TimeRangeQuery(BaseModel):
    """时间范围查询参数"""
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")


class PaginationQuery(BaseModel):
    """分页查询参数"""
    limit: int = Field(100, ge=1, le=1000, description="返回记录数量")
    offset: int = Field(0, ge=0, description="跳过记录数量")


class ArbitrageQuery(TimeRangeQuery, PaginationQuery):
    """套利查询参数"""
    min_profit: float = Field(0, ge=0, description="最小获利金额（USDT）")
    sort_by: str = Field("profit_desc", description="排序方式")
