import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal

class CmdThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, config_path, namespace):
        super().__init__()
        self.config_path = config_path
        self.namespace = namespace

    def run(self):
        try:
            cmd = f'ktctl connect -c="{self.config_path}" -n={self.namespace}'
            powershell_cmd = [
                "powershell", "-Command",
                f"Start-Process cmd -ArgumentList '/c {cmd}' -Verb RunAs"
            ]
            self.log_signal.emit(f"执行命令：{cmd}\n")
            proc = subprocess.Popen(
                powershell_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # 实时输出日志
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                self.log_signal.emit(line)
            proc.wait()
            if proc.returncode == 0:
                self.finished_signal.emit(True, "命令执行成功")
            else:
                err = proc.stderr.read()
                self.finished_signal.emit(False, f"命令执行失败: {err}")
        except Exception as e:
            self.finished_signal.emit(False, f"发生异常: {str(e)}")

class KtctlGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ktctl 管理员执行工具")
        self.setMinimumSize(600, 400)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # 配置文件选择
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("配置文件:"))
        self.file_edit = QLineEdit()
        file_layout.addWidget(self.file_edit)
        file_btn = QPushButton("选择文件")
        file_btn.clicked.connect(self.choose_file)
        file_layout.addWidget(file_btn)
        layout.addLayout(file_layout)

        # 命名空间输入
        ns_layout = QHBoxLayout()
        ns_layout.addWidget(QLabel("命名空间:"))
        self.ns_edit = QLineEdit()
        ns_layout.addWidget(self.ns_edit)
        layout.addLayout(ns_layout)

        # 执行按钮
        self.run_btn = QPushButton("以管理员权限执行")
        self.run_btn.clicked.connect(self.run_cmd)
        layout.addWidget(self.run_btn)

        # 日志输出
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

    def choose_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "选择配置文件", "", "Config Files (*.yaml *.yml *.json *.*)")
        if file:
            self.file_edit.setText(file)

    def log(self, msg):
        self.log_area.append(msg)

    def run_cmd(self):
        config_path = self.file_edit.text().strip()
        namespace = self.ns_edit.text().strip()
        if not config_path or not namespace:
            QMessageBox.critical(self, "错误", "请填写配置文件和命名空间")
            return
        self.run_btn.setEnabled(False)
        self.log_area.clear()
        self.log(f"准备以管理员权限执行 ktctl connect ...")
        self.thread = CmdThread(config_path, namespace)
        self.thread.log_signal.connect(self.log)
        self.thread.finished_signal.connect(self.on_finished)
        self.thread.start()

    def on_finished(self, success, msg):
        self.run_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, "成功", msg)
        else:
            QMessageBox.critical(self, "失败", msg)
        self.log(msg)

def main():
    app = QApplication(sys.argv)
    window = KtctlGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()