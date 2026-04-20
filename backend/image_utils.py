import base64
import os
import cv2
import numpy as np

# ================= 配置区 =================

# 前端面标识 -> 后端文件名
FACE_TO_FILENAME = {
    'U': 'white',    # 上
    'R': 'red',      # 右
    'F': 'green',    # 前
    'D': 'yellow',   # 下
    'L': 'orange',   # 左
    'B': 'blue'      # 后
}

# 图像最大尺寸（等比缩放）
MAX_IMAGE_SIZE = 640


# ================= 工具函数 =================

def _safe_base64_decode(base64_str: str) -> bytes | None:
    """
    安全解码 base64 字符串，自动处理 data:image/... 头
    """
    try:
        if ',' in base64_str:
            base64_str = base64_str.split(',', 1)[1]
        return base64.b64decode(base64_str, validate=True)
    except Exception:
        return None


def _resize_keep_ratio(img: np.ndarray, max_size: int) -> np.ndarray:
    """
    等比缩放图片，使最长边不超过 max_size
    """
    h, w = img.shape[:2]
    scale = max_size / max(h, w)

    if scale >= 1.0:
        return img  # 不需要放大

    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)


# ================= 主函数 =================

def save_base64_images(images_dict: dict, output_dir: str = 'images', session_id: str = None) -> dict:
    """
    接收前端 Base64 图片并保存为本地文件

    Args:
        images_dict: { 'U': 'base64...', 'F': 'base64...' }
        output_dir: 保存目录（当 session_id 存在时会被覆盖为会话目录）
        session_id: 会话唯一标识，用于会话隔离

    Returns:
        dict: { 'U': True, 'F': False } 表示各面是否保存成功
    """
    if session_id:
        from session_manager import get_session_dir
        dirs = get_session_dir(session_id)
        output_dir = dirs["images_dir"]

    os.makedirs(output_dir, exist_ok=True)
    print(f"📂 正在保存图片到 {output_dir} ...")

    save_results = {}

    for face_key, base64_str in images_dict.items():
        if face_key not in FACE_TO_FILENAME:
            continue

        filename = FACE_TO_FILENAME[face_key] + '.png'
        save_path = os.path.join(output_dir, filename)

        # ---------- Base64 解码 ----------
        img_bytes = _safe_base64_decode(base64_str)
        if img_bytes is None:
            print(f"  ❌ Base64 解码失败: {face_key}")
            save_results[face_key] = False
            continue

        # ---------- 转 OpenCV 图像 ----------
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            print(f"  ❌ 图像解析失败: {face_key}")
            save_results[face_key] = False
            continue

        # ---------- 尺寸控制 ----------
        img = _resize_keep_ratio(img, MAX_IMAGE_SIZE)

        # ---------- 保存 ----------
        try:
            cv2.imwrite(save_path, img)
            print(f"  ✅ 已保存: {face_key} -> {filename}")
            save_results[face_key] = True
        except Exception as e:
            print(f"  ❌ 保存失败 {face_key}: {e}")
            save_results[face_key] = False

    return save_results
