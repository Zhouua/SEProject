
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models import Base

# 将DATABASE_URL转换为async版本
DATABASE_URL_ASYNC = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# 创建异步数据库引擎
# echo=True 会输出所有SQL语句，仅在调试时使用
# 生产环境建议设置为 False，避免大量日志影响性能
# pool_pre_ping=True 可以在每次连接前检查连接是否有效
engine = create_async_engine(
    DATABASE_URL_ASYNC,
    echo=False,
    pool_size=5,           # 减小连接池大小
    max_overflow=10,       # 超过pool_size后最多再创建的连接数
    pool_timeout=10,       # 获取连接的超时时间（秒）- 减小超时时间
    pool_recycle=3600,     # 连接回收时间（秒），防止连接长时间不用被数据库断开
    pool_pre_ping=True,    # 每次使用连接前先ping一下，确保连接有效
    connect_args={
        "timeout": 5,      # 连接超时时间（秒）
        "command_timeout": 5,  # 命令超时时间（秒）
    }
)

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
