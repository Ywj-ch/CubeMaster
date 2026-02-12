from cube_image_detection import CubeDetector
from image_utils import save_base64_images
from convert_cube_state import solve_cube_pipeline

# --- 引入单例模式变量 ---
# 在模块级别定义，程序运行期间只会存在一份
_detector_instance = None

def get_detector():
    """获取全局唯一的检测器实例 (Lazy Initialization)"""
    global _detector_instance
    if _detector_instance is None:
        print("[System] 初始化全局 YOLO 检测器单例...")
        _detector_instance = CubeDetector()
    return _detector_instance

def recognize_cube(images_data: dict):
    if not images_data:
        raise ValueError("未接收到图片数据")

    save_base64_images(images_data, output_dir='images')

    # 使用单例，避免重复加载模型到显存
    detector = get_detector()
    cube_state = detector.detect_all_faces()

    return cube_state


def save_cube_state(state: dict):
    if not state:
        raise ValueError("状态数据为空")

    # 复用同一个实例
    detector = get_detector()
    detector.save_cube_state_json(state)


def solve_cube():
    return solve_cube_pipeline()