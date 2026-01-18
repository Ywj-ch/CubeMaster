from cube_image_detection import CubeDetector
from image_utils import save_base64_images
from convert_cube_state import solve_cube_pipeline
import os
import json


def recognize_cube(images_data: dict):
    if not images_data:
        raise ValueError("未接收到图片数据")

    save_base64_images(images_data, output_dir='images')

    detector = CubeDetector()
    cube_state = detector.detect_all_faces()

    return cube_state


def get_saved_cube_state():
    json_path = "cube_results/cube_state.json"
    if not os.path.exists(json_path):
        raise FileNotFoundError("cube_state.json 不存在")

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cube_state(state: dict):
    if not state:
        raise ValueError("状态数据为空")

    detector = CubeDetector()
    detector.save_cube_state_json(state)


def solve_cube():
    return solve_cube_pipeline()
