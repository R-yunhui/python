import sys

def add_fun(a, b):
    return a + b

def sub_fun(a, b):
    return a - b

def mul_fun(a, b):
    return a * b

def div_fun(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b

def calculate_fun(a, b, operator):
    if operator == '+':
        return add_fun(a, b)
    elif operator == '-':
        return sub_fun(a, b)
    elif operator == '*':
        return mul_fun(a, b)
    elif operator == '/':
        return div_fun(a, b)
    else:
        raise ValueError("Invalid operator. Supported operators are: +, -, *, /.")

if __name__ == '__main__':
    print(sys.prefix)

    # 测试加法
    result = add_fun(3, 5)
    print(f"3 + 5 = {result}")

    # 测试减法
    result = sub_fun(10, 4)
    print(f"10 - 4 = {result}")

    # 测试乘法
    result = mul_fun(7, 6)
    print(f"7 * 6 = {result}")

    # 测试除法
    try:
        result = div_fun(8, 2)
        print(f"8 / 2 = {result}")
        result = div_fun(8, 0)  # 测试除以零的情况
        print(f"8 / 0 = {result}")
    except ValueError as e:
        print(e)

    # 测试计算器函数
    print("测试计算器函数")
    try:
        result = calculate_fun(5, 3, '+')
        print(f"5 + 3 = {result}")
        result = calculate_fun(5, 3, '-')
        print(f"5 - 3 = {result}")
        result = calculate_fun(5, 3, '*')
        print(f"5 * 3 = {result}")
        result = calculate_fun(5, 3, '/')
        print(f"5 / 3 = {result}")
        result = calculate_fun(5, 3, '%')  # 测试无效操作符
        print(f"5 % 3 = {result}")
    except ValueError as e:
        print(e)
