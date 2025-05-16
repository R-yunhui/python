import paramiko
import time
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QMessageBox, QGroupBox)
from PyQt6.QtCore import QThread, pyqtSignal

class UpdateThread(QThread):
    """后台更新线程，用于执行镜像更新操作，避免界面卡死"""
    # 定义信号，用于向主线程发送日志和完成状态
    log_signal = pyqtSignal(str)  # 发送日志信息
    finished_signal = pyqtSignal(bool, str)  # 发送完成状态和消息

    def __init__(self, config):
        super().__init__()
        self.config = config  # 保存配置信息

    def run(self):
        """线程执行的主要逻辑"""
        try:
            # 创建更新器实例
            updater = K8sPodUpdater(
                hostname=self.config["hostname"],
                username=self.config["username"],
                password=self.config["password"],
                port=self.config["port"]
            )
            
            # 连接服务器
            if not updater.connect():
                self.finished_signal.emit(False, "连接服务器失败")
                return

            # 执行镜像更新
            success = updater.update_pod_image(
                self.config["namespace"],
                self.config["deployment_name"],
                self.config["new_image"]
            )
            
            updater.close()
            self.finished_signal.emit(success, "更新完成" if success else "更新失败")
            
        except Exception as e:
            self.finished_signal.emit(False, f"发生错误: {str(e)}")

