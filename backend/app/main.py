from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 修改导入路径 - 使用相对导入
from .routers import prices, arbitrage, statistics

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

@app.get("/")
async def root():
    return {
        "message": "Crypto Arbitrage API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
