import sys
import paramiko
import json # 添加json模块导入
# 移除了未使用的 re 模块导入
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTextEdit, QMessageBox, QGroupBox, QComboBox,
                             QTabWidget) # 确保 QTabWidget 也已导入
from PyQt6.QtCore import QThread, pyqtSignal

class ServerResourceMonitor:
    """处理SSH连接并获取服务器资源信息。"""
    def __init__(self, hostname, username, password=None, port=22, key_filename=None):
        """初始化服务器资源监视器。

        Args:
            hostname (str): 服务器的主机名或IP地址。
            username (str): SSH登录用户名。
            password (str, optional): SSH登录密码。默认为None。
            port (int, optional): SSH端口。默认为22。
            key_filename (str, optional): SSH私钥文件路径。默认为None。
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename  # SSH密钥文件，暂未在UI中实现输入
        self.client = None  # paramiko SSH客户端实例

    def connect(self):
        """建立到服务器的SSH连接。"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # 自动添加主机密钥
            if self.key_filename:
                # 使用密钥文件进行连接
                self.client.connect(hostname=self.hostname, port=self.port,
                                    username=self.username, key_filename=self.key_filename)
            else:
                # 使用密码进行连接
                self.client.connect(hostname=self.hostname, port=self.port,
                                    username=self.username, password=self.password)
            return True, "成功连接到服务器。"
        except Exception as e:
            self.client = None # 连接失败时重置客户端
            return False, f"连接失败: {str(e)}"

    def _execute_command(self, command):
        """在远程服务器上执行命令。

        Args:
            command (str): 要执行的命令字符串。

        Returns:
            tuple: (str or None, str or None) 第一个元素是命令的标准输出，第二个是错误信息。
                   如果命令执行成功但有非致命的stderr输出（如tty警告），错误信息可能为None。
        """
        if not self.client:
            return None, "未连接到服务器。"
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode().strip()  # 读取并解码标准输出
            error = stderr.read().decode().strip()   # 读取并解码标准错误
            if error:
                # 忽略一些常见的非致命错误信息，这些信息通常不影响命令结果的获取
                if "stdin: is not a tty" not in error and \
                   "TERM environment variable not set" not in error and \
                   "TERM setting 'dumb' is not supported" not in error: # 添加了对'dumb'终端错误的处理
                    return None, error # 返回真正的错误信息
            return output, None # 如果只有非致命错误，视作成功
        except Exception as e:
            return None, f"命令执行失败: {str(e)}"

    def get_cpu_usage(self):
        """获取CPU使用率。"""
        # vmstat的输出中，第15列是空闲CPU百分比，因此 100 - 空闲百分比 = CPU使用率。
        # vmstat 1 2 表示每秒采样一次，共采样两次，取第二次的稳定数据。
        output, err = self._execute_command("vmstat 1 2 | tail -1 | awk '{print 100 - $15}'")
        if err:
            return f"CPU错误: {err}"
        if output:
            return f"CPU使用率: {output}%"
        return "CPU使用率: 不可用"
    
    def get_memory_usage(self):
        """获取内存使用情况。"""
        # free -m 以MB为单位显示内存信息。
        # awk 用于格式化输出：已用MB / 总计MB (百分比%)
        # 修正 awk 命令中的引号问题
        command = "free -m | grep Mem | awk '{printf \"%s MB / %s MB (%.1f%%)\", $3, $2, $3/$2*100}'"
        output, err = self._execute_command(command)
        if err:
            return f"内存错误: {err}"
        if output:
            return f"内存: {output}"
        return "内存: 不可用"

    def get_disk_usage(self):
        """获取磁盘使用情况（/ 和 /home，如果存在）。"""
        lines = []
        # 获取根文件系统 (/) 的使用情况
        # df -hP 使用易读格式并按POSIX标准输出，tail -n1取最后一行（数据行），awk格式化
        output_root, err_root = self._execute_command("df -hP / | tail -n1 | awk '{print $5 \" 已用 \" $2 \" 总计 在 \" $1 \" (\" $4 \" 可用)\"}'")
        if err_root:
            lines.append(f"磁盘 (/): 错误: {err_root}")
        elif output_root:
            lines.append(f"磁盘 (/): {output_root}")
        else:
            lines.append("磁盘 (/): 不可用")

        # 检查 /home 是否为独立挂载点
        # 通过比较 / 和 /home 的挂载点名称来判断
        output_root_mount_point, _ = self._execute_command("df -P / | awk 'NR==2{print $6}'")
        output_home_mount_point, _ = self._execute_command("df -P /home | awk 'NR==2{print $6}'")

        # 如果 /home 存在且其挂载点与 / 不同，则获取 /home 的使用情况
        if output_root_mount_point and output_home_mount_point and output_root_mount_point != output_home_mount_point:
            output_home, err_home = self._execute_command("df -hP /home | tail -n1 | awk '{print $5 \" 已用 \" $2 \" 总计 在 \" $1 \" (\" $4 \" 可用)\"}'")
            if err_home:
                lines.append(f"磁盘 (/home): 错误: {err_home}")
            elif output_home:
                lines.append(f"磁盘 (/home): {output_home}")
            else:
                lines.append("磁盘 (/home): 不可用")
        
        return "\n".join(lines)


    def get_load_average(self):
        """获取系统平均负载。"""
        # uptime 命令输出中包含负载信息，awk用于提取，sed去除前导空格
        output, err = self._execute_command("uptime | awk -F'load average:' '{print $2}' | sed 's/^ *//'")
        if err:
            return f"平均负载错误: {err}"
        if output:
            return f"平均负载: {output}"
        return "平均负载: 不可用"

    def get_uptime(self):
        """获取服务器运行时间。"""
        # uptime -p 提供易读的运行时间格式 (例如 "up 2 days, 3 hours, 4 minutes")
        output, err = self._execute_command("uptime -p") 
        if err or not output: # 如果 uptime -p 失败或无输出，尝试备用命令
             # 备用命令，尝试从标准 uptime 输出中提取运行时间
             output_s, err_s = self._execute_command("uptime | awk -F'(up | days?,| users?,| load average:)' '{for(i=1;i<=NF;i++) if ($i ~ /min/) {print $i \" minutes\"; break} else if ($i ~ /day/) {print $i \" days, \" $(i+1); break} else if ($i ~ /user/) {print $(i-2) \" \" $(i-1); break} else {print $i}}' | head -n1 | sed 's/^ *//; s/, *$/ /'")
             if err_s:
                 return f"运行时间错误: {err_s}"
             if output_s: # 检查备用命令是否有输出
                 return f"运行时间: {output_s.strip()}"
        if output: # 如果 uptime -p 成功
            return f"{output.replace('up ', '运行时间: ')}"
        return "运行时间: 不可用"

    def get_pod_info(self, namespace, pod_name_filter):
        """获取指定命名空间中Pod的信息，包括节点名称和节点IP，并显示所有镜像。"""
        if not self.client:
            return "未连接到服务器。"
        
        command = f"kubectl get pods -n {namespace} -o json"
        # print(f"DEBUG: Executing Kubernetes command: '{command}' with pod_name_filter: '{pod_name_filter}'")
        output, err = self._execute_command(command)

        if err:
            if "command not found" in err.lower() or "not found" in err.lower() or "不存在" in err:
                 return f"获取Pod信息错误: {err}. 请确保 kubectl 已在服务器上安装并配置在PATH中。"
            return f"获取Pod信息错误: {err}"
        if not output:
            check_ns_cmd = f"kubectl get ns {namespace} --no-headers"
            ns_out, ns_err = self._execute_command(check_ns_cmd)
            if ns_err or not ns_out:
                return f"无法确认命名空间 '{namespace}' 是否存在，或kubectl没有输出。"
            return f"在命名空间 '{namespace}' 中未找到Pod，或者kubectl没有输出。"

        try:
            pod_data = json.loads(output)
            
            pods_to_process = []
            node_names = set() 

            items = pod_data.get("items")
            if items is None and not pod_data: 
                 return f"命名空间 '{namespace}' 可能不存在或您没有权限访问。"
            if not isinstance(items, list): 
                 return f"获取Pod信息时返回了意外的数据结构 (items不是列表)。"
            if not items: 
                return f"命名空间 '{namespace}' 中没有Pod。"

            for item in items:
                pod_name = item.get("metadata", {}).get("name", "N/A")
                
                # Pod 名称筛选 (如果提供了过滤器)
                if pod_name_filter and (pod_name_filter.lower() not in pod_name.lower()):
                    continue

                status = item.get("status", {}).get("phase", "N/A")
                node_name = item.get("spec", {}).get("nodeName", "N/A")
                if node_name != "N/A":
                    node_names.add(node_name)

                all_images = []
                for container in item.get("spec", {}).get("containers", []): 
                    all_images.append(container.get("image", ""))
                for init_container in item.get("spec", {}).get("initContainers", []): 
                    all_images.append(init_container.get("image", ""))
                
                # 不需要再特别筛选java_images，直接将收集到的信息加入
                pods_to_process.append({
                    "name": pod_name,
                    "status": status,
                    "node_name": node_name,
                    "images": all_images, # 保留所有镜像信息
                })

            if not pods_to_process: # 如果经过名称过滤后没有Pod了
                if pod_name_filter:
                    return f"在命名空间 '{namespace}' 中，名称包含 '{pod_name_filter}' 的Pod未找到。"
                else: # 如果没有名称过滤器，但列表仍为空，说明命名空间本身可能就没有Pod
                    return f"在命名空间 '{namespace}' 中未找到任何Pod。"


            node_ip_map = {}
            if node_names: 
                # print(f"DEBUG: Fetching IP info for nodes: {list(node_names)}")
                for n_name in node_names:
                    node_command = f"kubectl get node {n_name} -o json"
                    # print(f"DEBUG: Executing node command: '{node_command}'")
                    node_output, node_err = self._execute_command(node_command)
                    if node_err:
                        print(f"警告: 获取节点 '{n_name}' 信息失败: {node_err}")
                        node_ip_map[n_name] = "IP获取失败"
                        continue
                    if not node_output:
                        print(f"警告: 节点 '{n_name}' 未返回信息。")
                        node_ip_map[n_name] = "IP信息为空"
                        continue
                    
                    try:
                        node_json = json.loads(node_output)
                        ip_address = "N/A"
                        for addr in node_json.get("status", {}).get("addresses", []):
                            if addr.get("type") == "InternalIP":
                                ip_address = addr.get("address", "N/A")
                                break
                        if ip_address == "N/A": 
                             for addr in node_json.get("status", {}).get("addresses", []):
                                if addr.get("type") == "ExternalIP":
                                    ip_address = addr.get("address", "N/A")
                                    break
                        node_ip_map[n_name] = ip_address
                    except json.JSONDecodeError:
                        print(f"警告: 解析节点 '{n_name}' JSON失败。")
                        node_ip_map[n_name] = "IP解析失败"
                    except Exception as e_node:
                        print(f"警告: 处理节点 '{n_name}' 信息时发生错误: {str(e_node)}")
                        node_ip_map[n_name] = "IP处理错误"

            pod_details = []
            for pod_info in pods_to_process:
                node_ip = node_ip_map.get(pod_info["node_name"], "IP未知") if pod_info["node_name"] != "N/A" else "N/A"
                # 显示所有镜像
                images_str = ", ".join(pod_info['images']) if pod_info['images'] else "无" # 使用 'images' 键
                detail = (f"Pod: {pod_info['name']}\n"
                          f"  状态: {pod_info['status']}\n"
                          f"  镜像: {images_str}\n"  # 修改这里以显示所有镜像
                          f"  节点: {pod_info['node_name']}\n"
                          f"  节点IP: {node_ip}")
                pod_details.append(detail)
            
            if not pod_details: 
                 return f"在命名空间 '{namespace}' 中未找到符合条件的Pod（内部逻辑问题）。" 
                 
            return "\n---\n".join(pod_details)

        except json.JSONDecodeError:
            return f"解析Pod列表JSON失败 (非JSON输出): {output[:200]}... 请确保kubectl已正确配置并有权限。"
        except Exception as e: 
            import traceback 
            print(f"DEBUG: Unexpected error in get_pod_info: {str(e)}")
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            return f"处理Pod信息时发生意外错误: {str(e)}"

    def get_all_resources(self):
        """获取所有资源信息。"""
        if not self.client:
            return "未连接。请先连接服务器。"

        resources = [
            f"服务器: {self.hostname}:{self.port}",
            "---------------------------------",
            self.get_uptime(),
            self.get_cpu_usage(),
            self.get_memory_usage(),
            self.get_disk_usage(),
            self.get_load_average(),
            "---------------------------------"
        ]
        return "\n".join(resources)

    def close(self):
        """关闭SSH连接。"""
        if self.client:
            self.client.close()
            self.client = None
            print("连接已关闭。")


