#!/usr/bin/env python3
"""
Emoji → SVG Icon Migration Script
自动将 Vue 文件中的 emoji 替换为 Heroicons/Element Plus 图标
"""

import re
from pathlib import Path

# Emoji 到图标组件的映射
EMOJI_ICON_MAP = {
    # Heroicons Solid
    "🎨": ("PaintBrushIcon", "@heroicons/vue/24/solid"),
    "🚀": ("RocketLaunchIcon", "@heroicons/vue/24/solid"),
    "⚡": ("BoltIcon", "@heroicons/vue/24/solid"),
    "🔧": ("WrenchScrewdriverIcon", "@heroicons/vue/24/solid"),
    "📦": ("ArchiveBoxIcon", "@heroicons/vue/24/solid"),
    "💡": ("LightBulbIcon", "@heroicons/vue/24/solid"),
    "🧩": ("PuzzlePieceIcon", "@heroicons/vue/24/solid"),
    "👁️": ("EyeIcon", "@heroicons/vue/24/solid"),
    "🧠": ("CpuChipIcon", "@heroicons/vue/24/solid"),
    "🎯": ("BullseyeIcon", "@heroicons/vue/24/solid"),
    "✨": ("SparklesIcon", "@heroicons/vue/24/solid"),
    "🎮": ("CubeIcon", "@heroicons/vue/24/solid"),
    "🌙": ("MoonIcon", "@heroicons/vue/24/solid"),
    
    # Heroicons Outline
    "📊": ("ChartBarIcon", "@heroicons/vue/24/outline"),
    "📈": ("ArrowTrendingUpIcon", "@heroicons/vue/24/outline"),
    "🌐": ("GlobeAltIcon", "@heroicons/vue/24/outline"),
    "🔍": ("MagnifyingGlassIcon", "@heroicons/vue/24/outline"),
    "🌓": ("MoonIcon", "@heroicons/vue/24/outline"),
    "📱": ("DevicePhoneMobileIcon", "@heroicons/vue/24/outline"),
    "☁️": ("CloudIcon", "@heroicons/vue/24/solid"),
    "🔌": ("CloudIcon", "@heroicons/vue/24/solid"),  # 网络层用云图标
    
    # Element Plus Icons
    "🔒": ("Lock", "@element-plus/icons-vue"),
}

# 需要添加到文件的导入语句模板
HEROICONS_IMPORT = "import {{ICON_NAMES}}} from \"@heroicons/vue/24/{VARIANT}\";\n"
ELEMENT_PLUS_IMPORT = "import {{ICON_NAMES}}} from \"@element-plus/icons-vue\";\n"

def extract_emojis_from_file(file_path: Path) -> dict:
    """从文件中提取所有 emoji 及其位置"""
    emojis_found = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for emoji, (icon_name, package) in EMOJI_ICON_MAP.items():
        if emoji in content:
            count = content.count(emoji)
            if package not in emojis_found:
                emojis_found[package] = []
            emojis_found[package].append((emoji, icon_name, count))
    
    return emojis_found

def generate_import_statements(emojis_found: dict) -> str:
    """生成导入语句"""
    imports = []
    
    for package, icons in emojis_found.items():
        icon_names = list(set([icon_name for _, icon_name, _ in icons]))
        
        if "heroicons" in package:
            variant = "solid" if "solid" in package else "outline"
            import_stmt = f"import {{{', '.join(icon_names)}}} from \"@heroicons/vue/24/{variant}\";\n"
            imports.append(import_stmt)
        elif "element-plus" in package:
            import_stmt = f"import {{{', '.join(icon_names)}}} from \"@element-plus/icons-vue\";\n"
            imports.append(import_stmt)
    
    return "".join(imports)

def replace_emojis_in_template(content: str) -> str:
    """替换模板中的 emoji"""
    for emoji, (icon_name, package) in EMOJI_ICON_MAP.items():
        # 替换各种常见模式
        # 模式 1: <span class="icon">🎨</span>
        content = re.sub(
            rf'<span class="([^"]*icon[^"]*)">{emoji}</span>',
            rf'<{icon_name} class="\1 w-6 h-6" />',
            content
        )
        
        # 模式 2: <div class="icon">🎨</div>
        content = re.sub(
            rf'<div class="([^"]*icon[^"]*)">{emoji}</div>',
            rf'<{icon_name} class="\1 w-6 h-6" />',
            content
        )
        
        # 模式 3: <h3>🎨 Text</h3>
        content = re.sub(
            rf'(<h[1-6][^>]*>)({emoji})\s*',
            rf'\1<{icon_name} class="w-6 h-6 inline-block mr-2" /> ',
            content
        )
        
        # 模式 4: <span class="emoji">🎨</span>
        content = re.sub(
            rf'<span class="emoji">{emoji}</span>',
            rf'<{icon_name} class="w-6 h-6" />',
            content
        )
    
    return content

def process_vue_file(file_path: Path) -> None:
    """处理单个 Vue 文件"""
    print(f"\n{'='*60}")
    print(f"处理文件: {file_path}")
    print(f"{'='*60}")
    
    # 1. 提取 emoji
    emojis_found = extract_emojis_from_file(file_path)
    
    if not emojis_found:
        print("✓ 该文件没有需要替换的 emoji")
        return
    
    # 2. 统计信息
    total_emojis = sum(sum(count for _, _, count in icons) for icons in emojis_found.values())
    print(f"📊 发现 {total_emojis} 处 emoji:")
    
    for package, icons in emojis_found.items():
        for emoji, icon_name, count in icons:
            print(f"  {emoji} → {icon_name} ({count} 处)")
    
    # 3. 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 4. 生成导入语句
    imports = generate_import_statements(emojis_found)
    print(f"\n📦 需要添加的导入:\n{imports}")
    
    # 5. 替换模板中的 emoji
    new_content = replace_emojis_in_template(content)
    
    # 6. 添加导入语句（在 <script setup> 之后）
    if imports and "<script setup>" in new_content:
        # 找到 <script setup> 后的第一行 import
        script_match = re.search(r'<script setup>\n', new_content)
        if script_match:
            insert_pos = script_match.end()
            new_content = new_content[:insert_pos] + "\n" + imports + new_content[insert_pos:]
    
    # 7. 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 完成! 已替换 {total_emojis} 处 emoji")

def main():
    """主函数"""
    # 扫描所有 Vue 文件
    views_dir = Path("D:/Develop/PyCharm_Project/CubeMaster/frontend/src/views")
    
    vue_files = list(views_dir.glob("*.vue"))
    
    print(f"🔍 找到 {len(vue_files)} 个 Vue 文件")
    
    for vue_file in vue_files:
        process_vue_file(vue_file)
    
    print(f"\n{'='*60}")
    print("🎉 所有文件处理完成!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
