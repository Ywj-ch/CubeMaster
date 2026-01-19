import os
from pathlib import Path


def merge_project(root_dir, output_file):
    """
    将项目中的源代码合并为一个带有目录结构的 Markdown 文件
    """
    # 配置：需要包含的代码文件后缀名
    EXTENSIONS = {
        '.vue', '.js', '.ts', '.cpp', '.hpp', '.h',
        '.java', '.py', '.css', '.html', '.sql'
    }

    # 配置：绝对需要排除的目录（避免扫描第三方库或二进制文件）
    EXCLUDE_DIRS = {
        'node_modules', '.git', 'dist', 'build', 'target',
        '.vscode', '.idea', '__pycache__', '.venv_new', 'env', '.json'
    }

    root_path = Path(root_dir)

    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入 Markdown 头部信息
        f.write(f"# Project Source Code Context\n")
        f.write(f"Generated on: 2026-01-18\n")
        f.write(f"Root Directory: `{root_path.absolute()}`\n\n")
        f.write(f"---\n\n")

        # 递归遍历目录
        # rglob('*') 会搜索所有子目录下的文件
        for path in root_path.rglob('*'):
            # 1. 检查当前路径的任何部分是否在排除列表中
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue

            # 2. 只有是文件且符合后缀要求才处理
            if path.is_file() and path.suffix.lower() in EXTENSIONS:
                try:
                    # 获取相对于根目录的路径，这对 AI 理解项目逻辑至关重要
                    relative_path = path.relative_to(root_path)
                    print(f"正在处理: {relative_path}")

                    # 写入 Markdown 二级标题
                    f.write(f"## File Path: `{relative_path}`\n")

                    # 处理语法高亮标签
                    lang = path.suffix.lstrip('.').lower()
                    # 修正一些特殊的后缀名对应关系
                    lang_map = {
                        'hpp': 'cpp',
                        'h': 'cpp',
                        'vue': 'html',
                        'py': 'python',
                        'js': 'javascript',
                        'ts': 'typescript'
                    }
                    display_lang = lang_map.get(lang, lang)

                    f.write(f"```{display_lang}\n")

                    # 读取代码内容
                    # errors='ignore' 防止因为某些文件编码不是 utf-8 而崩溃
                    with open(path, 'r', encoding='utf-8', errors='ignore') as src:
                        content = src.read()
                        f.write(content)

                    f.write(f"\n```\n\n")
                    f.write(f"---\n\n")  # 分割线

                except Exception as e:
                    print(f"处理文件 {path} 时出错: {e}")


if __name__ == "__main__":
    # 配置：如果你想合并当前文件夹下的代码，就用 '.'
    # 结果会保存到 project_context.md
    target_project = '.'
    output_filename = 'project_context.md'

    print(f"开始合并项目: {Path(target_project).absolute()}")
    merge_project(target_project, output_filename)
    print(f"\n✅ 完成！合并结果已保存至: {output_filename}")