class MonitorThread(QThread):
    """运行资源监控的线程，以防止UI冻结。"""
    finished = pyqtSignal(str)  # 用于发射结果或错误的信号

    def __init__(self, monitor_instance, action, namespace=None, pod_name_filter=None):
        super().__init__()
        self.monitor = monitor_instance # ServerResourceMonitor 的实例
        self.action = action 
        self.namespace = namespace
        self.pod_name_filter = pod_name_filter

    def run(self):
        """线程的主要逻辑。"""
        # 首先尝试连接
        connected, msg = self.monitor.connect()
        if not connected:
            self.finished.emit(msg) # 发射连接失败的消息
            return

        # 发射正在获取数据的消息，给用户即时反馈
        self.finished.emit(f"已连接到 {self.monitor.hostname}。正在获取资源数据...") 
        
        result_data = ""
        if self.action == "get_resources":
            result_data = self.monitor.get_all_resources()
        elif self.action == "get_pod_info":
            if not self.namespace: # Namespace是必填的
                self.finished.emit("错误: 请提供Kubernetes命名空间。")
                self.monitor.close()
                return
            # pod_name_filter 可以为空字符串 (如果用户未输入，则传递空字符串)
            result_data = self.monitor.get_pod_info(self.namespace, self.pod_name_filter or "")
        else:
            result_data = "错误: 未知的操作。"

        self.monitor.close() # 关闭连接
        self.finished.emit(result_data) # 发射最终的资源数据


