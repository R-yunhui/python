# -*- coding: utf-8 -*-

class BankAccount:
    """模拟一个简单的银行账户"""

    # 类变量 (Class Variable)，用于生成唯一的账号。
    # 所有 BankAccount 对象共享这一个变量。
    # 通常用下划线开头表示内部使用，但这里为了清晰省略。
    next_account_number = 1001

    def __init__(self, owner_name, initial_balance=0.0):
        """
        构造方法 (Initializer/Constructor)。
        当创建一个新的 BankAccount 对象时自动调用。
        self 参数代表正在创建的对象实例本身。
        """
        print(f"\n正在创建新账户 (持有人: {owner_name}, 初始余额: {initial_balance})...")
        # --- 实例变量 (Instance Variables) ---
        # 每个 BankAccount 对象都有自己的一套实例变量。
        self.owner_name = owner_name # 账户所有者姓名

        # 对初始余额进行简单验证
        # 检查初始余额是否有效
        # 1. 使用 isinstance() 检查 initial_balance 是否为整数或浮点数
        # 2. 检查余额是否大于等于0
        # 3. 如果有效，将余额转换为浮点数并赋值给 self.balance
        # 4. 如果无效，打印警告信息并将余额设置为0.0
        if isinstance(initial_balance, (int, float)) and initial_balance >= 0:
            self.balance = float(initial_balance) # 使用 float 类型存储货币金额
        else:
            print(f"警告：初始余额 '{initial_balance}' 无效，已设置为 0.0。")
            self.balance = 0.0

        # 分配唯一的账号 (使用类变量来生成)
        self.account_number = BankAccount.next_account_number
        # 更新类变量，为下一个账户准备
        BankAccount.next_account_number += 1

        print(f"账户创建成功 - 账号: {self.account_number}, 持有人: {self.owner_name}, 当前余额: {self.balance:.2f}")

    # --- 实例方法 (Instance Methods) ---
    # 操作或访问对象实例数据的函数。第一个参数必须是 self。
    def deposit(self, amount):
        """向账户存款"""
        try:
            # 1. 尝试将存款金额转换为浮点数
            # 2. 如果转换成功，检查金额是否大于0
            # 3. 如果金额大于0，将金额加到余额上
            # 4. 打印成功信息
            # 5. 返回True表示成功
            amount = float(amount) # 尝试转换为浮点数
            if amount > 0:
                self.balance += amount
                print(f"存款成功 [账号:{self.account_number}]: +{amount:.2f}。当前余额: {self.balance:.2f}")
                return True # 表示成功
            else:
                print(f"存款失败 [账号:{self.account_number}]: 存款金额 '{amount}' 必须大于 0。")
                return False # 表示失败
        except ValueError:
            print(f"存款失败 [账号:{self.account_number}]: 输入的金额 '{amount}' 不是有效的数字。")
            return False

    def withdraw(self, amount):
        """从账户取款"""
        try:
            # 1. 尝试将取款金额转换为浮点数
            # 2. 如果转换成功，检查金额是否大于0
            # 3. 如果金额大于0，检查余额是否足够
            # 4. 如果余额足够，从余额中减去取款金额
            # 5. 打印成功信息
            # 6. 返回True表示成功
            amount = float(amount) # 尝试转换为浮点数
            if amount <= 0:
                print(f"取款失败 [账号:{self.account_number}]: 取款金额 '{amount}' 必须大于 0。")
                return False # 表示失败
            elif amount > self.balance:
                print(f"取款失败 [账号:{self.account_number}]: 余额不足。当前余额: {self.balance:.2f}，尝试取款: {amount:.2f}")
                return False # 表示失败
            else:
                self.balance -= amount
                print(f"取款成功 [账号:{self.account_number}]: -{amount:.2f}。当前余额: {self.balance:.2f}")
                return True # 表示成功
        except ValueError:
             print(f"取款失败 [账号:{self.account_number}]: 输入的金额 '{amount}' 不是有效的数字。")
             return False

    def get_balance(self):
        """获取当前账户余额"""
        # 这是一个访问器 (getter) 方法，提供对内部数据的受控访问
        return self.balance

    def display_account_info(self):
        """显示账户详细信息"""
        # 这个方法组合了对象的多个属性进行显示
        print(f"--- 账户信息 [账号:{self.account_number}] ---")
        print(f"持有人: {self.owner_name}")
        print(f"当前余额: {self.get_balance():.2f}") # 调用 get_balance() 获取余额
        print(f"------------------------------")

    # --- 特殊方法 (Dunder methods / Magic methods) ---
    # 以双下划线开头和结尾的方法，Python 在特定操作时会自动调用它们。
    def __str__(self):
        """
        定义当对象被 print() 函数打印，或使用 str() 转换时的字符串表示形式。
        应返回一个用户友好的字符串。
        """
        return f"BankAccount(账号: {self.account_number}, 持有人: {self.owner_name}, 余额: {self.balance:.2f})"

    def __repr__(self):
        """
        定义对象的"官方"字符串表示形式，主要用于调试。
        目标是返回一个清晰、无歧义的字符串，理想情况下可以让开发者重新创建该对象。
        如果 __str__ 未定义，print() 会尝试调用 __repr__。
        """
        return f"BankAccount(owner_name='{self.owner_name}', initial_balance={self.balance})"

# --- 主程序入口：演示如何使用 BankAccount 类 ---
if __name__ == "__main__":
    print("\n--- 面向对象编程 (OOP) 演示 ---")

    # 创建 BankAccount 对象 (实例化类)
    # 这会调用 BankAccount 类的 __init__ 方法
    account1 = BankAccount("张三", 1000.0)
    account2 = BankAccount("李四", "50.5") # 演示字符串余额也可以处理
    account3 = BankAccount("王五", -200) # 测试无效初始余额
    account4 = BankAccount("赵六")      # 测试默认初始余额 (0.0)

    print("\n--- 对账户1进行操作 ---")
    account1.display_account_info()
    account1.deposit(500.25)
    account1.withdraw(200)
    account1.withdraw(2000) # 测试余额不足
    print(f"账户1当前余额 (通过 get_balance): {account1.get_balance():.2f}")
    # 直接打印对象会调用 __str__ 方法
    print("直接打印账户1对象:", account1)
    # 在交互式解释器中直接输入对象名通常会调用 __repr__ 方法
    print("账户1对象的 repr:", repr(account1))


    print("\n--- 对账户2进行操作 ---")
    print("直接打印账户2对象:", account2)
    account2.withdraw("abc") # 测试无效取款金额
    account2.withdraw(60) # 测试余额不足
    account2.deposit(-100) # 测试无效存款
    account2.deposit("1000") # 演示字符串存款也可以处理
    account2.display_account_info()

    print("\n--- 再次查看账户3 和 账户4 ---")
    account3.display_account_info()
    account4.display_account_info()
    account4.deposit(150)

    print("\n--- OOP 演示结束 ---")
