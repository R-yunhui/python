# -*- coding: utf-8 -*-
# 文件顶部的这行注释定义了文件的编码为 UTF-8，这样可以在代码中写中文注释

import sys

import math # 模块导入通常放在文件顶部

# --- 1. 变量和基本数据类型演示 ---
def demonstrate_variables():
    print(sys.prefix)

    """演示 Python 的变量定义和基本数据类型"""
    print("\n--- 1. 变量和基本数据类型 ---")
    # Python 是动态类型语言，不需要像 Java 那样显式声明变量类型
    message = "Hello, Python Learner!"  # 字符串 (String)
    count = 10                         # 整数 (Integer)
    price = 99.9                       # 浮点数 (Float)
    is_active = True                   # 布尔值 (Boolean)

    # 打印变量的值和类型
    print(message)
    print(f"类型: {type(message)}") # f-string 是一种方便的字符串格式化方式，类似 Java 的 String.format 或模板字面量
    print(f"Count: {count}, Type: {type(count)}")
    print(f"Price: {price}, Type: {type(price)}")
    print(f"Is Active: {is_active}, Type: {type(is_active)}")

# --- 2. 基本运算符演示 ---
def demonstrate_operators():
    """演示 Python 的基本算术运算符"""
    print("\n--- 2. 基本运算符 ---")
    a = 15
    b = 4
    print(f"a = {a}, b = {b}")
    print(f"a + b = {a + b}")       # 加
    print(f"a - b = {a - b}")       # 减
    print(f"a * b = {a * b}")       # 乘
    print(f"a / b = {a / b}")       # 除 (结果是浮点数)
    print(f"a // b = {a // b}")      # 整除 (结果是整数)
    print(f"a % b = {a % b}")       # 取余 (模运算)
    print(f"a ** b = {a ** b}")      # 幂运算 (a 的 b 次方)

# --- 3. 集合类型演示 ---
def demonstrate_collections():
    """演示 Python 的列表、元组和字典"""
    print("\n--- 3. 集合类型 ---")
    # 列表 (List): 可变序列
    my_list = [1, "apple", 3.14, True]
    print(f"\nOriginal List: {my_list}")
    print(f"Element at index 1: {my_list[1]}") # 索引从 0 开始
    my_list.append("banana")                   # 添加元素
    print(f"List after append: {my_list}")
    my_list[0] = "one"                         # 修改元素
    print(f"List after modification: {my_list}")

    # 元组 (Tuple): 不可变序列，一旦创建不能修改
    my_tuple = (10, 20, 30)
    print(f"\nTuple: {my_tuple}")
    print(f"Element at index 0: {my_tuple[0]}")
    # my_tuple[0] = 5 # 这行会报错，因为元组是不可变的

    # 字典 (Dictionary): 键值对集合，类似于 Java 的 HashMap
    my_dict = {"name": "Alice", "age": 30, "city": "New York"}
    print(f"\nDictionary: {my_dict}")
    print(f"Name: {my_dict['name']}")          # 通过键访问值
    my_dict["age"] = 31                      # 修改值
    print(f"Dictionary after update: {my_dict}")
    my_dict["occupation"] = "Engineer"       # 添加新的键值对
    print(f"Dictionary after add: {my_dict}")

