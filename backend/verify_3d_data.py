# verify_3d_data.py
import json
import os


def verify_solution_data():
    """
    验证求解结果数据
    """
    json_file = 'cube_results/solution.json'

    if not os.path.exists(json_file):
        print("❌ 未找到solution.json文件")
        return False

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 验证必要字段
        required_fields = ['kociemba_code', 'raw_solution', 'moves','readable_solution', 'step_count']
        for field in required_fields:
            if field not in data:
                print(f"❌ 缺少必要字段: {field}")
                return False

        print("✅ 数据格式验证通过")
        print(f"魔方编码: {data['kociemba_code'][:20]}...")
        print(f"解法步骤数: {data['step_count']}")
        print(f"原始解法: {data['raw_solution']}")
        print(f"旋转操作: {data['moves']}")
        print(f"可读步骤: {data['readable_solution'][:3]}...")

        return True

    except Exception as e:
        print(f"❌ 数据验证失败: {e}")
        return False


if __name__ == "__main__":
    verify_solution_data()
