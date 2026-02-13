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

# 将mock模块插入sys.modules
for module_name, mock_obj in mock_modules.items():
    if module_name not in sys.modules:
        sys.modules[module_name] = mock_obj

# 现在安全地导入app
from app import app

client = TestClient(app)

def test_root_endpoint():
    """测试根端点返回服务信息"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "CubeMaster API"
    assert data["version"] == "1.0.0"
    assert "/docs" in data["docs"]
    assert "/api/health" in data["health_check"]

def test_health_check():
    """测试健康检查端点"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "python_version" in data
    assert "model_loaded" in data
    assert data["status"] in ["healthy", "unhealthy"]
    
def test_solve_endpoint():
    """测试求解端点（需要已有保存的状态）"""
    response = client.post("/api/solve")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    # 由于没有预先保存状态，可能返回错误
    # 但确保端点响应正常

def test_recognize_endpoint_invalid():
    """测试识别端点无效请求"""
    response = client.post("/api/recognize", json={})
    assert response.status_code == 200  # FastAPI返回200即使出错
    data = response.json()
    assert "success" in data
    assert data["success"] == False

def test_performance_middleware():
    """测试性能监控中间件是否添加X-Process-Time头"""
    response = client.get("/")
    assert response.status_code == 200
    assert "X-Process-Time" in response.headers
    time_header = response.headers["X-Process-Time"]
    assert time_header.endswith("s")
    # 确保时间格式正确
    try:
        time_value = float(time_header[:-1])
        assert time_value >= 0.0
    except ValueError:
        assert False, f"Invalid time format: {time_header}"