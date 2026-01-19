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