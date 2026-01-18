import cv2 as cv
import numpy as np
import os
import json
from pyciede2000 import ciede2000


class CubeDetector:
    """魔方颜色识别器 (基于轮廓查找 + CIEDE2000色差匹配)"""

    def __init__(self):
        """初始化魔方识别器"""
        # 结果保存目录
        self.results_dir = 'cube_results'
        self.debug_dir = os.path.join(self.results_dir, 'debug_steps')
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.debug_dir, exist_ok=True)

        # 颜色定义
        self.color_names = ['white', 'yellow', 'red', 'orange', 'blue', 'green']

        # 中心块颜色 -> 面标识映射
        self.center_to_face = {
            'white': 'U', 'red': 'R', 'green': 'F',
            'yellow': 'D', 'orange': 'L', 'blue': 'B'
        }

        # 标准魔方颜色参考值 (BGR格式) - 建议根据您的实际魔方微调
        self.bgr_refs = {
            'red': (0, 0, 200),  # 深红
            'orange': (0, 100, 255),  # 橙色
            'blue': (200, 0, 0),  # 蓝色
            'green': (0, 200, 0),  # 绿色
            'white': (220, 220, 220),  # 灰白 (避免过曝)
            'yellow': (0, 220, 220)  # 黄色
        }

    # ================= 工具函数 (移植自 functions.py) =================

    @staticmethod
    def get_dominant_colour(roi):
        """使用K-Means提取区域主色，抗反光干扰"""
        data = roi.reshape(-1, 3)
        data = np.float32(data)

        # 定义K-Means标准
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv.KMEANS_PP_CENTERS  # 使用更稳健的初始化

        # 聚类为1类
        try:
            _, labels, centers = cv.kmeans(data, 1, None, criteria, 10, flags)
            return centers[0].astype(np.uint8)  # 返回BGR
        except Exception:
            # 如果聚类失败，回退到平均值
            return np.mean(data, axis=0).astype(np.uint8)

    @staticmethod
    def convert_bgr_to_lab(bgr_colour):
        """
        手动将BGR转换为CIELab。
        OpenCV的cvtColor会将Lab缩放到0-255，而pyciede2000需要标准Lab值。
        来源: GitHub Reference / StackOverflow
        """
        # 归一化 BGR (0-1)
        b, g, r = bgr_colour / 255.0

        # sRGB -> Linear RGB
        rgb = [r, g, b]
        for i in range(3):
            if rgb[i] > 0.04045:
                rgb[i] = ((rgb[i] + 0.055) / 1.055) ** 2.4
            else:
                rgb[i] = rgb[i] / 12.92

        X = rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805
        Y = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
        Z = rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505

        # Normalize for D65 white point
        X = X / 0.95047
        Y = Y / 1.00000
        Z = Z / 1.08883

        # XYZ -> Lab
        xyz = [X, Y, Z]
        for i in range(3):
            if xyz[i] > 0.008856:
                xyz[i] = xyz[i] ** (1 / 3)
            else:
                xyz[i] = (7.787 * xyz[i]) + (16 / 116)

        L = (116 * xyz[1]) - 16
        a = 500 * (xyz[0] - xyz[1])
        b = 200 * (xyz[1] - xyz[2])

        return (L, a, b)

    def identify_color_ciede2000(self, bgr_sample):
        """使用CIEDE2000算法计算色差并匹配"""
        lab_sample = self.convert_bgr_to_lab(bgr_sample)

        min_delta = float('inf')
        best_match = 'unknown'

        for name, bgr_ref in self.bgr_refs.items():
            lab_ref = self.convert_bgr_to_lab(np.array(bgr_ref))

            # 计算色差
            delta_e = ciede2000(lab_sample, lab_ref)['delta_E_00']

            if delta_e < min_delta:
                min_delta = delta_e
                best_match = name

        # 阈值判定：如果色差太大，说明不是魔方颜色
        # 参考代码中阈值设为80，这是一个相对宽松的值
        if min_delta < 60:
            return best_match, min_delta
        else:
            return 'unknown', min_delta

    # ================= 核心检测逻辑 =================

    def detect_face_colors(self, image_path):
        """智能贴纸检测流程"""
        img = cv.imread(image_path)
        if img is None:
            print(f"❌ 无法读取: {image_path}")
            return None, None

        face_prefix = os.path.basename(image_path).split('.')[0]
        debug_img = img.copy()

        # 1. 预处理 (降噪 -> 灰度 -> 模糊 -> 边缘 -> 膨胀)
        # 降噪非常关键，去除颗粒感
        try:
            denoised = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        except:
            denoised = cv.GaussianBlur(img, (5, 5), 0)  # 如果太慢可用高斯代替

        gray = cv.cvtColor(denoised, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (5, 5), 0)

        # 宽松的Canny阈值，确保能抓到轮廓
        edges = cv.Canny(blurred, 20, 80)

        # 膨胀：连接断裂的边缘
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
        dilated = cv.dilate(edges, kernel)

        cv.imwrite(os.path.join(self.debug_dir, f'{face_prefix}_1_dilated.jpg'), dilated)

        # 2. 查找所有轮廓
        contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        valid_stickers = []  # 存储结构: {'x':, 'y':, 'color':, 'contour':}

        img_area = img.shape[0] * img.shape[1]

        for cnt in contours:
            # 2.1 形状初筛
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.05 * peri, True)  # 0.05系数允许圆角

            # 放宽到 4-6 个顶点，兼容圆角贴纸
            if 4 <= len(approx) <= 6:
                x, y, w, h = cv.boundingRect(approx)
                ratio = float(w) / h
                area = cv.contourArea(cnt)

                # 尺寸筛选: 接近正方形，且面积适中 (占全图 0.5% - 10%)
                if 0.7 < ratio < 1.4 and (img_area * 0.005 < area < img_area * 0.15):

                    # 2.2 颜色确认 (关键步骤)
                    # 提取该区域主色
                    roi_color = img[y:y + h, x:x + w]
                    dominant_bgr = self.get_dominant_colour(roi_color)

                    # 立即进行颜色匹配
                    color_name, delta = self.identify_color_ciede2000(dominant_bgr)

                    # 只有颜色匹配成功的才认为是贴纸
                    if color_name != 'unknown':
                        valid_stickers.append({
                            'x': x, 'y': y, 'w': w, 'h': h,
                            'color': color_name,
                            'bgr': dominant_bgr,
                            'cnt': approx
                        })
                        # 调试：画出候选框
                        cv.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv.putText(debug_img, f"{color_name}", (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # 3. 结果组装
        detected_matrix = []

        if len(valid_stickers) == 9:
            print(f"✅ {face_prefix}: 成功定位9个贴纸")

            # 排序逻辑：将散乱的贴纸映射到 3x3 矩阵
            # 1. 先按 Y 轴排序 (分出上中下三行)
            valid_stickers.sort(key=lambda s: s['y'])

            rows = [
                valid_stickers[0:3],  # Top row
                valid_stickers[3:6],  # Middle row
                valid_stickers[6:9]  # Bottom row
            ]

            # 2. 对每一行按 X 轴排序 (分出左中右)
            final_sorted = []
            for row in rows:
                row.sort(key=lambda s: s['x'])

                # 提取颜色名称构建矩阵
                matrix_row = [s['color'] for s in row]
                detected_matrix.append(matrix_row)
                final_sorted.extend(row)

            # 重新绘制带序号的调试图
            for idx, s in enumerate(final_sorted):
                cx, cy = s['x'] + s['w'] // 2, s['y'] + s['h'] // 2
                cv.putText(debug_img, str(idx), (cx, cy), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        else:
            print(f"⚠️ {face_prefix}: 找到 {len(valid_stickers)} 个有效贴纸 (需要9个)")
            # =================== 降级策略 (Fallback) ===================
            # 如果没找到9个，说明光线太差或者检测失败。
            # 此时回退到“中心网格强行采样” (Blind Grid Sampling)
            print(f"   >>> 启用降级策略: 中心强制采样")
            detected_matrix = self.fallback_grid_detection(img, debug_img)

        # 保存最终调试图
        cv.imwrite(os.path.join(self.debug_dir, f'{face_prefix}_result.jpg'), debug_img)
        return detected_matrix, debug_img

    def fallback_grid_detection(self, img, debug_img):
        """当智能检测失败时，强制在图像中心切9个格子进行识别"""
        h, w = img.shape[:2]
        # 假设魔方在正中心，占 60% 宽度
        cube_size = int(min(h, w) * 0.6)
        start_x = (w - cube_size) // 2
        start_y = (h - cube_size) // 2
        cell_size = cube_size // 3

        matrix = []
        for i in range(3):
            row_colors = []
            for j in range(3):
                cx = start_x + j * cell_size + cell_size // 2
                cy = start_y + i * cell_size + cell_size // 2

                # 采样中心 20x20 区域
                sample = img[cy - 10:cy + 10, cx - 10:cx + 10]
                dom_bgr = self.get_dominant_colour(sample)
                color_name, _ = self.identify_color_ciede2000(dom_bgr)

                # 降级模式下如果不确定，尽量猜一个最近的，不要返回unknown
                if color_name == 'unknown':
                    color_name = self.force_closest_color(dom_bgr)

                row_colors.append(color_name)

                # 画出强制网格
                cv.rectangle(debug_img, (cx - 15, cy - 15), (cx + 15, cy + 15), (0, 0, 255), 2)
                cv.putText(debug_img, color_name[:1], (cx, cy), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            matrix.append(row_colors)

        return matrix

    def force_closest_color(self, bgr_sample):
        """强制匹配一个最近的颜色 (用于降级模式)"""
        lab_sample = self.convert_bgr_to_lab(bgr_sample)
        min_delta = float('inf')
        best = 'white'  # 默认
        for name, ref in self.bgr_refs.items():
            lab_ref = self.convert_bgr_to_lab(np.array(ref))
            d = ciede2000(lab_sample, lab_ref)['delta_E_00']
            if d < min_delta:
                min_delta = d
                best = name
        return best

    # ================= 流程控制 (保持原逻辑) =================

    def detect_all_faces(self):
        """处理所有图片"""
        images_dir = 'images'
        cube_state = {}
        print("=== 开始检测魔方六个面 (CIE-DE2000 Lab版) ===")

        for color_name in self.color_names:
            img_path = os.path.join(images_dir, f"{color_name}.png")
            if not os.path.exists(img_path):
                print(f"❌ 缺失: {img_path}")
                continue

            print(f"\n🎯 处理 {color_name}.png ...")
            face_colors, _ = self.detect_face_colors(img_path)

            if face_colors:
                face_id = self.center_to_face[color_name]
                cube_state[face_id] = face_colors
                print(f"   结果: {face_colors}")

        return cube_state

    @staticmethod
    def display_cube_state(cube_state):
        print("\n" + "=" * 30 + " 最终状态 " + "=" * 30)
        desc = {
            'U': '上(White)', 'R': '右(Red)', 'F': '前(Green)',
            'D': '下(Yellow)', 'L': '左(Orange)', 'B': '后(Blue)'
        }
        for face in ['U', 'R', 'F', 'D', 'L', 'B']:
            if face in cube_state:
                print(f"[{desc[face]}]:")
                for row in cube_state[face]:
                    print(f"  {row}")
            else:
                print(f"[{desc[face]}]: ❌ 未识别")

    def save_cube_state_json(self, cube_state, filename='cube_state.json'):
        path = os.path.join(self.results_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cube_state, f, indent=2)
        print(f"✅ JSON已保存: {path}")


def main():
    detector = CubeDetector()
    state = detector.detect_all_faces()
    if len(state) == 6:
        detector.display_cube_state(state)
        detector.save_cube_state_json(state)
    else:
        print("\n⚠️ 警告: 未能完整识别6个面，仅显示结果，不保存文件。")


if __name__ == "__main__":
    main()