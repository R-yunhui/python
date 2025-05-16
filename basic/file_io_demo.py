# -*- coding: utf-8 -*-

def demonstrate_file_io():
    """演示基本的文件读写操作"""
    print("\n--- 文件操作 (File I/O) 演示 ---")

    file_path = "study/sample.txt" # 定义要操作的文件路径和名称

    # --- 1. 写入文件 ('w'模式) ---
    # 'w' 模式会覆盖已存在的文件内容；如果文件不存在，则会创建新文件。
    # 使用 with open(...) as ... 是一种推荐的方式，它能确保文件最终会被正确关闭，即使发生错误。
    # encoding='utf-8' 指定文件编码，以支持中文等非 ASCII 字符。
    print(f"\n[写入] 正在向文件 {file_path} 写入内容 (w 模式)...")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("这是第一行文本。\n") # write() 写入字符串
            f.write("Hello, File!\n")
            lines_to_write = ["第三行来自列表。\n", "这是最后一行写入。\n"]
            f.writelines(lines_to_write) # writelines() 可以写入一个字符串列表
        print("[写入] 文件写入成功。")
    except IOError as e: # 捕获可能的文件操作错误
        print(f"[写入] 文件时出错: {e}")

    # --- 2. 读取文件 ('r'模式) ---
    # 'r' 模式是默认模式（不写模式参数时就是r），用于读取文件。如果文件不存在会报错。
    print(f"\n[读取] 正在从文件 {file_path} 读取内容 (r 模式)...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 方法一：一次性读取所有内容到单个字符串
            # content = f.read()
            # print("--- 文件全部内容 ---")
            # print(content)
            # print("--- 读取结束 ---")

            # 方法二：逐行读取 (更适合大文件)
            print("--- 逐行读取文件内容 ---")
            for line in f: # 文件对象本身是可迭代的，每次迭代返回一行
                print(line.strip()) # strip() 去除行首行尾的空白字符（包括换行符）
            print("--- 读取结束 ---")

            # 注意：文件读取指针已到末尾，如果文件对象还在有效期，再次读取将为空
            # f.seek(0) # 可以将指针移回文件开头
            # content_again = f.read()
            # print(f"再次读取: '{content_again}'")

    except FileNotFoundError:
        print(f"[读取] 错误: 文件 {file_path} 未找到。")
    except IOError as e:
        print(f"[读取] 文件时出错: {e}")

    # --- 3. 追加内容到文件 ('a'模式) ---
    # 'a' 模式 (append) 会在文件末尾追加内容，如果文件不存在，则会创建新文件。
    print(f"\n[追加] 正在向文件 {file_path} 追加内容 (a 模式)...")
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write("这是追加的一行。\n")
            f.write("另一行追加的内容。\n")
        print("[追加] 文件追加成功。")
    except IOError as e:
        print(f"[追加] 文件时出错: {e}")

    # --- 4. 再次读取文件以查看追加结果 ---
    print(f"\n[再次读取] 查看追加后的文件 {file_path} 内容...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content_after_append = f.read()
            print("--- 追加后的文件内容 ---")
            print(content_after_append)
            print("--- 读取结束 ---")
    except FileNotFoundError:
        print(f"[再次读取] 错误: 文件 {file_path} 未找到。")
    except IOError as e:
        print(f"[再次读取] 文件时出错: {e}")

# --- 主程序入口 ---
if __name__ == "__main__":
    demonstrate_file_io()
    print("\n--- 文件操作演示结束 ---")
