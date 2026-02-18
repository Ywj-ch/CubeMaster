#!/usr/bin/env python3
"""
纹理图片优化脚本
将纹理图片压缩到适合WebGL的尺寸 (512x512)，优化加载性能
"""

import os
import sys
import subprocess
import tempfile

def check_pillow():
    """检查Pillow库是否可用"""
    try:
        from PIL import Image
        return True
    except ImportError:
        return False

def install_pillow():
    """安装Pillow库"""
    print("正在安装Pillow库...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        print("Pillow安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装Pillow失败: {e}")
        return False

def get_image_dimensions(image_path):
    """获取图片尺寸（不依赖Pillow）"""
    try:
        # 尝试使用PIL
        from PIL import Image
        with Image.open(image_path) as img:
            return img.size
    except:
        # 尝试使用文件头解析
        try:
            with open(image_path, 'rb') as f:
                data = f.read(24)
                if data.startswith(b'\xff\xd8'):  # JPEG
                    # 简单的JPEG尺寸解析
                    f.seek(0)
                    while True:
                        marker = f.read(2)
                        if len(marker) < 2 or marker[0] != 0xff:
                            break
                        if marker[1] == 0xd9 or marker[1] == 0xda:
                            break
                        length = int.from_bytes(f.read(2), 'big')
                        if marker[1] == 0xc0 or marker[1] == 0xc2:  # SOF0/SOF2
                            f.read(1)  # precision
                            height = int.from_bytes(f.read(2), 'big')
                            width = int.from_bytes(f.read(2), 'big')
                            return width, height
                        f.seek(length - 2, 1)
                elif data.startswith(b'\x89PNG'):  # PNG
                    # PNG尺寸在16-24字节
                    width = int.from_bytes(data[16:20], 'big')
                    height = int.from_bytes(data[20:24], 'big')
                    return width, height
        except:
            pass
    return None

def optimize_texture(input_path, output_path, max_size=512, quality=80):
    """优化单张纹理图片"""
    try:
        from PIL import Image
        
        # 打开图片
        with Image.open(input_path) as img:
            original_size = img.size
            original_format = img.format
            
            print(f"处理: {os.path.basename(input_path)}")
            print(f"  原始尺寸: {original_size[0]}x{original_size[1]}")
            
            # 计算新尺寸（保持宽高比）
            ratio = min(max_size / original_size[0], max_size / original_size[1])
            new_width = int(original_size[0] * ratio)
            new_height = int(original_size[1] * ratio)
            
            # 确保尺寸是2的幂（WebGL友好）
            def next_power_of_two(n):
                return 2 ** ((n - 1).bit_length())
            
            new_width = next_power_of_two(new_width)
            new_height = next_power_of_two(new_height)
            
            # 限制最大尺寸
            new_width = min(new_width, max_size)
            new_height = min(new_height, max_size)
            
            print(f"  优化尺寸: {new_width}x{new_height}")
            
            # 调整尺寸
            if original_size != (new_width, new_height):
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 保存为优化后的JPEG
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 保存为渐进式JPEG（渐进加载）
            img.save(
                output_path,
                'JPEG',
                quality=quality,
                optimize=True,
                progressive=True
            )
            
            # 检查文件大小
            output_size = os.path.getsize(output_path)
            print(f"  文件大小: {output_size / 1024:.1f}KB")
            
            return True
            
    except Exception as e:
        print(f"  处理失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("魔方纹理图片优化工具")
    print("=" * 60)
    
    # 检查Pillow
    if not check_pillow():
        print("未找到Pillow库，尝试安装...")
        if not install_pillow():
            print("无法安装Pillow，请手动安装: pip install pillow")
            return 1
    
    # 纹理文件列表
    texture_files = ['wood.jpg', 'metal.jpg', 'plastic.jpg', 'marble.jpg', 'checker.jpg']
    
    # 检查文件是否存在
    missing_files = []
    for f in texture_files:
        if not os.path.exists(f):
            missing_files.append(f)
    
    if missing_files:
        print(f"找不到文件: {', '.join(missing_files)}")
        return 1
    
    # 创建备份目录
    backup_dir = "backup_original"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # 处理每张图片
    success_count = 0
    for texture_file in texture_files:
        print()
        
        # 备份原文件
        backup_path = os.path.join(backup_dir, texture_file)
        if not os.path.exists(backup_path):
            import shutil
            shutil.copy2(texture_file, backup_path)
        
        # 获取原文件信息
        original_size = os.path.getsize(texture_file)
        dimensions = get_image_dimensions(texture_file)
        
        if dimensions:
            print(f"{texture_file}:")
            print(f"  原始: {dimensions[0]}x{dimensions[1]}, {original_size/1024:.1f}KB")
        else:
            print(f"{texture_file}: {original_size/1024:.1f}KB")
        
        # 创建临时文件
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, texture_file)
        
        # 优化图片
        if optimize_texture(texture_file, temp_file):
            # 检查优化效果
            optimized_size = os.path.getsize(temp_file)
            reduction = (original_size - optimized_size) / original_size * 100
            
            if reduction > 0:
                print(f"  优化: 减少{reduction:.1f}%，节省{(original_size-optimized_size)/1024:.1f}KB")
            else:
                print(f"  优化: 文件大小变化不大")
            
            # 替换原文件
            import shutil
            shutil.move(temp_file, texture_file)
            success_count += 1
            
            # 清理临时目录
            shutil.rmtree(temp_dir)
        else:
            print(f"  跳过: 优化失败，使用原文件")
    
    print()
    print("=" * 60)
    print(f"优化完成: {success_count}/{len(texture_files)} 张图片处理成功")
    print(f"原文件备份在: {backup_dir}/")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())