import sys
import time
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from cube_service import solve_cube
from cube_service import save_cube_state
from cube_service import recognize_cube

# 创建FastAPI应用实例
app = FastAPI(
    title="魔方求解API服务",
    description="提供魔方状态识别和求解功能的后端接口",
    version="1.0.0"
)

# 配置跨域资源共享（CORS）
# 允许所有来源访问，适用于开发和测试环境
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源（生产环境应限制具体域名）
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)

# 性能监控中间件 - 记录请求处理时间
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    # 可选：在控制台输出日志（生产环境应使用结构化日志）
    if process_time > 1.0:  # 慢请求警告
        print(f"[PERF] Slow request: {request.method} {request.url.path} took {process_time:.4f}s")
    return response


# 调用求解魔方接口，并返回求解步骤
@app.post("/api/solve")
def solve():
    try:
        return {"success": True, "data": solve_cube()}
    except Exception as e:
        return {"success": False, "error": str(e)}


# 接收魔方图片数据，识别魔方状态并返回
@app.post("/api/recognize")
def recognize_cube_images(payload: dict = Body(...)):
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


# 保存魔方状态到服务器.json文件
@app.post("/api/save_state")
def save_state(payload: dict = Body(...)):
    try:
        save_cube_state(payload)
        return {"success": True, "message": "状态已保存"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# API根端点 - 返回服务信息
@app.get("/")
def root():
    return {
        "service": "CubeMaster API",
        "version": "1.0.0",
        "docs": "/docs",
        "health_check": "/api/health"
    }


# 健康检查端点
@app.get("/api/health")
def health_check():
    try:
        # 尝试检查模型加载状态
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
            "fastapi_version": "0.104.1",  # 当前使用的FastAPI版本
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