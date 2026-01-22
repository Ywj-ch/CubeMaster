import cv2
import numpy as np
import os
import json
from ultralytics import YOLO


class CubeDetector:
    """
    魔方颜色识别器 (YOLOv8 智能填充版)
    """

    def __init__(self):
        # ---------- 目录 ----------
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.results_dir = os.path.join(base_dir, "cube_results")
        self.debug_dir = os.path.join(self.results_dir, "debug_steps")
        self.models_dir = os.path.join(base_dir, "models")

        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.debug_dir, exist_ok=True)

        # ---------- 加载 YOLO 模型 ----------
        model_path = os.path.join(self.models_dir, "best.pt")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"❌ 关键缺失：请将训练好的 best.pt 放入 {self.models_dir}")

        print(f"🚀 加载 YOLO 模型: {model_path}")
        self.model = YOLO(model_path)

        # ---------- 类别映射 ----------
        self.id_to_color = {
            0: 'blue', 1: 'green', 2: 'orange',
            3: 'red', 4: 'white', 5: 'yellow'
        }

        # ---------- 文件名映射 ----------
        self.filename_to_face = {
            "white": "U", "red": "R", "green": "F",
            "yellow": "D", "orange": "L", "blue": "B",
        }
        self.target_filenames = ["white", "yellow", "red", "orange", "blue", "green"]

    def detect_face_colors(self, image_path):
        """
        使用 YOLO 识别单张图片，返回 3x3 颜色矩阵 (支持部分识别)
        """
        img = cv2.imread(image_path)
        if img is None:
            print(f"❌ 无法读取图片: {image_path}")
            return [['black'] * 3 for _ in range(3)], None

        face_name = os.path.splitext(os.path.basename(image_path))[0]

        # 1. YOLO 推理 (开启半精度和尺寸限制，防止显存溢出)
        results = self.model.predict(
            img,
            conf=0.25,
            iou=0.6,
            agnostic_nms=True,
            verbose=False,
            imgsz=640,
            half=True
        )[0]

        stickers = []

        # 2. 解析结果
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            color = self.id_to_color.get(cls_id, 'unknown')
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

            stickers.append({
                'x': cx, 'y': cy, 'color': color, 'conf': conf,
                'box': (int(x1), int(y1), int(x2), int(y2))
            })

        # 3. 智能筛选 (Top 9)
        if len(stickers) > 9:
            print(f"⚠️ {face_name} 检测到 {len(stickers)} 个框，选取 Top 9")
            stickers.sort(key=lambda s: s['conf'], reverse=True)
            stickers = stickers[:9]

        # 4. 智能网格填充 (核心修改)
        # 即使数量 != 9，也尝试把现有的填进去
        matrix = self._smart_grid_fill(stickers)

        # 5. 保存调试图
        debug_img = self._draw_debug_boxes(img, stickers)
        # 如果数量不对，标记为 fail 图，方便查看，但不影响程序运行
        suffix = "_partial" if len(stickers) != 9 else "_ok"
        cv2.imwrite(os.path.join(self.debug_dir, f"{face_name}{suffix}.jpg"), debug_img)

        if len(stickers) != 9:
            print(f"⚠️ {face_name} 面仅识别 {len(stickers)}/9 个，已自动填充灰色")

        return matrix, debug_img

    @staticmethod
    def _smart_grid_fill(stickers):
        """
        智能网格映射算法：
        根据检测到的所有点的边界，划分 3x3 区域，将点落入对应的格子。
        """
        # 初始化全灰矩阵
        matrix = [['black'] * 3 for _ in range(3)]

        if not stickers:
            return matrix

        # 1. 计算所有点的边界范围
        xs = [s['x'] for s in stickers]
        ys = [s['y'] for s in stickers]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # 2. 计算每个格子的理论宽高
        # 加一点点 buffer 防止除以 0
        width = (max_x - min_x) + 1
        height = (max_y - min_y) + 1

        # 3. 映射每个点到 (row, col)
        for s in stickers:
            # 计算相对位置 (0.0 ~ 1.0)
            rel_x = (s['x'] - min_x) / width
            rel_y = (s['y'] - min_y) / height

            # 映射到 0, 1, 2
            # 理想情况下：0-0.33 -> 0, 0.33-0.66 -> 1, 0.66-1.0 -> 2
            col = int(rel_x * 3)
            row = int(rel_y * 3)

            # 边界保护 (防止算出来是 3)
            col = min(max(col, 0), 2)
            row = min(max(row, 0), 2)

            matrix[row][col] = s['color']

        return matrix

    @staticmethod
    def _draw_debug_boxes(img, stickers):
        debug_img = img.copy()
        for s in stickers:
            x1, y1, x2, y2 = s['box']
            color = s['color']
            cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(debug_img, color, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        return debug_img

    def detect_all_faces(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(base_dir, "images")

        # 默认全黑色
        default_matrix = [['black'] * 3 for _ in range(3)]
        cube_state = {code: default_matrix for code in self.filename_to_face.values()}

        print("🔍 开始 YOLO 识别流程...")

        for filename in self.target_filenames:
            path = os.path.join(images_dir, f"{filename}.png")
            face_code = self.filename_to_face[filename]

            if not os.path.exists(path):
                print(f"⚠️ 文件缺失: {path}")
                continue

            # 这里 matrix 肯定有值（最差也是全灰）
            matrix, _ = self.detect_face_colors(path)
            cube_state[face_code] = matrix
            print(f"✅ {filename} -> {face_code} 处理完毕")

        return cube_state

    def save_cube_state_json(self, cube_state, filename="cube_state.json"):
        path = os.path.join(self.results_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cube_state, f, indent=2)


if __name__ == "__main__":
    detector = CubeDetector()
    try:
        state = detector.detect_all_faces()
        detector.save_cube_state_json(state)
        print("🎉 流程结束，结果已保存！")
    except Exception as e:
        print(f"❌ 发生错误: {e}")