class ServerMonitorGUI(QMainWindow):
    """服务器资源监视器的主GUI窗口。"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("服务器资源监视器")
        self.setMinimumSize(600, 600) # 调整窗口大小以适应新UI元素

        self.monitor_thread = None # 用于管理监控线程
        self.current_action_button = None # 用于跟踪当前哪个按钮触发了操作

        # 预设服务器信息
        self.presets = [
            {"name": "选择预设服务器...", "hostname": "192.168.2.36", "port": "3622", "username": "root", "password": "kl123.A"},
            {"name": "36服务器", "hostname": "192.168.2.36", "port": "3622", "username": "root", "password": "kl123.A"},
            # 您可以在这里添加更多预设
        ]

        # 主窗口部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # 服务器连接信息组
        server_group = QGroupBox("服务器连接信息")
        server_layout = QVBoxLayout()
        self._create_server_inputs(server_layout) # 调用辅助方法创建输入字段
        server_group.setLayout(server_layout)
        layout.addWidget(server_group)

        # Tab Widget for Actions
        self.action_tabs = QTabWidget()
        layout.addWidget(self.action_tabs)

        # Tab 1: Server Resources
        resource_tab = QWidget()
        resource_tab_layout = QVBoxLayout(resource_tab)
        self.fetch_resources_button = QPushButton("获取服务器资源")
        self.fetch_resources_button.clicked.connect(self.start_fetch_resources)
        resource_tab_layout.addWidget(self.fetch_resources_button)
        self.action_tabs.addTab(resource_tab, "服务器资源")

        # Tab 2: Kubernetes Pod Info
        pod_tab = QWidget()
        pod_tab_layout = QVBoxLayout(pod_tab)

        ns_layout = QHBoxLayout()
        ns_layout.addWidget(QLabel("命名空间(Namespace):"))
        self.namespace_input = QLineEdit()
        self.namespace_input.setPlaceholderText("例如: default (必填)")
        ns_layout.addWidget(self.namespace_input)
        pod_tab_layout.addLayout(ns_layout)

        pod_filter_layout = QHBoxLayout()
        pod_filter_layout.addWidget(QLabel("Pod名称包含:"))
        self.pod_name_filter_input = QLineEdit()
        self.pod_name_filter_input.setPlaceholderText("可选，留空则匹配所有 Pod")
        pod_filter_layout.addWidget(self.pod_name_filter_input)
        pod_tab_layout.addLayout(pod_filter_layout)

        self.fetch_pod_info_button = QPushButton("获取Pod信息")
        self.fetch_pod_info_button.clicked.connect(self.start_fetch_pod_info)
        pod_tab_layout.addWidget(self.fetch_pod_info_button)
        self.action_tabs.addTab(pod_tab, "K8s Pod信息")
        
        results_group = QGroupBox("结果信息")
        results_layout = QVBoxLayout()
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True) # 设置为只读
        results_layout.addWidget(self.results_display)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        # 状态栏
        self.statusBar().showMessage("就绪。请输入服务器详细信息并选择操作。")

    def _create_server_inputs(self, server_layout):
        """创建服务器连接相关的输入字段。"""
        # 预设服务器选择
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("预设服务器:"))
        self.preset_combo = QComboBox()
        for preset in self.presets:
            self.preset_combo.addItem(preset["name"])
        self.preset_combo.currentIndexChanged.connect(self.on_preset_selected)
        preset_layout.addWidget(self.preset_combo)
        server_layout.addLayout(preset_layout)

        # 主机名/IP输入
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("主机名/IP:"))
        self.hostname_input = QLineEdit()
        host_layout.addWidget(self.hostname_input)
        server_layout.addLayout(host_layout)

        # 端口输入
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("端口:"))
        self.port_input = QLineEdit("22") # 默认端口为22
        port_layout.addWidget(self.port_input)
        server_layout.addLayout(port_layout)

        # 用户名输入
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("用户名:"))
        self.username_input = QLineEdit()
        user_layout.addWidget(self.username_input)
        server_layout.addLayout(user_layout)

        # 密码输入
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel("密码:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password) # 密码掩码显示
        pass_layout.addWidget(self.password_input)
        server_layout.addLayout(pass_layout)

    def on_preset_selected(self, index):
        """当用户从下拉框中选择预设服务器时调用。"""
        if index > 0: # 第一个项目是提示信息，跳过
            selected_preset = self.presets[index]
            self.hostname_input.setText(selected_preset["hostname"])
            self.port_input.setText(selected_preset["port"])
            self.username_input.setText(selected_preset["username"])
            self.password_input.setText(selected_preset["password"])
            self.statusBar().showMessage(f"已加载预设: {selected_preset['name']}")
        elif index == 0 : # 如果用户选择 "选择预设服务器..."
            self.hostname_input.clear()
            self.port_input.setText("22") # 重置为默认端口
            self.username_input.clear()
            self.password_input.clear()
            self.statusBar().showMessage("请选择一个预设或手动输入服务器信息。")

    def _validate_common_inputs(self):
        """验证通用的服务器连接输入。返回 (hostname, port, username, password) 或 None。"""
        hostname = self.hostname_input.text().strip()
        port_str = self.port_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not hostname or not username:
            QMessageBox.warning(self, "输入错误", "主机名和用户名是必填项。")
            return None
        try:
            port = int(port_str)
            if not (0 < port < 65536):
                raise ValueError("端口超出范围")
        except ValueError:
            QMessageBox.warning(self, "输入错误", "无效的端口号。")
            return None
        return hostname, port, username, password

    def _start_monitor_task(self, action, monitor_args, button_to_disable):
        """通用任务启动逻辑。"""
        common_inputs = self._validate_common_inputs()
        if not common_inputs:
            return

        hostname, port, username, password = common_inputs

        if self.monitor_thread and self.monitor_thread.isRunning():
            QMessageBox.information(self, "繁忙", "一个任务已在进行中，请稍候。")
            return

        self.results_display.setText(f"准备连接到 {hostname}...")
        # 禁用所有操作按钮
        self.fetch_resources_button.setEnabled(False)
        self.fetch_pod_info_button.setEnabled(False)
        self.current_action_button = button_to_disable # 记录当前操作按钮
        self.statusBar().showMessage(f"尝试连接到 {hostname}...")

        monitor = ServerResourceMonitor(hostname, username, password, port)
        
        thread_args = {
            "monitor_instance": monitor,
            "action": action,
        }
        thread_args.update(monitor_args) # 合并特定操作的参数

        self.monitor_thread = MonitorThread(**thread_args)
        self.monitor_thread.finished.connect(self.on_fetch_completed)
        self.monitor_thread.start()

    def start_fetch_resources(self):
        """处理"获取服务器资源"按钮点击事件。"""
        self._start_monitor_task(
            action="get_resources",
            monitor_args={},
            button_to_disable=self.fetch_resources_button
        )

    def start_fetch_pod_info(self):
        """处理"获取Pod信息"按钮点击事件。"""
        namespace = self.namespace_input.text().strip()
        if not namespace:
            QMessageBox.warning(self, "输入错误", "Kubernetes命名空间是必填项。")
            return
        
        pod_name_filter_value = self.pod_name_filter_input.text().strip()
        print(f"DEBUG: pod_name_filter_input read as: '{pod_name_filter_value}'")
        
        self._start_monitor_task(
            action="get_pod_info",
            monitor_args={"namespace": namespace, "pod_name_filter": pod_name_filter_value},
            button_to_disable=self.fetch_pod_info_button
        )

    def on_fetch_completed(self, result_text):
        """监控线程完成时的槽函数。"""
        self.results_display.setText(result_text)
        # 重新启用所有操作按钮
        self.fetch_resources_button.setEnabled(True)
        self.fetch_pod_info_button.setEnabled(True)
        self.current_action_button = None # 清除当前操作按钮记录
        
        if "连接失败" in result_text:
            self.statusBar().showMessage("连接失败。请检查服务器详情或服务器状态。")
        elif "错误" in result_text.lower() or "error" in result_text.lower() or "失败" in result_text :
             self.statusBar().showMessage("任务完成，但有错误发生。请检查结果。")
        else:
            self.statusBar().showMessage("任务成功完成。")


def main():
    """主函数，应用程序入口点。"""
    app = QApplication(sys.argv)
    window = ServerMonitorGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()