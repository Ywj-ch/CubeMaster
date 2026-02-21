"""
CubeMaster FastAPI 后端应用

提供魔方求解和识别的 RESTful API 服务。

主要功能:
- 魔方状态识别 (YOLOv8)
- Kociemba 二阶段求解算法
- 状态持久化存储

API 文档: /docs
健康检查: /api/health
"""

import sys
import time
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from cube_service import solve_cube
from cube_service import save_cube_state
from cube_service import recognize_cube

app = FastAPI(
    title="魔方求解API服务",
    description="提供魔方状态识别和求解功能的后端接口",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request, call_next):
    """性能监控中间件，记录请求处理时间并添加到响应头。
    
    Args:
        request: FastAPI 请求对象
        call_next: 下一个中间件或路由处理函数
        
    Returns:
        Response: 带有 X-Process-Time 头的响应
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    if process_time > 1.0:
        print(f"[PERF] Slow request: {request.method} {request.url.path} took {process_time:.4f}s")
    return response


@app.post("/api/solve")
def solve():
    """求解魔方接口。
    
    读取之前保存的魔方状态，使用 Kociemba 二阶段算法计算最优解。
    
    Returns:
        dict: 包含 success 字段和 data(成功)或 error(失败)字段
    """
    try:
        return {"success": True, "data": solve_cube()}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/recognize")
def recognize_cube_images(payload: dict = Body(...)):
    """识别魔方状态接口。
    
    接收六面图片的 base64 数据，使用 YOLOv8 模型识别每面颜色状态。
    
    Args:
        payload: 包含 images 字段的请求体，images 为面名到 base64 图片的映射
        
    Returns:
        dict: 包含 success 字段和 data(6面颜色数组)或 error 字段
    """
    try:
        cube_state = recognize_cube(payload.get("images", {}))

        if len(cube_state) == 6:
            return {"success": True, "data": cube_state}
        else:
            return {
                "success": False,
                "data": cube_state,
                "error": f"识别不完整 ({len(cube_state)}/6)"
            }

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/save_state")
def save_state(payload: dict = Body(...)):
    """保存魔方状态接口。
    
    将魔方状态保存到服务器 JSON 文件，供后续求解使用。
    
    Args:
        payload: 包含六面颜色数据的字典
        
    Returns:
        dict: 包含 success 字段和 message 字段
    """
    try:
        save_cube_state(payload)
        return {"success": True, "message": "状态已保存"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/")
def root():
    """API 根端点。
    
    返回服务基本信息和可用端点列表。
    
    Returns:
        dict: 服务名称、版本、文档地址等
    """
    return {
        "service": "CubeMaster API",
        "version": "1.0.0",
        "docs": "/docs",
        "health_check": "/api/health"
    }


@app.get("/api/health")
def health_check():
    """健康检查端点。
    
    检查服务运行状态和 YOLO 模型加载状态。
    
    Returns:
        dict: 包含 status、model_loaded、timestamp 等字段
    """
    try:
        model_loaded = False
        model_error = None
        
        try:
            from cube_service import get_detector
            detector = get_detector()
            model_loaded = detector.model is not None
        except ImportError as e:
            model_error = f"模型依赖未安装: {str(e)}"
        except Exception as e:
            model_error = f"模型加载失败: {str(e)}"
        
        return {
            "status": "healthy",
            "service": "CubeMaster API",
            "python_version": sys.version.split()[0],
            "fastapi_version": "0.104.1",
            "model_loaded": model_loaded,
            "model_error": model_error,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }