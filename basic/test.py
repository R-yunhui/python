from typing import List

def print_test():
    # 基础打印的练习
    print("Hello World！")
    
    print("My name is", " Mike")

    print("My age is", 30)

def base_operation():
    a = 10
    b = 20
    c = a + b
    d = a / b
    e = a - b
    f = a * b
    print("Addition:", c)
    print("Subtraction:", d)
    print("Multiplication:", e)
    print("Division:", f)

def conditional_statements(str1, str2, score=0):
    if str1 == str2:
        print("Strings are equal")
    else:
        print("Strings are not equal")

    if len(str1) > 3:
        print("String 1 is longer than 3 characters")

    if score == 100:
        print("满分")
    elif score >= 85:
        print("优秀")
    elif score >= 70:
        print("良好")
    elif score >= 60:
        print("及格")
    else:
        print("不及格")

def loops_statements():
    # 循环练习
    # 打印1到5
    numbers: List[int] = [1, 2, 3, 4, 5]
    for i in numbers:
        print(i)
    else:
        print("循环结束")

    # 2. while循环
    # 计算1到10的和
    sum = 0
    i = 1
    while i <= 10:
        sum += i
        i += 1
    print(f"1到10的和是：{sum}")

    # 打印 9 * 9 乘法表
    for i in range(1, 10):
        for j in range(1, i + 1):
            print(f"{i}×{j}={i * j}", end="\t")
            print()

def calculate():
    # 如果用户没有输出 exit 一直进行操作
    while True:
        print("请输入两个数字和一个运算符，用空格隔开，例如：1 + 2\n如果想退出计算器请输入 exit\n")
        user_input = input()
        if user_input == "exit":
            print("退出计算器")
            break
        else:
            inputs : List[int] = user_input.split(" ")
            num_one = int(inputs[0])
            operator = inputs[1]
            num_two = int(inputs[2])
            if operator == "+":
                print(f"{num_one} + {num_two} = {num_one + num_two}")
            elif operator == "-":
                print(f"{num_one} - {num_two} = {num_one - num_two}")
            elif operator == "*":
                print(f"{num_one} * {num_two} = {num_one * num_two}")
            elif operator == "/":
                print(f"{num_one} / {num_two} = {num_one / num_two}")
            else:
                print("输入的运算符有误")

if __name__ == "__main__":
    print("----- 基础打印练习 -----")
    print_test()

    print("\n----- 基础运算练习 -----")
    base_operation()

    print("\n----- 条件语句练习 -----")
    conditional_statements("test1", "test2")
    conditional_statements("test1", "test2", 33)

    print("\n----- 循环练习 -----")
    loops_statements()

    print("\n----- 计算器练习 -----")
    calculate()
