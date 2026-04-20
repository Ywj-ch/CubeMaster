import sys
from unittest.mock import Mock, MagicMock
from fastapi.testclient import TestClient

# Mock昂贵的依赖模块以避免测试时初始化
mock_modules = {
    'twophase.solver': MagicMock(),
    'ultralytics': MagicMock(),
    'ultralytics.YOLO': MagicMock(),
    'cube_image_detection': MagicMock(),
}

for module_name, mock_obj in mock_modules.items():
    if module_name not in sys.modules:
        sys.modules[module_name] = mock_obj

from app import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "CubeMaster API"
    assert "version" in data
    assert "/docs" in data["docs"]
    assert "/api/health" in data["health_check"]


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "python_version" in data
    assert "model_loaded" in data
    assert data["status"] in ["healthy", "unhealthy"]


def test_create_session():
    """测试创建会话端点"""
    response = client.post("/api/session")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "session_id" in data
    assert len(data["session_id"]) > 0


def test_close_session():
    """测试销毁会话端点"""
    create_resp = client.post("/api/session")
    session_id = create_resp.json()["session_id"]

    close_resp = client.delete(f"/api/session/{session_id}")
    assert close_resp.status_code == 200
    data = close_resp.json()
    assert data["success"] is True


def test_close_nonexistent_session():
    """测试销毁不存在的会话"""
    response = client.delete("/api/session/nonexistent-id")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_solve_endpoint():
    """测试求解端点（需要已有保存的状态）"""
    response = client.post("/api/solve", json={})
    assert response.status_code == 200
    data = response.json()
    assert "success" in data


def test_solve_endpoint_with_session():
    """测试带 session_id 的求解端点"""
    create_resp = client.post("/api/session")
    session_id = create_resp.json()["session_id"]

    response = client.post("/api/solve", json={"session_id": session_id})
    assert response.status_code == 200
    data = response.json()
    assert "success" in data


def test_recognize_endpoint_invalid():
    """测试识别端点无效请求"""
    response = client.post("/api/recognize", json={})
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is False


def test_recognize_endpoint_with_session():
    """测试带 session_id 的识别端点"""
    create_resp = client.post("/api/session")
    session_id = create_resp.json()["session_id"]

    response = client.post("/api/recognize", json={
        "images": {},
        "session_id": session_id,
    })
    assert response.status_code == 200
    data = response.json()
    assert "success" in data


def test_save_state_with_session():
    """测试带 session_id 的保存状态端点"""
    create_resp = client.post("/api/session")
    session_id = create_resp.json()["session_id"]

    response = client.post("/api/save_state", json={
        "faces": {"U": ["white"] * 9},
        "session_id": session_id,
    })
    assert response.status_code == 200
    data = response.json()
    assert "success" in data


def test_performance_middleware():
    """测试性能监控中间件是否添加X-Process-Time头"""
    response = client.get("/")
    assert response.status_code == 200
    assert "X-Process-Time" in response.headers
    time_header = response.headers["X-Process-Time"]
    assert time_header.endswith("s")
    try:
        time_value = float(time_header[:-1])
        assert time_value >= 0.0
    except ValueError:
        assert False, f"Invalid time format: {time_header}"