class K8sPodUpdater:
    """Kubernetes Pod 更新器，负责与服务器交互和更新操作"""
    def __init__(self, hostname, username, password=None, key_filename=None, port=22):
        """初始化更新器
        Args:
            hostname: 服务器地址
            username: SSH用户名
            password: SSH密码
            key_filename: SSH密钥文件路径
            port: SSH端口
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.client = None

    def connect(self):
        """建立SSH连接"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # 根据认证方式选择连接方法
            if self.key_filename:
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    key_filename=self.key_filename
                )
            else:
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password
                )
            print(f"成功连接到服务器 {self.hostname}")
            return True
        except Exception as e:
            print(f"连接失败: {str(e)}")
            return False

    def update_pod_image(self, namespace, deployment_name, new_image):
        """更新Pod的镜像
        Args:
            namespace: 命名空间
            deployment_name: deployment名称
            new_image: 新的镜像地址
        """
        if not self.client:
            print("未连接到服务器")
            return False

        try:
            # 获取deployment中容器的名称
            get_deployment_cmd = f"kubectl get deployment {deployment_name} -n {namespace} -o jsonpath='{{.spec.template.spec.containers[0].name}}'"
            stdin, stdout, stderr = self.client.exec_command(get_deployment_cmd)
            container_name = stdout.read().decode().strip()
            
            if not container_name:
                print(f"无法获取 deployment {deployment_name} 的容器名称")
                return False
            
            print(f"找到容器名称: {container_name}")
            
            # 执行更新镜像的命令
            command = f"kubectl set image deployment/{deployment_name} {container_name}={new_image} -n {namespace}"
            
            stdin, stdout, stderr = self.client.exec_command(command)
            
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            if error:
                print(f"执行出错: {error}")
                return False
            
            print(f"命令执行成功: {output}")
            
            # 等待更新完成
            self._wait_for_deployment_rollout(namespace, deployment_name)
            
            return True
        except Exception as e:
            print(f"更新失败: {str(e)}")
            return False

    def _wait_for_deployment_rollout(self, namespace, deployment_name, timeout=300):
        """等待deployment更新完成
        Args:
            namespace: 命名空间
            deployment_name: deployment名称
            timeout: 超时时间（秒）
        """
        print(f"等待 deployment {deployment_name} 更新完成...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            command = f"kubectl rollout status deployment/{deployment_name} -n {namespace}"
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode()
            
            if "successfully rolled out" in output:
                print(f"Deployment {deployment_name} 更新成功")
                return True
            
            time.sleep(5)
        
        print(f"Deployment {deployment_name} 更新超时")
        return False

    def close(self):
        """关闭SSH连接"""
        if self.client:
            self.client.close()
            print("已关闭连接")

class K8sPodUpdaterGUI(QMainWindow):
    """主窗口类，负责界面显示和用户交互"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("K8s Pod 镜像更新工具")
        self.setMinimumSize(800, 600)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建主布局
        layout = QVBoxLayout(main_widget)
        
        # 创建服务器连接信息组
        server_group = QGroupBox("服务器连接信息")
        server_layout = QVBoxLayout()
        
        # 添加服务器连接信息输入框
        self._create_server_inputs(server_layout)
        
        server_group.setLayout(server_layout)
        layout.addWidget(server_group)
        
        # 创建Kubernetes信息组
        k8s_group = QGroupBox("Kubernetes信息")
        k8s_layout = QVBoxLayout()
        
        # 添加Kubernetes信息输入框
        self._create_k8s_inputs(k8s_layout)
        
        k8s_group.setLayout(k8s_layout)
        layout.addWidget(k8s_group)
        
        # 创建日志输出区域
        self._create_log_area(layout)
        
        # 创建更新按钮
        self._create_update_button(layout)
        
        # 创建状态栏
        self.statusBar().showMessage("就绪")

    def _create_server_inputs(self, layout):
        """创建服务器连接信息输入框"""
        # IP地址
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("服务器IP地址:"))
        self.hostname = QLineEdit()
        ip_layout.addWidget(self.hostname)
        layout.addLayout(ip_layout)
        
        # 端口
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("SSH端口:"))
        self.port = QLineEdit("22")
        port_layout.addWidget(self.port)
        layout.addLayout(port_layout)
        
        # 用户名
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("SSH用户名:"))
        self.username = QLineEdit()
        username_layout.addWidget(self.username)
        layout.addLayout(username_layout)
        
        # 密码
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("SSH密码:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password)
        layout.addLayout(password_layout)

    def _create_k8s_inputs(self, layout):
        """创建Kubernetes信息输入框"""
        # 命名空间
        namespace_layout = QHBoxLayout()
        namespace_layout.addWidget(QLabel("命名空间:"))
        self.namespace = QLineEdit()
        namespace_layout.addWidget(self.namespace)
        layout.addLayout(namespace_layout)
        
        # Deployment名称
        deployment_layout = QHBoxLayout()
        deployment_layout.addWidget(QLabel("Deployment名称:"))
        self.deployment_name = QLineEdit()
        deployment_layout.addWidget(self.deployment_name)
        layout.addLayout(deployment_layout)
        
        # 新镜像地址
        image_layout = QHBoxLayout()
        image_layout.addWidget(QLabel("新镜像地址:"))
        self.new_image = QLineEdit()
        image_layout.addWidget(self.new_image)
        layout.addLayout(image_layout)

    def _create_log_area(self, layout):
        """创建日志输出区域"""
        log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout()
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        log_layout.addWidget(self.log_area)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

    def _create_update_button(self, layout):
        """创建更新按钮"""
        self.update_button = QPushButton("更新镜像")
        self.update_button.clicked.connect(self.update_image)
        layout.addWidget(self.update_button)

    def log(self, message):
        """添加日志到日志区域"""
        self.log_area.append(message)

    def update_image(self):
        """更新镜像的主函数"""
        # 获取输入值
        config = {
            "hostname": self.hostname.text().strip(),
            "port": int(self.port.text().strip() or "22"),
            "username": self.username.text().strip(),
            "password": self.password.text(),
            "namespace": self.namespace.text().strip(),
            "deployment_name": self.deployment_name.text().strip(),
            "new_image": self.new_image.text().strip()
        }
        
        # 验证输入
        if not all([config["hostname"], config["username"], config["password"], 
                   config["namespace"], config["deployment_name"], config["new_image"]]):
            QMessageBox.critical(self, "错误", "请填写所有必填字段")
            return
        
        # 禁用更新按钮
        self.update_button.setEnabled(False)
        self.statusBar().showMessage("正在更新...")
        
        # 创建并启动更新线程
        self.update_thread = UpdateThread(config)
        self.update_thread.log_signal.connect(self.log)
        self.update_thread.finished_signal.connect(self.update_finished)
        self.update_thread.start()

    def update_finished(self, success, message):
        """更新完成后的处理"""
        self.update_button.setEnabled(True)
        self.statusBar().showMessage(message)
        if success:
            QMessageBox.information(self, "成功", "镜像更新成功")
        else:
            QMessageBox.critical(self, "错误", message)

def main():
    """程序入口函数"""
    app = QApplication(sys.argv)
    window = K8sPodUpdaterGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()