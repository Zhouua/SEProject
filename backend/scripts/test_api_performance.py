#!/usr/bin/env python3
"""
API 性能测试脚本
自动测试所有后端 API 的响应时间并生成报告
"""

import requests
import time
import statistics
from typing import List, Dict
from datetime import datetime

# ANSI 颜色代码
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def test_api(url: str, num_requests: int = 20, timeout: int = 10) -> Dict:
    """
    测试单个 API 的性能
    
    Args:
        url: API 完整 URL
        num_requests: 请求次数
        timeout: 超时时间（秒）
    
    Returns:
        包含性能指标的字典
    """
    times = []
    failed = 0
    
    print(f"\n{'='*60}")
    print(f"测试: {BLUE}{url}{RESET}")
    print(f"请求次数: {num_requests}")
    print("-" * 60)
    
    for i in range(num_requests):
        start = time.time()
        try:
            response = requests.get(url, timeout=timeout)
            end = time.time()
            
            elapsed = (end - start) * 1000  # 转换为毫秒
            
            if response.status_code == 200:
                times.append(elapsed)
                status = f"{GREEN}✓{RESET}"
            else:
                failed += 1
                status = f"{RED}✗ ({response.status_code}){RESET}"
            
            # 显示进度
            if (i + 1) % 5 == 0 or i == num_requests - 1:
                print(f"  进度: [{i+1}/{num_requests}] {status} {elapsed:.2f}ms")
                
        except requests.exceptions.Timeout:
            failed += 1
            print(f"  请求 {i+1}: {RED}超时{RESET}")
        except Exception as e:
            failed += 1
            print(f"  请求 {i+1}: {RED}异常 - {str(e)}{RESET}")
    
    if not times:
        print(f"{RED}❌ 所有请求失败{RESET}")
        return None
    
    # 计算统计数据
    avg = statistics.mean(times)
    median = statistics.median(times)
    stdev = statistics.stdev(times) if len(times) > 1 else 0
    min_time = min(times)
    max_time = max(times)
    
    # 计算百分位数
    sorted_times = sorted(times)
    p50 = sorted_times[int(len(sorted_times) * 0.50)] if sorted_times else 0
    p95 = sorted_times[min(int(len(sorted_times) * 0.95), len(sorted_times)-1)] if sorted_times else 0
    p99 = sorted_times[min(int(len(sorted_times) * 0.99), len(sorted_times)-1)] if sorted_times else 0
    
    return {
        'url': url,
        'success': len(times),
        'failed': failed,
        'avg': avg,
        'median': median,
        'stdev': stdev,
        'min': min_time,
        'max': max_time,
        'p50': p50,
        'p95': p95,
        'p99': p99
    }

def print_result(result: Dict):
    """打印单个 API 的测试结果"""
    if not result:
        return
    
    # 判断性能等级
    avg = result['avg']
    if avg < 100:
        status = f"{GREEN}优秀{RESET}"
    elif avg < 300:
        status = f"{YELLOW}良好{RESET}"
    else:
        status = f"{RED}需优化{RESET}"
    
    print(f"\n{BLUE}📊 测试结果{RESET}")
    print(f"  ✅ 成功: {result['success']} | ❌ 失败: {result['failed']}")
    print(f"  平均响应时间: {result['avg']:.2f} ms {status}")
    print(f"  中位数: {result['median']:.2f} ms")
    print(f"  标准差: {result['stdev']:.2f} ms")
    print(f"  最快: {result['min']:.2f} ms")
    print(f"  最慢: {result['max']:.2f} ms")
    print(f"  P50: {result['p50']:.2f} ms")
    print(f"  P95: {result['p95']:.2f} ms")
    print(f"  P99: {result['p99']:.2f} ms")

def print_summary_table(results: List[Dict]):
    """打印汇总表格"""
    print(f"\n{'='*80}")
    print(f"{BLUE}📈 性能测试汇总报告{RESET}")
    print(f"{'='*80}")
    
    # 表头
    print(f"{'API 端点':<45} {'平均':<12} {'P95':<12} {'P99':<12} {'状态':<8}")
    print("-" * 80)
    
    for r in results:
        # 提取 API 名称
        path = r['url'].split('://')[1] if '://' in r['url'] else r['url']
        api_path = '/'.join(path.split('/')[2:])  # 去掉 host:port
        
        # 截断过长的 URL
        if len(api_path) > 42:
            api_path = api_path[:39] + "..."
        
        # 状态标识
        if r['avg'] < 100:
            status = f"{GREEN}✅{RESET}"
        elif r['avg'] < 300:
            status = f"{YELLOW}⚠️{RESET}"
        else:
            status = f"{RED}❌{RESET}"
        
        print(f"{api_path:<45} {r['avg']:<12.2f} {r['p95']:<12.2f} {r['p99']:<12.2f} {status}")
    
    # 计算总体统计
    all_avgs = [r['avg'] for r in results]
    overall_avg = statistics.mean(all_avgs)
    
    print("-" * 80)
    print(f"{'总体平均响应时间':<45} {overall_avg:<12.2f} ms")
    print("=" * 80)

def generate_markdown_report(results: List[Dict], filename: str = "performance_report.md"):
    """生成 Markdown 格式的测试报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# API 性能测试报告\n\n")
        f.write(f"**测试时间**: {timestamp}\n\n")
        f.write(f"**测试环境**: 本地开发环境\n\n")
        
        f.write(f"## 测试结果\n\n")
        f.write(f"| API 端点 | 平均响应 | P50 | P95 | P99 | 最小 | 最大 | 状态 |\n")
        f.write(f"|----------|----------|-----|-----|-----|------|------|------|\n")
        
        for r in results:
            path = r['url'].split('://')[1] if '://' in r['url'] else r['url']
            api_path = '/'.join(path.split('/')[2:])
            
            status = "✅" if r['avg'] < 100 else ("⚠️" if r['avg'] < 300 else "❌")
            
            f.write(f"| {api_path} | {r['avg']:.2f}ms | {r['p50']:.2f}ms | "
                   f"{r['p95']:.2f}ms | {r['p99']:.2f}ms | {r['min']:.2f}ms | "
                   f"{r['max']:.2f}ms | {status} |\n")
        
        # 添加性能标准说明
        f.write(f"\n## 性能评级标准\n\n")
        f.write(f"- ✅ **优秀**: < 100ms\n")
        f.write(f"- ⚠️ **良好**: 100-300ms\n")
        f.write(f"- ❌ **需优化**: > 300ms\n")
        
        # 添加测试配置
        f.write(f"\n## 测试配置\n\n")
        f.write(f"- **请求次数**: 20 次/端点\n")
        f.write(f"- **超时时间**: 10 秒\n")
        f.write(f"- **并发数**: 1（串行测试）\n")
    
    print(f"\n{GREEN}✅ 报告已生成: {filename}{RESET}")

def main():
    """主函数"""
    print(f"\n{BLUE}╔════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║              API 性能测试工具                              ║{RESET}")
    print(f"{BLUE}╚════════════════════════════════════════════════════════════╝{RESET}")
    
    # 定义要测试的 API
    base_url = "http://localhost:8000"
    
    apis = [
        f"{base_url}/api/prices/?limit=100",
        f"{base_url}/api/prices/latest",
        f"{base_url}/api/arbitrage/?limit=100",
        f"{base_url}/api/arbitrage/top?top_n=10",
        f"{base_url}/api/liquidity/analysis",
        f"{base_url}/api/commits/latest?limit=10",
        f"{base_url}/api/commits/count",
        f"{base_url}/api/statistics/overview",
    ]
    
    # 测试每个 API
    results = []
    for api in apis:
        result = test_api(api, num_requests=20)
        if result:
            print_result(result)
            results.append(result)
    
    # 打印汇总表格
    if results:
        print_summary_table(results)
        
        # 生成 Markdown 报告
        generate_markdown_report(results, "performance_report.md")
        
        print(f"\n{GREEN}✅ 测试完成！{RESET}")
    else:
        print(f"\n{RED}❌ 所有测试失败，请检查后端服务是否运行{RESET}")
        print(f"\n启动后端服务:")
        print(f"  cd backend")
        print(f"  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⚠️  测试被用户中断{RESET}")
    except Exception as e:
        print(f"\n{RED}❌ 发生错误: {str(e)}{RESET}")
