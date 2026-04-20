"""
会话管理模块

为每个用户创建独立的文件存储目录，解决并发场景下文件覆盖问题。

目录结构:
  images/{session_id}/white.png   - 用户上传的六面图片
  cube_results/{session_id}/      - 用户求解结果

生命周期:
  - 前端生成 UUID 作为 session_id
  - 后端收到请求时自动创建目录
  - 超过 24 小时的会话目录在服务启动时自动清理
"""

import os
import shutil
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_ROOT = os.path.join(BASE_DIR, "images")
RESULTS_ROOT = os.path.join(BASE_DIR, "cube_results")

SESSION_EXPIRE_HOURS = 24

_sessions = {}


def get_session_dir(session_id: str) -> dict:
    """获取会话的目录路径，自动创建目录。

    Args:
        session_id: 会话唯一标识（前端生成的 UUID）

    Returns:
        dict: 包含 images_dir 和 results_dir 的字典
    """
    images_dir = os.path.join(IMAGES_ROOT, session_id)
    results_dir = os.path.join(RESULTS_ROOT, session_id)

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    _sessions[session_id] = {
        "created_at": time.time(),
        "images_dir": images_dir,
        "results_dir": results_dir,
    }

    return {"images_dir": images_dir, "results_dir": results_dir}


def delete_session(session_id: str) -> bool:
    """删除会话的所有目录和文件。

    Args:
        session_id: 会话唯一标识

    Returns:
        bool: 是否成功删除
    """
    removed = False

    images_dir = os.path.join(IMAGES_ROOT, session_id)
    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)
        removed = True

    results_dir = os.path.join(RESULTS_ROOT, session_id)
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
        removed = True

    _sessions.pop(session_id, None)

    return removed


def cleanup_expired_sessions(max_age_hours: float = SESSION_EXPIRE_HOURS) -> int:
    """清理过期的会话目录。

    遍历 images/ 和 cube_results/ 下的所有子目录，
    删除创建时间超过 max_age_hours 的目录。

    Args:
        max_age_hours: 最大保留时间（小时），默认 24

    Returns:
        int: 清理的目录数量
    """
    max_age_seconds = max_age_hours * 3600
    current_time = time.time()
    count = 0

    for root_dir in [IMAGES_ROOT, RESULTS_ROOT]:
        if not os.path.exists(root_dir):
            continue

        for entry in os.listdir(root_dir):
            entry_path = os.path.join(root_dir, entry)
            if not os.path.isdir(entry_path):
                continue

            dir_mtime = os.path.getmtime(entry_path)
            if current_time - dir_mtime > max_age_seconds:
                shutil.rmtree(entry_path)
                count += 1

    _sessions.clear()

    return count


def has_session(session_id: str) -> bool:
    """检查会话是否存在。

    Args:
        session_id: 会话唯一标识

    Returns:
        bool: 会话是否存在
    """
    return session_id in _sessions or os.path.exists(
        os.path.join(IMAGES_ROOT, session_id)
    )