"""
SessionManager 会话管理模块测试

测试会话的创建、目录隔离、销毁和过期清理功能
"""

import os
import time
import shutil
import tempfile
import pytest
from unittest.mock import patch

from session_manager import (
    get_session_dir,
    delete_session,
    cleanup_expired_sessions,
    has_session,
    IMAGES_ROOT,
    RESULTS_ROOT,
)


@pytest.fixture
def temp_dirs():
    """使用临时目录替代真实目录进行测试"""
    with tempfile.TemporaryDirectory() as tmp_root:
        images_dir = os.path.join(tmp_root, "images")
        results_dir = os.path.join(tmp_root, "cube_results")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)
        yield {
            "tmp_root": tmp_root,
            "images_dir": images_dir,
            "results_dir": results_dir,
        }


@pytest.fixture(autouse=True)
def cleanup_sessions():
    """每个测试后清理会话内存缓存"""
    yield
    from session_manager import _sessions
    _sessions.clear()


class TestGetSessionDir:
    """测试 get_session_dir 函数"""

    def test_creates_directories(self):
        """测试会话目录自动创建"""
        session_id = "test-create-dir"
        dirs = get_session_dir(session_id)

        assert os.path.isdir(dirs["images_dir"])
        assert os.path.isdir(dirs["results_dir"])

        os.rmdir(dirs["images_dir"])
        os.rmdir(dirs["results_dir"])

    def test_returns_correct_paths(self):
        """测试返回正确的路径结构"""
        session_id = "test-paths"
        dirs = get_session_dir(session_id)

        assert session_id in dirs["images_dir"]
        assert session_id in dirs["results_dir"]
        assert dirs["images_dir"].endswith(session_id)
        assert dirs["results_dir"].endswith(session_id)

    def test_same_session_returns_same_dirs(self):
        """测试相同 session_id 返回相同目录"""
        session_id = "test-same-session"
        dirs1 = get_session_dir(session_id)
        dirs2 = get_session_dir(session_id)

        assert dirs1["images_dir"] == dirs2["images_dir"]
        assert dirs1["results_dir"] == dirs2["results_dir"]

    def test_different_sessions_different_dirs(self):
        """测试不同 session_id 返回不同目录"""
        dirs1 = get_session_dir("session-a")
        dirs2 = get_session_dir("session-b")

        assert dirs1["images_dir"] != dirs2["images_dir"]
        assert dirs1["results_dir"] != dirs2["results_dir"]


class TestDeleteSession:
    """测试 delete_session 函数"""

    def test_delete_existing_session(self):
        """测试删除存在的会话"""
        session_id = "test-delete"
        dirs = get_session_dir(session_id)

        assert os.path.exists(dirs["images_dir"])
        assert os.path.exists(dirs["results_dir"])

        result = delete_session(session_id)

        assert result is True
        assert not os.path.exists(dirs["images_dir"])
        assert not os.path.exists(dirs["results_dir"])

    def test_delete_nonexistent_session(self):
        """测试删除不存在的会话"""
        result = delete_session("nonexistent-session")

        assert result is False

    def test_delete_session_removes_from_memory(self):
        """测试删除会话后从内存缓存移除"""
        session_id = "test-mem-remove"
        get_session_dir(session_id)

        assert has_session(session_id) is True

        delete_session(session_id)

        assert session_id not in _sessions_dict()


class TestCleanupExpiredSessions:
    """测试 cleanup_expired_sessions 函数"""

    def test_cleanup_old_sessions(self):
        """测试清理过期会话"""
        session_id = "test-old-session"
        dirs = get_session_dir(session_id)

        assert os.path.exists(dirs["images_dir"])

        count = cleanup_expired_sessions(max_age_hours=0)

        assert count >= 1
        assert not os.path.exists(dirs["images_dir"])

    def test_cleanup_preserves_recent_sessions(self):
        """测试不清理新创建的会话"""
        session_id = "test-recent-session"
        dirs = get_session_dir(session_id)

        count = cleanup_expired_sessions(max_age_hours=24)

        assert count == 0
        assert os.path.exists(dirs["images_dir"])


class TestHasSession:
    """测试 has_session 函数"""

    def test_has_existing_session(self):
        """测试检查存在的会话"""
        session_id = "test-has"
        get_session_dir(session_id)

        assert has_session(session_id) is True

    def test_has_nonexistent_session(self):
        """测试检查不存在的会话"""
        assert has_session("nonexistent") is False


def _sessions_dict():
    """辅助函数：获取当前会话字典"""
    from session_manager import _sessions
    return _sessions