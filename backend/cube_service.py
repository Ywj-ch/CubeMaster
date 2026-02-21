"""
CubeMaster 业务服务层

提供魔方识别、状态保存和求解的高级业务逻辑封装。
使用单例模式管理 YOLO 检测器实例，避免重复加载模型。
"""

from cube_image_detection import CubeDetector
from image_utils import save_base64_images
from convert_cube_state import solve_cube_pipeline

_detector_instance = None


def get_detector():
    """获取全局唯一的 YOLO 检测器实例（延迟初始化）。
    
    使用单例模式确保整个应用生命周期内只有一个检测器实例，
    避免重复加载模型到显存。
    
    Returns:
        CubeDetector: YOLO 魔方检测器实例
    """
    global _detector_instance
    if _detector_instance is None:
        print("[System] 初始化全局 YOLO 检测器单例...")
        _detector_instance = CubeDetector()
    return _detector_instance


def recognize_cube(images_data: dict) -> list:
    """识别魔方状态。
    
    将六面图片保存到本地，然后使用 YOLO 模型识别每面的颜色状态。
    
    Args:
        images_data: 字典，键为面名（如 'U', 'D', 'F' 等），
                     值为对应面的 base64 编码图片数据
                    
    Returns:
        list: 6个元素的列表，每个元素是对应面的颜色状态数组
        
    Raises:
        ValueError: 如果 images_data 为空
    """
    if not images_data:
        raise ValueError("未接收到图片数据")

    save_base64_images(images_data, output_dir='images')

    detector = get_detector()
    cube_state = detector.detect_all_faces()

    return cube_state


def save_cube_state(state: dict) -> None:
    """保存魔方状态到 JSON 文件。
    
    将魔方状态持久化存储，供后续求解使用。
    
    Args:
        state: 包含六面颜色数据的字典
        
    Raises:
        ValueError: 如果 state 为空
    """
    if not state:
        raise ValueError("状态数据为空")

    detector = get_detector()
    detector.save_cube_state_json(state)


def solve_cube() -> dict:
    """求解魔方。
    
    读取之前保存的魔方状态，使用 Kociemba 二阶段算法计算最优解。
    
    Returns:
        dict: 包含 readable_solution（可读步数）和 moves（内部表示）的字典
    """
    return solve_cube_pipeline()