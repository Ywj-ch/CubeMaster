import cv2
import os


def capture_images():
    # --- 配置 ---
    # 保存路径
    save_dir = 'raw_images'
    # 摄像头索引 (通常 0 是内置摄像头，如果有外接可能是 1)
    camera_id = 0

    # --- 初始化 ---
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"📂 已创建文件夹: {save_dir}")

    cap = cv2.VideoCapture(camera_id)

    # 设置分辨率为 1280x720 (根据摄像头能力调整，越高越好)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("❌ 无法打开摄像头！请检查连接。")
        return

    print("=" * 40)
    print("📸 自动拍照脚本启动！")
    print("按 【空格键】 拍照")
    print("按 【Q】 键退出")
    print(f"图片将保存到: {os.path.abspath(save_dir)}")
    print("=" * 40)

    count = 0
    # 自动检测当前目录下已有的图片数量，防止覆盖
    existing_files = [f for f in os.listdir(save_dir) if f.endswith('.jpg')]
    if existing_files:
        # 找到最大的编号，从下一个开始
        # 假设文件名格式为 img_0.jpg, img_1.jpg
        try:
            nums = [int(f.split('_')[1].split('.')[0]) for f in existing_files]
            count = max(nums) + 1
        except:
            count = len(existing_files)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ 无法获取画面")
            break

        # 显示实时画面
        cv2.imshow('Capture Data (Space to Save, Q to Quit)', frame)

        key = cv2.waitKey(1) & 0xFF

        # 按空格键拍照
        if key == 32:
            filename = os.path.join(save_dir, f"webcam_{count}.jpg")
            cv2.imwrite(filename, frame)
            print(f"✅ 已保存: {filename}")
            count += 1

            # 视觉反馈：闪一下屏
            cv2.imshow('Capture Data (Space to Save, Q to Quit)', 255 - frame)
            cv2.waitKey(50)

            # 按 Q 键退出
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("👋 拍摄结束！")


if __name__ == "__main__":
    capture_images()