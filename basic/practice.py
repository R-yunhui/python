## python 练习

def basic_datastruct_test():
    
    print("--- 字符串 (String) 示例 ---")
    my_str = "Hello Word!"
    print(f"字符串长度: {len(my_str)}")
    print(f"获取字符串第一个字符: {my_str[0]}")
    print(f"获取字符串最后一个字符: {my_str[-1]}")
    print(f"根据指定的分隔符将字符串分割成列表: {my_str.split(' ')}")
    print(f"将字符串转换为小写: {my_str.lower()}")
    print(f"将字符串转换为大写: {my_str.upper()}")

    print("--- 列表 (List) 示例 ---")
    my_list = [1, 2, 3, 4, 5]
    print(f"原始列表: {my_list}")
    print(f"列表长度: {len(my_list)}")
    print(f"第一个元素: {my_list[0]}")
    print(f"切片 [1:4]: {my_list[1:4]}")
    my_list.append(6)
    print(f"添加元素 6: {my_list}")
    my_list.remove(2)
    print(f"移除元素 2: {my_list}")
    print(f"元素 3 是否在列表中: {3 in my_list}")

    print("\n--- 元组 (Tuple) 示例 ---")
    my_tuple = (10, 20, 30)
    print(f"原始元组: {my_tuple}")
    print(f"元组长度: {len(my_tuple)}")
    print(f"第一个元素: {my_tuple[0]}")
    # 元组是不可变的，不能修改元素

    print("\n--- 字典 (Dictionary) 示例 ---")
    my_dict = {"a": 1, "b": 2, "c": 3}
    print(f"原始字典: {my_dict}")
    print(f"字典长度: {len(my_dict)}")
    print(f"键 'b' 对应的值: {my_dict['b']}")
    my_dict["d"] = 4
    print(f"添加键 'd': {my_dict}")
    del my_dict["a"]
    print(f"删除键 'a': {my_dict}")
    print(f"所有键: {my_dict.keys()}")
    print(f"所有值: {my_dict.values()}")

    print("\n--- 集合 (Set) 示例 ---")
    my_set = {1, 2, 3, 2, 1}
    print(f"原始集合: {my_set}") # 集合会自动去重
    my_set.add(4)
    print(f"添加元素 4: {my_set}")
    my_set.remove(2)
    print(f"移除元素 2: {my_set}")
    other_set = {3, 4, 5}
    print(f"集合并集: {my_set.union(other_set)}")
    print(f"集合交集: {my_set.intersection(other_set)}")

    print("\n--- 数字类型 (int, float) 示例 ---")
    integer_num = 10
    float_num = 20.5
    print(f"整数: {integer_num}")
    print(f"浮点数: {float_num}")
    print(f"相加: {integer_num + float_num}")
    print(f"类型转换 (int to float): {float(integer_num)}")
    print(f"类型转换 (float to int): {int(float_num)}")

if __name__ == "__main__":
    basic_datastruct_test()   