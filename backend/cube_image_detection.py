import cv2 as cv
import numpy as np
import os
import json


class CubeDetector:
    """魔方颜色识别器

    用于从六张魔方照片中识别每个面的9个色块颜色，并按标准魔方表示法输出结果。

    Attributes:
        results_dir: 结果保存目录
        color_names: 六个面的颜色名称
        center_to_face: 中心颜色到魔方面字母标识的映射
    """

    def __init__(self):
        """初始化魔方识别器"""
        # 创建结果文件夹
        self.results_dir = 'cube_results'
        os.makedirs(self.results_dir, exist_ok=True)

        # 定义魔方六个面的标准颜色（对应图片文件名）
        self.color_names = ['white', 'yellow', 'red', 'orange', 'blue', 'green']

        # 中心颜色到魔方面字母标识的映射（采用标准魔方表示法）
        self.center_to_face = {
            'white': 'U',  # 上面（UP）
            'red': 'R',  # 右面（RIGHT）
            'green': 'F',  # 前面（FRONT）
            'yellow': 'D',  # 下面（DOWN）
            'orange': 'L',  # 左面（LEFT）
            'blue': 'B'  # 后面（BACK）
        }


    # TODO：颜色识别算法当前存在不稳定性，后续可优化HSV阈值和采样策略
    @staticmethod
    def hsv_to_color(h, s, v):
        """根据HSV值判断对应的魔方颜色

        Args:
            h: 色相值（0-180）
            s: 饱和度值（0-255）
            v: 明度值（0-255）

        Returns:
            str: 识别出的颜色名称，或'unknown'表示无法识别
        """
        # 白色检测：低饱和度、高明度
        if s < 40 and v > 120:
            return 'white'

        # 黄色检测：色相在20-35之间，高饱和度
        if 20 <= h <= 35 and s > 100:
            return 'yellow'

        # 橙色检测：色相在5-18之间，高饱和度和明度
        if 5 < h <= 18 and s > 120 and v > 100:
            return 'orange'

        # 红色检测（HSV色相环两端）：色相<10或>170，高饱和度
        if (h < 10 or h > 170) and s > 100:
            return 'red'

        # 绿色检测：色相在35-85之间，高饱和度
        if 35 <= h < 85 and s > 100:
            return 'green'

        # 蓝色检测：色相在85-130之间，高饱和度
        if 85 <= h < 130 and s > 100:
            return 'blue'

        # 未识别的颜色
        return 'unknown'


    @staticmethod
    def detect_cube_face_roi(img):
        """定位魔方面区域并裁剪多余背景

        通过颜色饱和度检测找到魔方区域，返回裁剪后的魔方面图像。

        Args:
            img: 输入图像（BGR格式）

        Returns:
            numpy.ndarray: 裁剪后的魔方面图像，未检测到时返回None
        """
        # 转换到HSV颜色空间以便分离色度和饱和度
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)

        # 创建掩膜：高饱和度区域（排除灰暗背景）
        mask = (s > 60) & (v > 50)

        # 查找非零像素位置（即魔方区域）
        coords = cv.findNonZero(mask.astype('uint8'))
        if coords is None:
            return None

        # 获取魔方面的最小外接矩形并裁剪
        x, y, w, h = cv.boundingRect(coords)
        return img[y:y + h, x:x + w]


    @staticmethod
    def sample_cell_color(hsv, cx, cy, cell_size):
        """从魔方单个色块中采样颜色

        在每个色块的四个方向偏移位置采样，取平均值以提高鲁棒性。

        Args:
            hsv: 整个魔方面的HSV图像
            cx, cy: 色块中心坐标
            cell_size: 色块预估尺寸
        """
        # 四个采样点相对于中心的偏移量
        offsets = [
            (-cell_size // 4, 0),  # 左
            (cell_size // 4, 0),  # 右
            (0, -cell_size // 4),  # 上
            (0, cell_size // 4),  # 下
        ]

        samples = []

        for dx, dy in offsets:
            x = int(cx + dx)
            y = int(cy + dy)

            # 以采样点为中心取小区域
            half = cell_size // 8
            patch = hsv[y - half:y + half, x - half:x + half]

            if patch.size > 0:
                samples.append(np.mean(patch, axis=(0, 1)))

        # 返回四个采样点的平均HSV值
        return np.mean(samples, axis=0)


    def detect_face_colors(self, image_path):
        """检测单张魔方面图片的9个色块颜色

        主要流程：
        1. 读取图像并定位魔方面区域
        2. 预处理（调整大小、高斯模糊）
        3. 划分3x3网格并采样每个色块颜色
        4. 可视化标记并返回结果

        Args:
            image_path: 魔方面图片路径

        Returns:
            tuple: (3x3颜色矩阵, 标记后的可视化图像) 或失败时返回None
        """
        # 读取图像
        img = cv.imread(image_path)
        if img is None:
            print(f"❌ 无法读取图像: {image_path}")
            return None

        # 定位魔方面区域（去除背景）
        roi = self.detect_cube_face_roi(img)
        if roi is None:
            print("❌ 未检测到魔方面，使用原图")
            roi = img

        # 预处理：统一尺寸为400x400，高斯模糊降噪
        roi = cv.resize(roi, (400, 400))
        img_blur = cv.GaussianBlur(roi, (5, 5), 0)
        hsv = cv.cvtColor(img_blur, cv.COLOR_BGR2HSV)

        # 初始化3x3颜色矩阵
        detected_face = []
        cell_size = 120  # 预估每个色块大小
        margin = 20  # 魔方边缘留白

        for i in range(3):  # 行循环
            row_colors = []
            for j in range(3):  # 列循环
                # 计算当前色块中心坐标
                center_x = margin + j * cell_size + cell_size // 2
                center_y = margin + i * cell_size + cell_size // 2

                # 定义采样区域（30x30像素）
                sample_size = 30
                x1 = max(0, center_x - sample_size // 2)
                y1 = max(0, center_y - sample_size // 2)
                x2 = min(400, center_x + sample_size // 2)
                y2 = min(400, center_y + sample_size // 2)

                # 采样颜色
                sample_region = hsv[y1:y2, x1:x2]
                if sample_region.size == 0:
                    row_colors.append('unknown')
                    continue

                # 计算平均HSV值并识别颜色
                avg_hsv = self.sample_cell_color(hsv, center_x, center_y, cell_size)
                h, s, v = avg_hsv
                detected_color = self.hsv_to_color(h, s, v)
                row_colors.append(detected_color)

                # 在图像上标记识别结果
                cv.putText(roi, detected_color, (x1, y1 - 5),
                           cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                cv.rectangle(roi, (x1, y1), (x2, y2), (255, 255, 255), 1)

            detected_face.append(row_colors)

        return detected_face, roi


    def detect_all_faces(self):
        """批量处理六个面的魔方图片

        遍历images文件夹中的六张图片（按颜色命名），
        识别每张图片的3x3颜色矩阵并确定对应的魔方面。

        Returns:
            dict: 魔方状态字典，键为面标识（U/R/F/D/L/B），值为3x3颜色矩阵
        """
        images_dir = 'images'
        cube_state = {}

        print("=== 开始检测魔方六个面 ===")

        for color_name in self.color_names:
            # 构建图片路径（格式：颜色名.png）
            img_path = os.path.join(images_dir, f"{color_name}.png")

            if not os.path.exists(img_path):
                print(f"❌ 图像不存在: {img_path}")
                continue

            print(f"\n🎯 检测 {color_name}.png (中心块: {color_name})")

            # 检测当前面的颜色
            face_colors, marked_img = self.detect_face_colors(img_path)

            if face_colors:
                # 根据中心颜色确定面标识
                face_name = self.center_to_face[color_name]
                cube_state[face_name] = face_colors

                # 保存可视化结果
                result_path = os.path.join(self.results_dir, f'result_{face_name}_{color_name}.jpg')
                cv.imwrite(result_path, marked_img)
                print(f"✅ {face_name}面结果保存: {result_path}")
                print(f"   检测结果: {face_colors}")

        return cube_state


    @staticmethod
    def display_cube_state(cube_state):
        """格式化显示魔方六面状态

        以可读格式输出每个面的颜色矩阵和中文描述。

        Args:
            cube_state: 魔方状态字典
        """
        print("\n" + "=" * 60)
        print("                 魔方六面状态报告")
        print("=" * 60)

        # 面标识与中文描述映射
        face_descriptions = {
            'U': '上面 (UP - 白色中心)',
            'R': '右面 (RIGHT - 红色中心)',
            'F': '前面 (FRONT - 绿色中心)',
            'D': '下面 (DOWN - 黄色中心)',
            'L': '左面 (LEFT - 橙色中心)',
            'B': '后面 (BACK - 蓝色中心)'
        }

        # 按固定顺序显示六面
        for face_name in ['U', 'R', 'F', 'D', 'L', 'B']:
            if face_name in cube_state:
                colors = cube_state[face_name]
                print(f"\n{face_descriptions[face_name]}:")
                for i, row in enumerate(colors):
                    print(f"  行{i + 1}: {row}")
            else:
                print(f"\n❌ 缺少 {face_descriptions[face_name]} 的数据")

        print("\n" + "=" * 60)


    def save_cube_state(self, cube_state, filename='cube_state.txt'):
        """保存魔方状态到文本文件

        Args:
            cube_state: 魔方状态字典
            filename: 输出文件名（保存在results_dir目录）
        """
        filepath = os.path.join(self.results_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("魔方六面状态识别结果\n")
            f.write("=" * 50 + "\n\n")

            face_descriptions = {
                'U': '上面 (UP - 白色中心)',
                'R': '右面 (RIGHT - 红色中心)',
                'F': '前面 (FRONT - 绿色中心)',
                'D': '下面 (DOWN - 黄色中心)',
                'L': '左面 (LEFT - 橙色中心)',
                'B': '后面 (BACK - 蓝色中心)'
            }

            # 按标准顺序写入六个面
            for face_name in ['U', 'R', 'F', 'D', 'L', 'B']:
                if face_name in cube_state:
                    f.write(f"{face_descriptions[face_name]}:\n")
                    for row in cube_state[face_name]:
                        f.write(f"  {row}\n")
                    f.write("\n")

        print(f"✅ 魔方状态已保存到: {filename}")


    def save_cube_state_json(self, cube_state, filename='cube_state.json'):
        """保存魔方状态到JSON文件

        便于程序化读取和处理识别结果。

        Args:
            cube_state: 魔方状态字典
            filename: JSON文件名
        """
        filepath = os.path.join(self.results_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(cube_state, f, ensure_ascii=False, indent=2)
        print(f"✅ 魔方状态 JSON 已保存到: {filename}")


def main():
    """主函数：执行魔方六面识别完整流程

    流程步骤：
    1. 初始化识别器
    2. 识别六张图片
    3. 显示和保存结果
    """
    detector = CubeDetector()

    # 批量识别images目录下的六张魔方面图片
    cube_state = detector.detect_all_faces()

    # 检查是否成功识别六面
    if len(cube_state) == 6:
        # 显示识别结果
        detector.display_cube_state(cube_state)

        # 保存结果到文件
        detector.save_cube_state(cube_state)
        detector.save_cube_state_json(cube_state)

        print("🎉 魔方六面识别完成！")
        print("📁 每个面的标记图像已保存为 result_面名_中心颜色.jpg")
    else:
        print(f"❌ 识别不完整，只识别了 {len(cube_state)}/6 个面")
        # 部分识别时仍显示已有结果
        if cube_state:
            detector.display_cube_state(cube_state)


if __name__ == "__main__":
    """程序入口点"""
    main()