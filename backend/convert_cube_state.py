import twophase.solver as sv
import os
import json
import re

# =========================
# 通用工具函数
# =========================

def normalize_color_list(raw_list):
    """
    将各种异常格式的颜色数据统一修复为颜色单词列表
    返回形如: ['white', 'red', ...]
    """
    if not raw_list:
        return []

    valid_colors = ['white', 'yellow', 'red', 'orange', 'blue', 'green']

    # 已经是正常的颜色单词列表
    if isinstance(raw_list, list) and len(raw_list) == 9 and len(str(raw_list[0])) > 1:
        return raw_list

    # 被拆成字符列表 ['g','r','e','e','n', ...]
    if isinstance(raw_list, list) and len(raw_list) > 9 and len(str(raw_list[0])) == 1:
        combined = ''.join(raw_list)
        return re.findall('|'.join(valid_colors), combined.lower())

    # 长字符串 "greenredblue..."
    if isinstance(raw_list, str):
        return re.findall('|'.join(valid_colors), raw_list.lower())

    return []


def parse_solution_moves(raw_solution: str):
    """统一解析 Kociemba 解法中的动作序列"""
    raw_solution = re.sub(r"\(.*?\)", "", raw_solution).strip()
    return re.findall(r"[UDLRFB][123']?", raw_solution)


# =========================
# 状态解析与转换
# =========================

def parse_cube_state_from_file(filename='cube_results/cube_state.json'):
    """从 JSON 文件解析魔方状态"""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"找不到文件: {filename}")

    with open(filename, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    cube_state = {}
    for face, matrix in raw_data.items():
        flat = [c for row in matrix for c in row]
        cube_state[face] = flat

    return cube_state


def convert_to_kociemba_format(cube_state):
    """将魔方状态转换为 Kociemba 54 字符串"""
    color_mapping = {
        'white': 'U', 'yellow': 'D', 'red': 'R',
        'orange': 'L', 'green': 'F', 'blue': 'B'
    }
    order = ['U', 'R', 'F', 'D', 'L', 'B']
    result = ''

    for face in order:
        raw_list = cube_state.get(face, [])
        colors = normalize_color_list(raw_list)

        if len(colors) < 9:
            print(f"❌ {face} 面颜色不足 9 个")
            result += '?' * 9
            continue

        for c in colors[:9]:
            result += color_mapping.get(c, '?')

    return result


def validate_kociemba_state(kociemba_string):
    """验证 Kociemba 状态合法性"""
    if len(kociemba_string) != 54:
        return False, f"长度错误: {len(kociemba_string)} / 54"

    centers = {
        'U': kociemba_string[4],
        'R': kociemba_string[13],
        'F': kociemba_string[22],
        'D': kociemba_string[31],
        'L': kociemba_string[40],
        'B': kociemba_string[49]
    }

    for face, val in centers.items():
        if face != val:
            return False, f"{face} 面中心错误，应为 {face}，检测为 {val}"

    return True, '状态有效'


# =========================
# 解法解析与保存
# =========================

def convert_to_readable(raw_solution):
    moves = parse_solution_moves(raw_solution)

    face_map = {
        'U': '上', 'D': '下', 'F': '前',
        'B': '后', 'L': '左', 'R': '右'
    }

    direction_map = {
        '1': '顺时针90°',
        '2': '旋转180°',
        '3': '逆时针90°',
        "'": '逆时针90°'
    }

    readable = []
    for m in moves:
        face = m[0]
        suffix = m[1] if len(m) > 1 else '1'
        if suffix == '2':
            readable.append(f"{face_map[face]}面旋转180°")
        else:
            readable.append(f"{face_map[face]}面{direction_map[suffix]}")

    return readable


def parse_raw_solution(raw_solution):
    moves = parse_solution_moves(raw_solution)
    result = []

    for m in moves:
        face = m[0]
        suffix = m[1:] if len(m) > 1 else '1'
        if suffix == '1':
            result.append(face)
        elif suffix == '2':
            result.append(face + '2')
        elif suffix in ('3', "'"):
            result.append(face + "'")

    return result


def save_solution_results(solution, kociemba_code, output_dir='cube_results'):
    os.makedirs(output_dir, exist_ok=True)

    readable = convert_to_readable(solution)
    moves = parse_raw_solution(solution)

    path = os.path.join(output_dir, 'solution.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({
            'kociemba_code': kociemba_code,
            'raw_solution': solution,
            'moves': moves,
            'readable_solution': readable,
            'step_count': len(moves)
        }, f, ensure_ascii=False, indent=2)

    return readable, moves


# =========================
# 求解主流程（供 API 调用）
# =========================

def solve_cube_pipeline():
    cube_state = parse_cube_state_from_file('cube_results/cube_state.json')
    kociemba_code = convert_to_kociemba_format(cube_state)

    valid, msg = validate_kociemba_state(kociemba_code)
    if not valid:
        raise RuntimeError(msg)

    solution = sv.solve(kociemba_code, 20, 2).replace('\n', '').strip()
    readable, moves = save_solution_results(solution, kociemba_code)

    return {
        'kociemba_code': kociemba_code,
        'raw_solution': solution,
        'moves': moves,
        'readable_solution': readable,
        'step_count': len(moves)
    }


# =========================
# CLI 调试入口（可选）
# =========================

def main():
    try:
        cube_state = parse_cube_state_from_file('cube_results/cube_state.json')
        code = convert_to_kociemba_format(cube_state)
        print('Kociemba 编码:', code)
        valid, msg = validate_kociemba_state(code)
        print('校验结果:', msg)
        return code
    except Exception as e:
        print('❌', e)
        return None


if __name__ == '__main__':
    code = main()
    if code:
        result = solve_cube_pipeline()
        for i, step in enumerate(result['readable_solution'], 1):
            print(f"步骤{i}: {step}")