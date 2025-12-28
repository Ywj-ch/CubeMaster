from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from convert_cube_state import solve_cube_pipeline
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ping")
def ping():
    """
    测试接口
    """
    return {"msg": "backend is alive"}

@app.post("/api/solve")
def solve_cube():
    """
    调用魔方换元算法模块
    """
    try:
        result = solve_cube_pipeline()
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/cube_state")
def get_cube_state():
    """
    返回当前识别到的魔方六面状态（JSON）
    """
    try:
        json_path = "cube_results/cube_state.json"
        if not os.path.exists(json_path):
            return {
                "success": False,
                "error": "cube_state.json 不存在"
            }

        with open(json_path, "r", encoding="utf-8") as f:
            cube_state = json.load(f)

        return {
            "success": True,
            "data": cube_state
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }