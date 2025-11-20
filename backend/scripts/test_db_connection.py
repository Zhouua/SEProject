import sys
import os
import asyncio

# 将backend目录添加到Python路径，使得可以导入app模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.database import engine


async def test_connection():
    try:
        # 尝试连接数据库，执行SELECT 1语句
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            scalar_result = result.scalar()
            print("✅ Database connected successfully, test query result:", scalar_result)
    except Exception as e:
        print("❌ Database connection failed:", str(e))
    finally:
        # 关闭引擎
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_connection())
