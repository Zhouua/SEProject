import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL连接字符串，格式：postgresql://user:password@host:port/dbname
    DATABASE_URL: str = "postgresql://postgres:521346Aa@localhost:5432/arbitrage_db"

    # 其他可扩展配置项
    APP_NAME: str = "ArbitrageDetectionAPI"
    DEBUG: bool = True

    class Config:
        env_file = ".env"  # 读取同目录的 .env 环境变量文件


settings = Settings()
