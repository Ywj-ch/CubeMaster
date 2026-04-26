"""
CubeMaster FastAPI 后端应用

提供魔方求解和识别的 RESTful API 服务。

主要功能:
- 魔方状态识别 (YOLOv8)
- Kociemba 二阶段求解算法
- 状态持久化存储
- 基于会话的文件隔离，支持多用户并发访问

API 文档: /docs
健康检查: /api/health
"""

import sys
import uuid
import time
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from cube_service import solve_cube
from cube_service import save_cube_state
from cube_service import recognize_cube
from session_manager import (
    get_session_dir,
    delete_session,
    cleanup_expired_sessions,
    has_session,
)

app = FastAPI(
    title="魔方求解API服务",
    description="提供魔方状态识别和求解功能的后端接口",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_cleanup():
    """服务启动时清理过期会话目录"""
    count = cleanup_expired_sessions()
    if count > 0:
        print(f"🧹 启动清理：删除了 {count} 个过期会话目录")


@app.middleware("http")
async def add_process_time_header(request, call_next):
    """性能监控中间件，记录请求处理时间并添加到响应头。"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    if process_time > 1.0:
        print(f"[PERF] Slow request: {request.method} {request.url.path} took {process_time:.4f}s")
    return response


@app.post("/api/session")
def create_session():
    """创建新的用户会话。

    生成唯一的 session_id，并创建对应的文件存储目录。
    同一用户多次访问应复用同一 session_id（由前端管理）。

    Returns:
        dict: 包含 session_id 和存储目录信息
    """
    session_id = str(uuid.uuid4())
    dirs = get_session_dir(session_id)
    return {
        "success": True,
        "session_id": session_id,
        "message": "会话创建成功"
    }


@app.delete("/api/session/{session_id}")
def close_session(session_id: str):
    """销毁指定会话，删除其所有文件。

    Args:
        session_id: 要销毁的会话 ID

    Returns:
        dict: 包含操作结果
    """
    if not has_session(session_id):
        return {"success": False, "error": "会话不存在"}

    removed = delete_session(session_id)
    if removed:
        return {"success": True, "message": "会话已销毁"}
    else:
        return {"success": False, "error": "会话销毁失败"}


@app.get("/api/session/{session_id}/load")
def load_session(session_id: str):
    """加载已保存的会话数据（魔方状态 + 求解结果）。

    直接读取 cube_results/{session_id}/ 下的 cube_state.json 和 solution.json，
    无需重新求解。用于回看历史会话。

    Args:
        session_id: 会话唯一标识

    Returns:
        dict: 包含 cube_state（六面颜色数组）和 solution（求解步骤）的字典
    """
    try:
        import os
        import json
        from session_manager import RESULTS_ROOT

        results_dir = os.path.join(RESULTS_ROOT, session_id)
        cube_path = os.path.join(results_dir, "cube_state.json")
        solution_path = os.path.join(results_dir, "solution.json")

        if not os.path.exists(cube_path):
            return {"success": False, "error": "会话不存在或无保存的状态数据"}

        with open(cube_path, "r", encoding="utf-8") as f:
            cube_state = json.load(f)

        result = {"cube_state": cube_state}

        if os.path.exists(solution_path):
            with open(solution_path, "r", encoding="utf-8") as f:
                solution = json.load(f)
            result["solution"] = {
                "readable_solution": solution.get("readable_solution", []),
                "moves": solution.get("moves", []),
                "step_count": solution.get("step_count", 0),
            }

        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/solve")
def solve(payload: dict = Body(...)):
    """求解魔方接口。

    读取之前保存的魔方状态，使用 Kociemba 二阶段算法计算最优解。

    Args:
        payload: 可选包含 session_id 的请求体，用于会话隔离

    Returns:
        dict: 包含 success 字段和 data(成功)或 error(失败)字段
    """
    try:
        session_id = payload.get("session_id") if payload else None
        return {"success": True, "data": solve_cube(session_id=session_id)}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/recognize")
def recognize_cube_images(payload: dict = Body(...)):
    """识别魔方状态接口。

    接收六面图片的 base64 数据，使用 YOLOv8 模型识别每面的颜色状态。

    Args:
        payload: 包含 images 字段和可选 session_id 字段的请求体

    Returns:
        dict: 包含 success 字段和 data(6面颜色数组)或 error 字段
    """
    try:
        session_id = payload.get("session_id")
        cube_state = recognize_cube(payload.get("images", {}), session_id=session_id)

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
        payload: 包含六面颜色数据和可选 session_id 的字典

    Returns:
        dict: 包含 success 字段和 message 字段
    """
    try:
        session_id = payload.get("session_id")
        state = {k: v for k, v in payload.items() if k != "session_id"}
        save_cube_state(state, session_id=session_id)
        return {"success": True, "message": "状态已保存"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/")
def root():
    """API 根端点。"""
    return {
        "service": "CubeMaster API",
        "version": "1.1.0",
        "docs": "/docs",
        "health_check": "/api/health"
    }


@app.get("/api/health")
def health_check():
    """健康检查端点。"""
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