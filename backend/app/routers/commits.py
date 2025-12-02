from fastapi import APIRouter, HTTPException
from typing import List
import subprocess
from datetime import datetime, timedelta
import re
import os

router = APIRouter(
    prefix="/api/commits",
    tags=["commits"]
)

def parse_time_ago(time_str: str) -> datetime:
    """将 git log 的相对时间转换为 datetime 对象"""
    now = datetime.now()
    
    # 匹配各种时间格式
    patterns = [
        (r'(\d+)\s*秒钟?前', lambda m: now - timedelta(seconds=int(m.group(1)))),
        (r'(\d+)\s*分钟前', lambda m: now - timedelta(minutes=int(m.group(1)))),
        (r'(\d+)\s*小时前', lambda m: now - timedelta(hours=int(m.group(1)))),
        (r'(\d+)\s*天前', lambda m: now - timedelta(days=int(m.group(1)))),
        (r'(\d+)\s*周前', lambda m: now - timedelta(weeks=int(m.group(1)))),
        (r'(\d+)\s*月前', lambda m: now - timedelta(days=int(m.group(1)) * 30)),
        (r'(\d+)\s*年前', lambda m: now - timedelta(days=int(m.group(1)) * 365)),
        (r'(\d+)\s*seconds? ago', lambda m: now - timedelta(seconds=int(m.group(1)))),
        (r'(\d+)\s*minutes? ago', lambda m: now - timedelta(minutes=int(m.group(1)))),
        (r'(\d+)\s*hours? ago', lambda m: now - timedelta(hours=int(m.group(1)))),
        (r'(\d+)\s*days? ago', lambda m: now - timedelta(days=int(m.group(1)))),
        (r'(\d+)\s*weeks? ago', lambda m: now - timedelta(weeks=int(m.group(1)))),
        (r'(\d+)\s*months? ago', lambda m: now - timedelta(days=int(m.group(1)) * 30)),
        (r'(\d+)\s*years? ago', lambda m: now - timedelta(days=int(m.group(1)) * 365)),
    ]
    
    for pattern, converter in patterns:
        match = re.match(pattern, time_str.strip())
        if match:
            return converter(match)
    
    # 默认返回当前时间
    return now

def get_commit_type(message: str) -> str:
    """根据 commit message 判断通知类型"""
    message_lower = message.lower()
    
    if message_lower.startswith('feat'):
        return 'success'
    elif message_lower.startswith('fix'):
        return 'warning'
    elif message_lower.startswith('chore') or message_lower.startswith('docs'):
        return 'warning'
    elif message_lower.startswith('merge'):
        return 'info'
    else:
        return 'info'

@router.get("/latest")
async def get_latest_commits(limit: int = 10):
    """
    获取最新的 git commit 记录
    
    参数:
    - limit: 返回的 commit 数量，默认 10 条
    """
    try:
        # 自动检测项目根目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '../../..'))
        
        # 如果设置了环境变量，优先使用环境变量
        git_repo_path = os.getenv('GIT_REPO_PATH', project_root)
        
        # 验证路径是否存在
        if not os.path.exists(git_repo_path):
            raise HTTPException(status_code=500, detail=f"Git repository path not found: {git_repo_path}")
        
        # 执行 git log 命令获取提交历史
        # 格式: hash|subject|relative_time|author_name
        result = subprocess.run(
            ['git', 'log', f'--pretty=format:%h|%s|%cr|%an', f'-{limit}'],
            capture_output=True,
            text=True,
            cwd=git_repo_path  # 使用动态检测的项目根目录
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Git command failed: {result.stderr}")
        
        commits = []
        lines = result.stdout.strip().split('\n')
        
        for idx, line in enumerate(lines):
            if not line:
                continue
                
            parts = line.split('|')
            if len(parts) != 4:
                continue
            
            hash_short, subject, time_ago, author = parts
            
            commit = {
                "id": idx + 1,
                "hash": hash_short,
                "title": subject,
                "author": author,
                "time_ago": time_ago,
                "timestamp": parse_time_ago(time_ago).isoformat(),
                "type": get_commit_type(subject),
                "read": idx >= 3  # 前3条标记为未读
            }
            commits.append(commit)
        
        return {
            "success": True,
            "data": commits,
            "count": len(commits)
        }
        
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to get git commits: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/count")
async def get_unread_count():
    """获取未读通知数量"""
    try:
        # 这里可以根据实际需求调整逻辑
        # 例如：只计算最近24小时内的提交为未读
        # 自动检测项目根目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '../../..'))
        git_repo_path = os.getenv('GIT_REPO_PATH', project_root)
        
        result = subprocess.run(
            ['git', 'log', '--pretty=format:%cr', '--since="24 hours ago"'],
            capture_output=True,
            text=True,
            cwd=git_repo_path
        )
        
        if result.returncode == 0:
            count = len([line for line in result.stdout.strip().split('\n') if line])
            return {
                "success": True,
                "unread_count": min(count, 3)  # 最多显示3个未读
            }
        else:
            return {"success": False, "unread_count": 0}
            
    except Exception as e:
        return {"success": False, "unread_count": 0, "error": str(e)}
