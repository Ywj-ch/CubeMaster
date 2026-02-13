"""
pytest配置文件 - CubeMaster后端测试

此文件确保测试运行时正确的Python路径配置，
无论从项目根目录还是backend目录运行测试都能正常工作。
"""

import sys
from pathlib import Path

# 将backend目录添加到Python路径
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# 可选：打印调试信息（生产环境建议注释掉）
# def pytest_configure(config):
#     """pytest配置钩子，可添加测试配置"""
#     print(f"[pytest] Python路径已配置，backend目录: {backend_dir}")
#     print(f"[pytest] sys.path第一个元素: {sys.path[0] if sys.path else 'None'}")