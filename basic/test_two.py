import os
from typing import List

# 基础的学生类定义
class Student:
    def __init__(self, name: str, age: int, score: float):
        if score < 0 or score > 100:
            raise ValueError("分数必须在0到100之间")
        if age < 0 or age > 100:
            raise ValueError("年龄必须在0到100之间")

        self.name = name
        self.score = score
        self.age = age

    def introduction(self):
        score_range = self.check_range()
        print(f"我的名字是 {self.name}, 我今年 {self.age} 岁, 我这次考了 {self.score} 分, 等级是 {score_range}.")

    def check_range(self):
        if self.score == 100:
            return "满分"
        elif self.score >= 85:
            return "优秀"
        elif self.score >= 70:
            return "良好"
        elif self.score >= 60:
            return "及格"
        else:
            return "不及格"

# 2. 继承练习
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        # pass：不需要执行任何代码时的占位符
        pass

# 继承自 Animal 类
class Dog(Animal):
    def speak(self):
        return f"{self.name}说：汪汪！"

# 继承自 Animal 类
class Cat(Animal):
    def speak(self):
        return f"{self.name}说：喵喵！"

# 基础 io 练习
def io_test():
    # 创建一个文件
    file_path = "./demo.txt"

    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在，正在创建...")
        try:
            # 创建并写入文件
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("Hello, World!")
            print(f"文件 {file_path} 创建成功。")
        except Exception as e:
            print(f"创建文件时发生错误: {e}")
    else:
        print(f"文件 {file_path} 已存在。")
        # 读取文件内容
        try:
            # 读取文件内容
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                print(f"文件内容: {content}")
        except Exception as e:
            print(f"读取文件时发生错误: {e}")

if __name__ == "__main__":
    # 初始化一个学生的列表 List
    student_list : List[Student] = [
        Student("小明", 15, 90),
        Student("小红", 16, 80),
        Student("小刚", 17, 70),
        Student("小美", 18, 60),
        Student("小强", 19, 50)
    ]
    # 调用
    for student in student_list:
        student.introduction()

    # 使用示例
    dog = Dog("旺财")
    cat = Cat("咪咪")
    print(dog.speak())
    print(cat.speak())

    # 文件读写
    io_test()
