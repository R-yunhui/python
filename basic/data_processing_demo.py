# -*- coding: utf-8 -*-
import statistics # 导入 statistics 模块用于计算统计值，如平均数和中位数
# import collections # 如果想用 Counter，需要导入这个模块

def demonstrate_data_processing():
    """演示基本的数据处理和简单分析"""
    print("\n--- 数据处理与简单分析演示 ---")

    # --- 1. 示例数据 ---
    # 假设我们有一组学生数据，存储在字典列表中
    # 这种结构很常见，例如从 JSON 文件或数据库查询结果中获取的数据
    students_data = [
        {"name": "Alice", "score": 85, "city": "New York"},
        {"name": "Bob", "score": 92, "city": "London"},
        {"name": "Charlie", "score": 78, "city": "New York"},
        {"name": "David", "score": 92, "city": "Paris"},
        {"name": "Eve", "score": 88, "city": "London"},
    ]
    print("\n原始学生数据:")
    for student in students_data:
        print(student)

    # --- 2. 提取特定数据列 ---
    # 使用列表推导式 (List Comprehension) 是一种简洁高效的方式
    # 语法: [expression for item in iterable if condition]
    scores = [student["score"] for student in students_data]
    print(f"\n所有学生的分数列表: {scores}")

    # --- 3. 基本统计计算 ---
    if scores: # 确保列表不为空，防止计算出错
        # 计算平均分
        average_score = statistics.mean(scores)
        print(f"平均分数: {average_score:.2f}") # :.2f 格式化字符串，保留两位小数

        # 找到最高分和最低分
        max_score = max(scores)
        min_score = min(scores)
        print(f"最高分数: {max_score}")
        print(f"最低分数: {min_score}")

        # 计算分数中位数 (排序后中间的值)
        median_score = statistics.median(scores)
        print(f"分数中位数: {median_score}")
    else:
        print("\n没有分数数据可供分析。")
        average_score = 0 # 设定一个默认值，避免后面筛选时出错
        max_score = 0

    # --- 4. 根据条件筛选数据 ---
    # 筛选出来自伦敦 (London) 的学生 (使用列表推导式)
    london_students = [student for student in students_data if student["city"] == "London"]
    print("\n来自伦敦的学生:")
    if london_students:
        for student in london_students:
            print(student)
    else:
        print("没有来自伦敦的学生。")

    # 筛选出分数高于平均分的学生姓名
    above_average_students = [student["name"] for student in students_data if student["score"] > average_score]
    print(f"\n分数高于平均分 ({average_score:.2f}) 的学生姓名: {above_average_students}")

    # --- 5. 查找特定信息 ---
    # 找到分数最高的学生 (可能有多个)
    top_students = [student["name"] for student in students_data if student["score"] == max_score]
    print(f"\n分数最高的学生 ({max_score}): {top_students}")

    # --- 6. 简单的数据聚合 (按城市统计学生数量) ---
    city_counts = {} # 创建一个空字典来存储计数
    for student in students_data:
        city = student["city"]
        # 使用字典的 get(key, default) 方法更简洁地处理计数
        city_counts[city] = city_counts.get(city, 0) + 1

    # 如果想用更 Pythonic 的方式，可以使用 collections.Counter:
    # from collections import Counter
    # cities = [student["city"] for student in students_data]
    # city_counts_counter = Counter(cities)
    # print("\n按城市统计学生数量 (使用 Counter):")
    # print(dict(city_counts_counter)) # 转回普通字典打印

    print("\n按城市统计学生数量:")
    print(city_counts)

# --- 主程序入口 ---
if __name__ == "__main__":
    demonstrate_data_processing()
    print("\n--- 数据处理演示结束 ---")
