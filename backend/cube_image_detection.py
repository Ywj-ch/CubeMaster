import cv2 as cv
import numpy as np
import os
import json
from pyciede2000 import ciede2000


class CubeDetector:
    """
    魔方颜色识别器
    基于：轮廓检测 + 主色提取 + CIEDE2000 色差匹配
    """

    # ================= 初始化 =================

    def __init__(self):
        # ---------- 目录 ----------
        self.results_dir = "cube_results"
        self.debug_dir = os.path.join(self.results_dir, "debug_steps")
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.debug_dir, exist_ok=True)

        # ---------- 颜色与面映射 ----------
        self.color_names = ["white", "yellow", "red", "orange", "blue", "green"]

        self.center_to_face = {
            "white": "U",
            "red": "R",
            "green": "F",
            "yellow": "D",
            "orange": "L",
            "blue": "B",
        }

        # ---------- BGR 参考色（可微调） ----------
        self.bgr_refs = {
            "red": (0, 0, 200),
            "orange": (0, 100, 255),
            "blue": (200, 0, 0),
            "green": (0, 200, 0),
            "white": (220, 220, 220),
            "yellow": (0, 220, 220),
        }

        # ---------- 预计算 Lab 参考色 ----------
        self.lab_refs = {
            name: self.convert_bgr_to_lab(np.array(bgr))
            for name, bgr in self.bgr_refs.items()
        }

        # ================= 可调参数区 =================
        self.CANNY_LOW = 20
        self.CANNY_HIGH = 80

        self.DILATE_KERNEL = 9

        self.MIN_AREA_RATIO = 0.005
        self.MAX_AREA_RATIO = 0.15

        self.SQUARE_RATIO_MIN = 0.7
        self.SQUARE_RATIO_MAX = 1.4

        self.DELTA_E_THRESHOLD = 60

    # ================= 工具函数 =================

    @staticmethod
    def get_dominant_colour(roi):
        """K-Means 提取主色，抗反光"""
        data = roi.reshape(-1, 3).astype(np.float32)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)

        try:
            _, _, centers = cv.kmeans(
                data, 1, None, criteria, 10, cv.KMEANS_PP_CENTERS
            )
            return centers[0].astype(np.uint8)
        except Exception:
            return np.mean(data, axis=0).astype(np.uint8)

    @staticmethod
    def convert_bgr_to_lab(bgr):
        """手动 BGR -> CIE Lab（标准 Lab 空间）"""
        b, g, r = bgr / 255.0
        rgb = [r, g, b]

        for i in range(3):
            if rgb[i] > 0.04045:
                rgb[i] = ((rgb[i] + 0.055) / 1.055) ** 2.4
            else:
                rgb[i] /= 12.92

        X = rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805
        Y = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
        Z = rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505

        X /= 0.95047
        Z /= 1.08883

        xyz = [X, Y, Z]
        for i in range(3):
            if xyz[i] > 0.008856:
                xyz[i] = xyz[i] ** (1 / 3)
            else:
                xyz[i] = 7.787 * xyz[i] + 16 / 116

        L = 116 * xyz[1] - 16
        a = 500 * (xyz[0] - xyz[1])
        b = 200 * (xyz[1] - xyz[2])

        return (L, a, b)

    # ================= 颜色匹配 =================

    def identify_color_ciede2000(self, bgr_sample):
        lab_sample = self.convert_bgr_to_lab(bgr_sample)

        min_delta = float("inf")
        best = "unknown"

        for name, lab_ref in self.lab_refs.items():
            d = ciede2000(lab_sample, lab_ref)["delta_E_00"]
            if d < min_delta:
                min_delta = d
                best = name

        if min_delta < self.DELTA_E_THRESHOLD:
            return best, min_delta
        return "unknown", min_delta

    # ================= 核心检测 =================

    def detect_face_colors(self, image_path):
        img = cv.imread(image_path)
        if img is None:
            return None, None

        face_name = os.path.splitext(os.path.basename(image_path))[0]
        debug_img = img.copy()
        img_area = img.shape[0] * img.shape[1]

        # ---------- 预处理 ----------
        try:
            denoised = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        except Exception:
            denoised = cv.GaussianBlur(img, (5, 5), 0)

        gray = cv.cvtColor(denoised, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (5, 5), 0)

        edges = cv.Canny(blurred, self.CANNY_LOW, self.CANNY_HIGH)
        kernel = cv.getStructuringElement(
            cv.MORPH_RECT, (self.DILATE_KERNEL, self.DILATE_KERNEL)
        )
        dilated = cv.dilate(edges, kernel)

        cv.imwrite(
            os.path.join(self.debug_dir, f"{face_name}_dilated.jpg"), dilated
        )

        # ---------- 轮廓 ----------
        contours, _ = cv.findContours(
            dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )

        stickers = []

        for cnt in contours:
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.05 * peri, True)

            if not (4 <= len(approx) <= 6):
                continue

            x, y, w, h = cv.boundingRect(approx)
            ratio = w / float(h)
            area = cv.contourArea(cnt)

            if not (self.SQUARE_RATIO_MIN < ratio < self.SQUARE_RATIO_MAX):
                continue
            if not (self.MIN_AREA_RATIO * img_area < area < self.MAX_AREA_RATIO * img_area):
                continue

            roi = img[y : y + h, x : x + w]
            dom_bgr = self.get_dominant_colour(roi)
            color, _ = self.identify_color_ciede2000(dom_bgr)

            if color == "unknown":
                continue

            stickers.append(
                {"x": x, "y": y, "w": w, "h": h, "color": color}
            )
            cv.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # ---------- 组装 ----------
        if len(stickers) == 9:
            stickers.sort(key=lambda s: s["y"])
            matrix = []

            for i in range(3):
                row = sorted(
                    stickers[i * 3 : (i + 1) * 3], key=lambda s: s["x"]
                )
                matrix.append([s["color"] for s in row])
        else:
            matrix = self.fallback_grid_detection(img, debug_img)

        cv.imwrite(
            os.path.join(self.debug_dir, f"{face_name}_result.jpg"), debug_img
        )
        return matrix, debug_img

    # ================= 降级策略 =================

    def fallback_grid_detection(self, img, debug_img):
        h, w = img.shape[:2]
        cube_size = int(min(h, w) * 0.6)
        sx = (w - cube_size) // 2
        sy = (h - cube_size) // 2
        cell = cube_size // 3

        matrix = []

        for i in range(3):
            row = []
            for j in range(3):
                cx = sx + j * cell + cell // 2
                cy = sy + i * cell + cell // 2
                sample = img[cy - 10 : cy + 10, cx - 10 : cx + 10]

                dom = self.get_dominant_colour(sample)
                color, _ = self.identify_color_ciede2000(dom)

                if color == "unknown":
                    color = self.force_closest_color(dom)

                row.append(color)
                cv.rectangle(
                    debug_img,
                    (cx - 15, cy - 15),
                    (cx + 15, cy + 15),
                    (0, 0, 255),
                    2,
                )
            matrix.append(row)

        return matrix

    def force_closest_color(self, bgr):
        lab = self.convert_bgr_to_lab(bgr)
        best, min_d = "white", float("inf")

        for name, lab_ref in self.lab_refs.items():
            d = ciede2000(lab, lab_ref)["delta_E_00"]
            if d < min_d:
                best, min_d = name, d

        return best

    # ================= 流程控制 =================

    def detect_all_faces(self):
        images_dir = "images"
        cube_state = {}

        for name in self.color_names:
            path = os.path.join(images_dir, f"{name}.png")
            if not os.path.exists(path):
                continue

            matrix, _ = self.detect_face_colors(path)
            if matrix:
                cube_state[self.center_to_face[name]] = matrix

        return cube_state

    def save_cube_state_json(self, cube_state, filename="cube_state.json"):
        path = os.path.join(self.results_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cube_state, f, indent=2)


def main():
    detector = CubeDetector()
    state = detector.detect_all_faces()

    if len(state) == 6:
        detector.save_cube_state_json(state)
    else:
        print("⚠️ 未完整识别 6 个面")


if __name__ == "__main__":
    main()
