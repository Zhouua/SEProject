from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models import Base

# 将DATABASE_URL转换为async版本
DATABASE_URL_ASYNC = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# 创建异步数据库引擎
engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


# 获取数据库Session的依赖注入函数
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# 创建所有表
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created successfully!")


# 删除所有表（慎用，仅用于开发测试）
async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("⚠️ All tables dropped!")
