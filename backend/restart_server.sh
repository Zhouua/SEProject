#!/bin/bash
# 重启服务器脚本

echo "🔍 Checking for processes on port 8000..."
PIDS=$(lsof -ti :8000 | grep -v "Code Helper" || true)

if [ -z "$PIDS" ]; then
    echo "✅ No Python processes found on port 8000"
else
    echo "⚠️  Found processes: $PIDS"
    echo "🔨 Killing processes..."
    for PID in $PIDS; do
        echo "   Killing PID: $PID"
        kill -9 $PID 2>/dev/null || true
    done
    sleep 1
    echo "✅ Processes killed"
fi

echo ""
echo "🚀 Starting server..."
echo "📍 Server will be available at http://localhost:8000/docs"
echo ""

# 启动服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
