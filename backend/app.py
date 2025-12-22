from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 👇 直接 import 你的算法流水线
from convert_cube_state import solve_cube_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ping")
def ping():
    return {"msg": "backend is alive"}

@app.post("/api/solve")
def solve_cube():
    """
    正式方案：
    直接调用 Python 算法模块
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
