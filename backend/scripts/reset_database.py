import asyncio
from app.database import drop_tables, create_tables


async def reset_database():
    """删除所有表并重新创建"""
    print("⚠️  正在删除所有表...")
    await drop_tables()
    
    print("📝 正在重新创建表结构...")
    await create_tables()
    
    print("✅ 数据库重置完成！")


if __name__ == "__main__":
    asyncio.run(reset_database())
