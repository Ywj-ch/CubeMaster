import twophase.solver as sv
import os
import json
import re


def parse_cube_state_from_file(filename='cube_results/cube_state.txt'):
    """从文本文件解析魔方状态

    解析由CubeDetector生成的魔方状态文本文件，提取六面颜色矩阵。

    Args:
        filename: 魔方状态文本文件路径

    Returns:
        dict: 魔方状态字典，键为面标识(U/R/F/D/L/B)，值为该面9个色块的颜色列表
    """
    cube_state = {}

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_face = None  # 当前正在处理的面标识
    face_data = []  # 当前面收集的颜色数据

    for line in lines:
        line = line.strip()

        # 检测面的开始行（通过中文描述识别）
        if '上面 (UP' in line:
            current_face = 'U'
            face_data = []
        elif '右面 (RIGHT' in line:
            current_face = 'R'
            face_data = []
        elif '前面 (FRONT' in line:
            current_face = 'F'
            face_data = []
        elif '下面 (DOWN' in line:
            current_face = 'D'
            face_data = []
        elif '左面 (LEFT' in line:
            current_face = 'L'
            face_data = []
        elif '后面 (BACK' in line:
            current_face = 'B'
            face_data = []

        # 解析颜色行（格式如："['red', 'orange', 'blue']"）
        elif line.startswith("['") and current_face:
            # 提取颜色字符串并清理格式
            colors_str = line.replace("'", "").replace("[", "").replace("]", "")
            colors = [color.strip() for color in colors_str.split(',')]
            face_data.extend(colors)  # 添加到当前面数据

            # 当收集到9个颜色时（一个完整的3x3面），保存该面数据
            if len(face_data) == 9:
                cube_state[current_face] = face_data.copy()
                face_data = []  # 重置为下一个面准备

    return cube_state


def convert_to_kociemba_format(cube_state):
    """将魔方状态转换为Kociemba算法要求的字符串格式

    按照标准顺序(U, R, F, D, L, B)将颜色转换为单字母表示。

    Args:
        cube_state: 魔方状态字典

    Returns:
        str: Kociemba格式的54个字符字符串
    """
    # 颜色名称到Kociemba字母的映射
    color_mapping = {
        'white': 'U',  # 上面
        'red': 'R',  # 右面
        'green': 'F',  # 前面
        'yellow': 'D',  # 下面
        'orange': 'L',  # 左面
        'blue': 'B'  # 后面
    }

    # Kociemba算法要求的固定面顺序
    kociemba_order = ['U', 'R', 'F', 'D', 'L', 'B']
    kociemba_string = ""

    for face in kociemba_order:
        if face in cube_state:
            colors = cube_state[face]
            for color in colors:
                if color in color_mapping:
                    kociemba_string += color_mapping[color]
                else:
                    # 遇到未映射的颜色，使用问号占位并警告
                    print(f"⚠️ 警告: 未知颜色 '{color}' 在面 {face}")
                    kociemba_string += '?'
        else:
            print(f"❌ 错误: 缺少面 {face} 的数据")

    return kociemba_string


def validate_kociemba_state(kociemba_string):
    """验证Kociemba状态字符串的有效性

    检查字符串长度是否为54，并验证每个面的中心块是否正确。

    Args:
        kociemba_string: Kociemba格式的状态字符串

    Returns:
        tuple: (是否有效, 验证消息)
    """
    # 检查字符串长度
    if len(kociemba_string) != 54:
        return False, f"长度错误: 需要54个字符，实际得到{len(kociemba_string)}个"

    # 检查每个面的中心块（标准位置）
    centers = {
        'U': kociemba_string[4],  # U面中心位置（索引4）
        'R': kociemba_string[13],  # R面中心位置（索引13）
        'F': kociemba_string[22],  # F面中心位置（索引22）
        'D': kociemba_string[31],  # D面中心位置（索引31）
        'L': kociemba_string[40],  # L面中心位置（索引40）
        'B': kociemba_string[49]  # B面中心位置（索引49）
    }

    # 预期的中心块字母
    expected_centers = {'U': 'U', 'R': 'R', 'F': 'F', 'D': 'D', 'L': 'L', 'B': 'B'}

    # 验证每个中心块
    for face, actual in centers.items():
        if actual != expected_centers[face]:
            return False, f"面{face}的中心应该是{expected_centers[face]}，但检测到{actual}"

    return True, "状态有效"


def convert_to_readable(kociemba_solution):
    """将Kociemba解法转换为人类可读的中文步骤

    自动忽略(19f)等统计信息，将符号表示转换为中文描述。

    Args:
        kociemba_solution: Kociemba求解器返回的原始解法字符串

    Returns:
        list: 人类可读的中文解法步骤列表
    """
    # 提取合法的魔方步骤（匹配U, D, L, R, F, B及可能的数字或'后缀）
    moves = re.findall(r"[UDLRFB][123']?", kociemba_solution)

    # 面标识到中文的映射
    face_map = {
        'U': '上', 'D': '下', 'F': '前',
        'B': '后', 'L': '左', 'R': '右'
    }

    # 方向后缀到中文描述的映射
    direction_map = {
        '1': '顺时针90°',  # 默认方向，通常省略
        '2': '旋转180°',  # 180度旋转
        '3': '逆时针90°',  # 逆时针旋转
        "'": '逆时针90°'  # 另一种逆时针表示
    }

    readable_steps = []

    for move in moves:
        face = move[0]  # 面标识
        direction = move[1] if len(move) > 1 else '1'  # 旋转方向（默认为1）

        face_cn = face_map[face]
        direction_cn = direction_map[direction]

        # 特殊处理180度旋转
        if direction == '2':
            readable_steps.append(f"{face_cn}面旋转180°")
        else:
            readable_steps.append(f"{face_cn}面{direction_cn}")

    return readable_steps


