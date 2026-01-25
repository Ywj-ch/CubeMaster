from ultralytics import YOLO
import os


def train_model():
    # 1. 加载预训练模型
    current_dir = os.path.dirname(os.path.abspath(__file__)) # yolo_train 目录
    project_root = os.path.dirname(current_dir)              # CubeSolver 根目录
    model_path = os.path.join(project_root, 'runs', 'detect', 'cube_yolo_v1', 'weights', 'best.pt')
    model = YOLO(model_path)

    # 2. 获取 data.yaml 的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, 'datasets', 'data.yaml')

    print(f"🚀 开始训练！配置文件路径: {yaml_path}")

    # 3. 开始训练
    results = model.train(
        data=yaml_path,
        epochs=50,
        imgsz=640,
        batch=-1,
        device=0,
        workers=0,
        name='cube_yolo_finetune_v1'  # 训练结果保存的文件夹名字
    )

    print("✅ 训练完成！")


if __name__ == '__main__':
    train_model()