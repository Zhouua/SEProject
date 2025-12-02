#!/usr/bin/env python
"""
启动服务器的辅助脚本，带有更好的错误处理和日志
"""
import sys
import os

# 确保在正确的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    
    # 启动服务器
    print("🚀 Starting Crypto Arbitrage API Server...")
    print("📍 Server will be available at:")
    print("   - http://localhost:8000")
    print("   - http://127.0.0.1:8000")
    print("   - http://0.0.0.0:8000")
    print("📖 API Documentation:")
    print("   - Swagger UI: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")
    print("\n⏳ Initializing...")
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True,
            # 添加超时配置
            timeout_keep_alive=5,
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
