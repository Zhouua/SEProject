from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 修改导入路径 - 使用相对导入
from .routers import prices, arbitrage, statistics, liquidity

app = FastAPI(
    title="Crypto Arbitrage API",
    description="ETH/USDT套利机会分析API",
    version="1.0.0"
)

# 配置CORS（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(prices.router)
app.include_router(arbitrage.router)
app.include_router(statistics.router)
app.include_router(liquidity.router)

@app.get("/")
async def root():
    return {
        "message": "Crypto Arbitrage API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查接口，用于监控服务状态"""
    from .database import engine
    from sqlalchemy import text
    
    try:
        # 测试数据库连接
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
