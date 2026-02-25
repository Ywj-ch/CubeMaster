from ultralytics import YOLO
import os


def train_model():
    # 1. 加载预训练模型
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    model_path = os.path.join(project_root, 'runs', 'detect', 'cube_yolo_finetune_v1', 'weights', 'best.pt')
    model = YOLO(model_path)

    # 2. 获取 data.yaml 的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, 'datasets', 'data.yaml')

    print(f"🚀 开始训练！配置文件路径: {yaml_path}")

    # 3. 开始训练（添加光照增强参数）
    results = model.train(
        data=yaml_path,
        epochs=60,
        imgsz=640,
        batch=16,
        device=0,
        workers=4,
        name='cube_yolo_finetune_v2_lighting',
        # ===== 光照增强参数 =====
        hsv_v=0.6,
        hsv_s=0.7,
        hsv_h=0.015,
        degrees=5,
        translate=0.1,
        scale=0.3,
        mosaic=1.0,
        mixup=0.1,
    )

    print("✅ 训练完成！")


if __name__ == '__main__':
    train_model()