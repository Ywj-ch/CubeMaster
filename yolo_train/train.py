from ultralytics import YOLO
import os


def train_model():
    # 1. 加载预训练模型 (Nano版本，最快)
    # 第一次运行会自动下载 yolov8n.pt，不用担心
    model = YOLO('yolov8n.pt')

    # 2. 获取 data.yaml 的绝对路径 (防止路径错误)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, 'datasets', 'data.yaml')

    print(f"🚀 开始训练！配置文件路径: {yaml_path}")

    # 3. 开始训练
    # epochs=100: 训练 100 轮
    # imgsz=640: 图片大小
    # batch=16: 一次喂 16 张图 (显存不够可以改小，比如 8 或 4)
    # device=0: 使用第一块 GPU (RTX 3060)
    results = model.train(
        data=yaml_path,
        epochs=100,
        imgsz=640,
        batch=8,
        device=0,
        workers=0,
        name='cube_yolo_v1'  # 训练结果保存的文件夹名字
    )

    print("✅ 训练完成！")


if __name__ == '__main__':
    train_model()