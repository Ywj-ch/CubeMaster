from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from convert_cube_state import solve_cube_pipeline
import os
import json

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


@app.get("/api/ping")
def ping():
    """健康检查接口

    用于验证后端服务是否正常运行。

    Returns:
        dict: 包含服务状态信息的字典
    """
    return {"msg": "backend is alive"}


@app.post("/api/solve")
def solve_cube():
    """触发魔方求解流程的接口

    调用convert_cube_state模块中的求解管道，执行以下步骤：
    1. 解析cube_state.txt文件中的魔方状态
    2. 转换为Kociemba算法格式
    3. 验证状态有效性
    4. 调用Kociemba算法求解
    5. 保存求解结果到JSON文件

    Returns:
        dict: 包含求解结果或错误信息的响应字典
        - success: 布尔值，表示操作是否成功
        - data: 成功时返回的求解结果（包含状态编码、解法步骤等）
        - error: 失败时返回的错误描述

    Raises:
        无：所有异常都被捕获并转换为错误响应
    """
    try:
        # 调用求解管道，获取完整求解结果
        result = solve_cube_pipeline()

        # 成功响应
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        # 异常处理，返回错误信息
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/api/cube_state")
def get_cube_state():
    """获取已识别的魔方状态接口

    从cube_results目录读取cube_state.json文件，
    返回当前识别到的魔方六面状态。

    Returns:
        dict: 包含魔方状态或错误信息的响应字典
        - success: 布尔值，表示操作是否成功
        - data: 成功时返回的魔方状态JSON对象
        - error: 失败时返回的错误描述
    """
    try:
        # 魔方状态JSON文件路径
        json_path = "cube_results/cube_state.json"

        # 检查文件是否存在
        if not os.path.exists(json_path):
            return {
                "success": False,
                "error": "cube_state.json 不存在，请先运行魔方识别"
            }

        # 读取并解析JSON文件
        with open(json_path, "r", encoding="utf-8") as f:
            cube_state = json.load(f)

        # 成功响应
        return {
            "success": True,
            "data": cube_state
        }

    except json.JSONDecodeError as e:
        # JSON解析错误
        return {
            "success": False,
            "error": f"JSON解析错误: {str(e)}"
        }
    except Exception as e:
        # 其他异常
        return {
            "success": False,
            "error": str(e)
        }

