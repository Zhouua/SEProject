"""
测试导出功能的脚本
"""
import requests
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8000"

def test_export_endpoints():
    """测试所有导出接口"""
    
    print("=" * 60)
    print("测试导出功能")
    print("=" * 60)
    
    # 测试参数
    start_time = "2025-09-01 00:00:00"
    end_time = "2025-09-30 23:59:59"
    
    endpoints = [
        {
            "name": "导出套利机会CSV",
            "url": f"{BASE_URL}/api/export/arbitrage-opportunities/csv",
            "params": {
                "start_time": start_time,
                "end_time": end_time,
                "min_profit": 0
            }
        },
        {
            "name": "导出价格数据CSV",
            "url": f"{BASE_URL}/api/export/price-data/csv",
            "params": {
                "start_time": start_time,
                "end_time": end_time,
                "limit": 1000
            }
        },
        {
            "name": "导出所有数据CSV",
            "url": f"{BASE_URL}/api/export/all-data/csv",
            "params": {
                "start_time": start_time,
                "end_time": end_time
            }
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n测试: {endpoint['name']}")
        print(f"URL: {endpoint['url']}")
        print(f"参数: {endpoint['params']}")
        
        try:
            response = requests.get(endpoint['url'], params=endpoint['params'], timeout=30)
            
            if response.status_code == 200:
                # 检查是否是CSV内容
                content_type = response.headers.get('Content-Type', '')
                if 'csv' in content_type or 'text/csv' in content_type:
                    # 获取前几行内容
                    content_lines = response.text.split('\n')[:5]
                    print(f"✓ 成功! 状态码: {response.status_code}")
                    print(f"  Content-Type: {content_type}")
                    print(f"  内容预览 (前5行):")
                    for line in content_lines:
                        print(f"    {line[:100]}...")  # 只显示前100个字符
                else:
                    print(f"✓ 响应成功，但Content-Type可能不正确: {content_type}")
                    print(f"  内容长度: {len(response.text)} 字节")
            else:
                print(f"✗ 失败! 状态码: {response.status_code}")
                print(f"  响应: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"✗ 连接失败! 请确保后端服务正在运行 (localhost:8000)")
            break
        except Exception as e:
            print(f"✗ 错误: {str(e)}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_export_endpoints()
