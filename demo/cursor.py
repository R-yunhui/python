import subprocess
import time
import pyautogui

email = "sddie3zsdsf5"

def run_cursor_installation():
    try:
        # 使用PowerShell执行命令
        powershell_command = 'irm https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.ps1 | iex'
        process = subprocess.Popen(
            ['powershell', '-Command', powershell_command],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 等待一段时间确保窗口已打开
        time.sleep(5)
        # 等待提示出现
        print("等待输入提示...")
        while True:
            output = process.stdout.readline()
            if output:  # 检查是否有输出
                print(f"输出: {output.strip()}")
            if "any key to exit" in output:
                # 输入选项2
                print("检测到输入提示，输入选项2...")
                pyautogui.typewrite('2\n')
                break
        
        time.sleep(5)
        pyautogui.typewrite(f'{email}{int(time.time())}@2925.com\n')

        # 等待进程完成
        stdout, stderr = process.communicate()

        # 打印输出结果
        print("执行结果:")
        print(stdout)
        if stderr:
            print("错误信息:")
            print(stderr)

    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    run_cursor_installation()