# --- 4. 控制流演示 ---
def demonstrate_control_flow():
    """演示 Python 的条件语句和循环"""
    print("\n--- 4. 控制流 ---")
    # 条件语句 (if/elif/else)
    score = 75
    print(f"\nScore: {score}")
    if score >= 90:
        print("Grade: A")
    elif score >= 80: # elif 相当于 Java 的 else if
        print("Grade: B")
    elif score >= 60:
        print("Grade: C")
    else:
        print("Grade: D")

    # For 循环: 主要用于遍历序列
    print("\nLooping through a list:")
    # 在此函数内部定义一个用于演示循环的列表
    loop_list = ["a", "b", "c", 1, 2, 3]
    for item in loop_list: # 使用在此函数内定义的 loop_list
        print(item, end=" ") # end=" " 让 print 不换行，以空格结尾
    print() # 换行

    print("\nLooping with range:")
    for i in range(5): # range(5) 生成从 0 到 4 的序列 [0, 1, 2, 3, 4]
        print(i, end=" ")
    print()

    print("\nLooping through a dictionary (keys):")
    # 在此函数内部定义一个用于演示循环的字典
    loop_dict = {"key1": "value1", "key2": "value2"}
    for key in loop_dict: # 使用在此函数内定义的 loop_dict
        print(f"{key}: {loop_dict[key]}")

    # While 循环
    print("\nWhile loop:")
    counter = 0
    while counter < 3:
        print(f"Counter: {counter}")
        counter += 1 # Python 没有 ++ 或 -- 运算符，使用 += 1 或 -= 1

# --- 5. 函数定义与调用演示 ---
# greet 和 add 函数定义在全局作用域，以便 demonstrate_functions 调用
def greet(name):
    """这是一个函数文档字符串 (docstring)，用于解释函数的功能。"""
    print(f"\nHello, {name}!")

def add(x, y):
    """计算两个数的和"""
    return x + y

def demonstrate_functions():
    """演示 Python 的函数定义和调用"""
    print("\n--- 5. 函数 ---")
    # 调用上面定义的函数
    greet("Bob")

    result = add(5, 3)
    print(f"5 + 3 = {result}")
    # 访问函数的文档字符串
    print(f"Docstring for greet: {greet.__doc__}")

# --- 6. 类和对象演示 ---
# Python 也支持面向对象编程
class Dog:
    # 构造函数 (初始化方法)，相当于 Java 的构造器
    # 注意第一个参数总是 self，相当于 Java 的 this
    def __init__(self, name, breed):
        self.name = name    # 实例变量 (成员变量)
        self.breed = breed

    # 实例方法，第一个参数必须是 self
    def bark(self):
        print(f"{self.name} says Woof!")

def demonstrate_classes():
    """演示 Python 的类定义、对象创建和方法调用"""
    print("\n--- 6. 类和对象 (基础) ---")
    # 创建对象 (实例化)，不需要 new 关键字
    my_dog = Dog("Buddy", "Golden Retriever")

    # 访问属性和调用方法
    print(f"\nMy dog's name is {my_dog.name} and breed is {my_dog.breed}.")
    my_dog.bark()

# --- 7. 模块导入演示 ---
# 可以导入 Python 标准库或其他第三方库
def demonstrate_imports():
    """演示 Python 如何导入和使用模块"""
    print("\n--- 7. 模块导入 (基础) ---")
    # math 模块已在文件顶部导入
    print(f"Square root of 16 is: {math.sqrt(16)}")
    print(f"Value of PI is: {math.pi}")

    # 你也可以从模块中只导入特定的函数或变量
    # from math import sqrt, pi
    # print(f"Square root of 16 is: {sqrt(16)}")
    # print(f"Value of PI is: {pi}")

    # 演示只导入特定部分 (通常不推荐在函数内部这样做，但为了演示)
    from math import factorial
    print(f"Factorial of 5 (5!) is: {factorial(5)}")

# --- 主程序入口 ---
# 当这个脚本直接被运行时， __name__ 的值是 "__main__"
# 如果它被其他脚本导入，__name__ 的值是模块名 "main"
# 这是一个常见的 Python 惯用法，用来定义脚本的主执行逻辑
if __name__ == "__main__":
    print("--- Starting Python Syntax Demo ---")

    # demonstrate_variables()
    # demonstrate_operators()
    demonstrate_collections()
    # demonstrate_control_flow()
    # demonstrate_functions()
    # demonstrate_classes()
    # demonstrate_imports()

    print("\n--- End of Python Syntax Demo ---")
