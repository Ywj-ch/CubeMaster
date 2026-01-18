import base64
import os
import cv2
import numpy as np


def save_base64_images(images_dict, output_dir='images'):
    """
    接收前端传来的图片字典，解码并保存为本地文件。

    Args:
        images_dict (dict): { 'F': 'base64str...', 'B': '...' }
        output_dir (str): 保存目录，默认为 'images'
    """
    # 确保目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 关键映射：前端发来的面(U/D...) -> 后端识别器需要的文件名(颜色.png)
    # 依据是你在 cube_image_detection.py 里的定义：
    # 'white': 'U', 'red': 'R', 'green': 'F', 'yellow': 'D', 'orange': 'L', 'blue': 'B'
    # 所以我们需要反向映射，把 U 面存为 white.png，这样检测器才能工作
    FACE_TO_FILENAME = {
        'U': 'white',  # 上面 -> 存为 white.png
        'R': 'red',  # 右面 -> 存为 red.png
        'F': 'green',  # 前面 -> 存为 green.png
        'D': 'yellow',  # 下面 -> 存为 yellow.png
        'L': 'orange',  # 左面 -> 存为 orange.png
        'B': 'blue'  # 后面 -> 存为 blue.png
    }

    print(f"📂 正在保存图片到 {output_dir}...")

    for face_key, base64_str in images_dict.items():
        if face_key not in FACE_TO_FILENAME:
            continue

        target_filename = f"{FACE_TO_FILENAME[face_key]}.png"
        save_path = os.path.join(output_dir, target_filename)

        try:
            # 1. 清理 Base64 头部 (data:image/jpeg;base64,...)
            if ',' in base64_str:
                base64_str = base64_str.split(',')[1]

            # 2. 解码
            img_bytes = base64.b64decode(base64_str)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # 3. 保存文件
            if img is not None:
                # 可以在这里做 resize，保证图片不用太大
                img = cv2.resize(img, (640, 640))
                cv2.imwrite(save_path, img)
                print(f"  ✅ 已保存: {face_key} -> {target_filename}")
            else:
                print(f"  ❌ 解码失败: {face_key}")

        except Exception as e:
            print(f"  ❌ 保存出错 {face_key}: {str(e)}")