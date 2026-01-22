import torch
print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 是否可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"当前显卡: {torch.cuda.get_device_name(0)}")
else:
    print("❌ 警告：未检测到 GPU，将使用 CPU 训练（速度会慢）")