def parse_raw_solution(raw_solution: str):
    """将原始解法字符串解析为标准化步骤列表

    将如"F3 D3 L3 ... (19f)"转换为['F'', 'D'', 'L'', 'U', ...]格式，
    便于前端或其他程序处理。

    Args:
        raw_solution: Kociemba求解器返回的原始解法字符串

    Returns:
        list: 标准化步骤列表
    """
    # 移除(19f)等统计信息
    raw_solution = re.sub(r"\(.*?\)", "", raw_solution).strip()

    moves = []
    tokens = raw_solution.split()

    for t in tokens:
        face = t[0]  # 面标识
        suffix = t[1:] if len(t) > 1 else "1"  # 旋转方向后缀

        # 转换为标准表示法
        if suffix == "1":
            moves.append(face)  # 顺时针90°
        elif suffix == "2":
            moves.append(face + "2")  # 180°
        elif suffix == "3":
            moves.append(face + "'")  # 逆时针90°

    return moves


def save_solution_results(solution, kociemba_code, output_dir='cube_results'):
    """保存求解结果到JSON文件

    将原始解法、标准化步骤和可读步骤保存为结构化JSON。

    Args:
        solution: 原始解法字符串
        kociemba_code: Kociemba格式的状态字符串
        output_dir: 输出目录

    Returns:
        tuple: (可读步骤列表, 标准化步骤列表)
    """
    os.makedirs(output_dir, exist_ok=True)

    # 转换格式
    readable_solution = convert_to_readable(solution)
    moves = parse_raw_solution(solution)

    # 保存到JSON文件
    json_file = os.path.join(output_dir, 'solution.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'kociemba_code': kociemba_code,  # 魔方状态编码
            'raw_solution': solution,  # 原始解法字符串
            'moves': moves,  # 标准化步骤列表
            'readable_solution': readable_solution,  # 中文可读步骤
            'step_count': len(moves)  # 总步数
        }, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON格式已保存: {json_file}")

    return readable_solution, moves


def solve_cube_pipeline():
    """魔方求解完整流程

    从文件解析魔方状态，转换为Kociemba格式，验证并求解。

    Returns:
        dict: 包含求解结果的完整信息字典

    Raises:
        RuntimeError: 当魔方状态无效时抛出
    """
    # 1. 从文件解析魔方状态
    cube_state = parse_cube_state_from_file('cube_results/cube_state.txt')

    # 2. 转换为Kociemba格式
    kociemba_code = convert_to_kociemba_format(cube_state)

    # 3. 验证状态有效性
    is_valid, msg = validate_kociemba_state(kociemba_code)
    if not is_valid:
        raise RuntimeError(msg)

    # 4. 调用Kociemba求解器（最大深度20，超时2秒）
    solution = sv.solve(kociemba_code, 20, 2)
    solution = solution.replace("\n", "").strip()

    # 5. 保存求解结果
    readable_solution, moves = save_solution_results(solution, kociemba_code)

    # 6. 返回完整结果
    return {
        "kociemba_code": kociemba_code,
        "raw_solution": solution,
        "moves": moves,
        "readable_solution": readable_solution,
        "step_count": len(moves)
    }


def main():
    """主函数：执行魔方求解完整流程

    流程步骤：
    1. 解析魔方状态文件
    2. 转换为Kociemba格式
    3. 验证状态有效性
    4. 显示求解命令（备用）
    5. 调用求解管道
    """
    try:
        # 1. 从文件解析魔方状态
        print("📖 正在解析cube_state.txt文件...")
        cube_state = parse_cube_state_from_file('cube_results/cube_state.txt')

        # 显示解析结果
        print("\n🔍 解析到的魔方状态:")
        for face, colors in cube_state.items():
            print(f"  {face}面: {colors}")

        # 2. 转换为Kociemba格式
        print("\n🔄 正在转换为kociemba格式...")
        kociemba_string = convert_to_kociemba_format(cube_state)
        print(f"✅ kociemba编码: {kociemba_string}")

        # 3. 验证状态有效性
        print("\n🔍 验证状态有效性...")
        is_valid, message = validate_kociemba_state(kociemba_string)
        if is_valid:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")

        # 4. 保存Kociemba编码到文件
        output_filename = 'cube_results/kociemba_state.txt'
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(kociemba_string)
        print(f"\n💾 kociemba编码已保存到: {output_filename}")

        # 5. 显示求解命令（供手动调试使用）
        print(f"\n🎯 求解命令:")
        print(f"python -c \"import two_phase.solver as sv; print(sv.solve('{kociemba_string}', 20, 2))\"")

        return kociemba_string

    except FileNotFoundError:
        print("❌ 错误: 找不到cube_state.txt文件")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


if __name__ == "__main__":
    """程序入口点"""
    # 1. 执行主函数获取Kociemba编码
    kociemba_code = main()

    if kociemba_code:
        try:
            # 2. 执行求解管道
            print("\n🎯 开始求解...")
            result = solve_cube_pipeline()

            # 3. 显示求解结果
            print("\n🎉 求解成功")
            for i, step in enumerate(result["readable_solution"], 1):
                print(f"步骤{i}: {step}")

        except Exception as e:
            print(f"\n❌ 求解失败: {e}")