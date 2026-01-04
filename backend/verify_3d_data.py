import json
import os

"""
魔方求解结果数据验证模块

用于验证solution.json文件的数据完整性和格式正确性。
确保求解结果数据可用于后续的三维可视化处理。
"""

def verify_solution_data():
    """验证魔方求解结果数据

    检查solution.json文件的存在性、数据完整性和格式正确性。
    确保数据包含所有必要字段且格式正确，以供三维可视化使用。

    Returns:
        bool: 验证通过返回True，否则返回False

    Note:
        验证的必需字段包括：
        - kociemba_code: Kociemba格式的魔方状态编码
        - raw_solution: 原始解法字符串
        - moves: 标准化步骤列表
        - readable_solution: 人类可读的解法步骤
        - step_count: 解法步骤总数
    """
    # 定义求解结果JSON文件路径
    json_file = 'cube_results/solution.json'

    # 检查文件是否存在
    if not os.path.exists(json_file):
        print("❌ 未找到solution.json文件")
        print("   请先运行魔方求解流程生成数据")
        return False

    try:
        # 读取并解析JSON文件
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 定义必需字段列表
        required_fields = [
            'kociemba_code',  # Kociemba编码
            'raw_solution',  # 原始解法字符串
            'moves',  # 标准化步骤列表
            'readable_solution',  # 可读解法步骤
            'step_count'  # 步骤总数
        ]

        # 验证所有必需字段是否存在
        for field in required_fields:
            if field not in data:
                print(f"❌ 缺少必要字段: {field}")
                print(f"   请检查求解结果数据的完整性")
                return False

        # 验证字段数据类型
        if not isinstance(data['moves'], list):
            print("❌ 'moves'字段应为列表类型")
            return False

        if not isinstance(data['readable_solution'], list):
            print("❌ 'readable_solution'字段应为列表类型")
            return False

        if not isinstance(data['step_count'], int):
            print("❌ 'step_count'字段应为整数类型")
            return False

        # 验证步骤数量一致性
        if data['step_count'] != len(data['moves']):
            print("❌ 'step_count'与'moves'列表长度不一致")
            print(f"   step_count: {data['step_count']}, moves长度: {len(data['moves'])}")
            return False

        # 验证Kociemba编码长度（应为54个字符）
        if len(data['kociemba_code']) != 54:
            print("❌ Kociemba编码长度不正确")
            print(f"   应为54个字符，实际为{len(data['kociemba_code'])}个")
            return False

        # 验证步骤数量合理性
        if data['step_count'] == 0:
            print("⚠️ 警告: 步骤数量为0，可能是已还原状态")
        elif data['step_count'] > 30:
            print("⚠️ 警告: 步骤数量较多，可能需要较长还原时间")

        # 验证通过，显示数据摘要
        print("✅ 数据格式验证通过")
        print(f"📋 数据摘要:")
        print(f"   魔方编码: {data['kociemba_code'][:20]}...")  # 显示前20个字符
        print(f"   解法步骤数: {data['step_count']}")
        print(f"   原始解法: {data['raw_solution'][:50]}..." if len(
            data['raw_solution']) > 50 else f"   原始解法: {data['raw_solution']}")
        print(f"   旋转操作: {data['moves'][:5]}{'...' if len(data['moves']) > 5 else ''}")  # 显示前5个步骤
        print(
            f"   可读步骤: {data['readable_solution'][:3]}{'...' if len(data['readable_solution']) > 3 else ''}")  # 显示前3个步骤

        # 显示详细统计信息
        print(f"📊 详细统计:")
        print(f"   - 总步骤数: {data['step_count']}")
        print(f"   - Kociemba编码长度: {len(data['kociemba_code'])}")
        print(f"   - 可读步骤数量: {len(data['readable_solution'])}")

        # 检查是否存在未知颜色占位符
        if '?' in data['kociemba_code']:
            print("⚠️ 警告: Kociemba编码中包含未知颜色占位符'?'")
            unknown_count = data['kociemba_code'].count('?')
            print(f"   共发现{unknown_count}个未知颜色块")

        return True

    except json.JSONDecodeError as e:
        # JSON格式解析错误
        print(f"❌ JSON格式错误: {e}")
        print("   请检查solution.json文件格式是否正确")
        return False

    except KeyError as e:
        # 键错误
        print(f"❌ 数据键错误: {e}")
        return False

    except Exception as e:
        # 其他未知错误
        print(f"❌ 数据验证失败: {e}")
        return False


if __name__ == "__main__":
    """
    模块独立运行时的入口函数

    直接运行此脚本将验证solution.json文件，
    输出验证结果。
    """
    print("🔍 开始验证魔方求解结果数据...")
    print("=" * 50)

    success = verify_solution_data()

    print("=" * 50)
    if success:
        print("🎉 数据验证完成，可以用于三维可视化")
    else:
        print("❌ 数据验证失败，请检查数据源")

    # 返回验证结果作为退出码
    exit(0 if success else 1)