# -*- coding: utf-8 -*-
import random # 导入 random 模块用于生成随机数

def guess_number_game():
    """一个简单的猜数字游戏"""
    print("\n--- 猜数字游戏 --- (1-100)")

    # 1. 生成秘密数字
    lower_bound = 1
    upper_bound = 100
    secret_number = random.randint(lower_bound, upper_bound) # 生成指定范围内的随机整数
    attempts = 0 # 记录尝试次数
    guessed_correctly = False # 标记是否猜对

    print(f"我已经想好了一个 {lower_bound} 到 {upper_bound} 之间的数字，你来猜猜看！")

    # 2. 循环获取用户猜测，直到猜对为止
    while not guessed_correctly:
        guess_str = input("请输入你猜的数字: ") # 获取用户输入（总是字符串）
        attempts += 1 # 尝试次数加 1

        # 3. 验证输入并比较
        try:
            guess = int(guess_str) # 尝试将用户输入的字符串转换为整数

            # 检查输入是否在有效范围内
            if guess < lower_bound or guess > upper_bound:
                print(f"输入无效，请输入 {lower_bound} 到 {upper_bound} 之间的数字。")
                continue # 跳过本次循环的剩余部分，直接进入下一次猜测

            # 将猜测与秘密数字比较
            if guess < secret_number:
                print("太低了，再试试！")
            elif guess > secret_number:
                print("太高了，再试试！")
            else:
                # 猜对了！
                guessed_correctly = True # 设置标记为 True，结束 while 循环
                print(f"\n恭喜你，猜对了！秘密数字就是 {secret_number}!")
                print(f"你一共猜了 {attempts} 次。")

        except ValueError: # 如果 int(guess_str) 转换失败（用户输入的不是合法数字）
            print("输入无效，请输入一个整数数字。")
            # 循环会继续，提示用户重新输入

# --- 主程序入口 ---
if __name__ == "__main__":
    guess_number_game()
    print("\n--- 游戏结束 ---")
