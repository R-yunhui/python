import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, 
                            QTextEdit, QMessageBox, QCheckBox, QComboBox, QLabel)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

class ChatThread(QThread):  # 继承自QThread类，用于创建后台线程
    """后台聊天线程"""
    response_signal = pyqtSignal(str)  # 发送响应文本
    finished_signal = pyqtSignal(bool, str)  # 发送完成状态和消息

    def __init__(self, llm, prompt_template, question, memory, use_stream=False):
        super().__init__()
        self.llm = llm
        self.prompt_template = prompt_template
        self.question = question
        self.memory = memory
        self.use_stream = use_stream
        self.is_running = True

    def run(self):
        try:
            if self.use_stream:
                # 直接使用模型的流式输出
                messages = self.prompt_template.format_messages(
                    user_input=self.question,
                    chat_history=self.memory.chat_memory.messages
                )
                
                for chunk in self.llm.stream(messages):
                    if not self.is_running:
                        break
                    if hasattr(chunk, 'content'):
                        self.response_signal.emit(chunk.content)
                    elif isinstance(chunk, dict) and 'content' in chunk:
                        self.response_signal.emit(chunk['content'])
                    elif isinstance(chunk, str):
                        self.response_signal.emit(chunk)
                
                # 更新对话历史
                self.memory.chat_memory.add_user_message(self.question)
                self.memory.chat_memory.add_ai_message(chunk.content if hasattr(chunk, 'content') else str(chunk))
            else:
                # 非流式输出使用chain
                chain = LLMChain(
                    llm=self.llm,
                    prompt=self.prompt_template,
                    memory=self.memory,
                    verbose=True
                )
                response = chain.invoke({"user_input": self.question})
                if isinstance(response, dict) and 'text' in response:
                    self.response_signal.emit(response['text'])
                elif hasattr(response, 'content'):
                    self.response_signal.emit(response.content)

            self.finished_signal.emit(True, "对话完成")
        except Exception as e:
            self.finished_signal.emit(False, f"发生错误: {str(e)}")

    def stop(self):
        self.is_running = False

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("本地大模型聊天")
        self.setMinimumSize(800, 600)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建主布局
        layout = QVBoxLayout(main_widget)
        
        # 创建顶部控制区域
        control_layout = QHBoxLayout()
        
        # 模型选择下拉框
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "deepseek-r1",
            "qwen2.5-72b-instruct",
            "qwen-vl-72b",
            "qwen2.5-vl-72b-instruct"
        ])
        self.model_combo.currentTextChanged.connect(self.model_changed)
        control_layout.addWidget(QLabel("选择模型:"))
        control_layout.addWidget(self.model_combo)
        
        # 流式输出选项
        self.stream_checkbox = QCheckBox("流式输出")
        self.stream_checkbox.setChecked(False)
        control_layout.addWidget(self.stream_checkbox)
        
        # 清除历史按钮
        self.clear_button = QPushButton("清除历史")
        self.clear_button.clicked.connect(self.clear_history)
        control_layout.addWidget(self.clear_button)
        
        layout.addLayout(control_layout)
        
        # 创建聊天历史显示区域
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        
        # 输入框
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        # 发送按钮
        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        # 停止按钮
        self.stop_button = QPushButton("停止")
        self.stop_button.clicked.connect(self.stop_chat)
        self.stop_button.setEnabled(False)
        input_layout.addWidget(self.stop_button)
        
        layout.addLayout(input_layout)
        
        # 初始化大模型和对话历史
        self.init_llm()
        
        # 初始化聊天线程
        self.chat_thread = None
        self.is_first_ai_chunk = True

    def init_llm(self):
        """初始化大语言模型和对话历史"""
        self.llm = ChatOpenAI(
            model_name=self.model_combo.currentText(),
            openai_api_base="http://192.168.2.54:9015/v1/",
            openai_api_key="NA",
            temperature=0.7,
            max_tokens=150
        )
        
        # 创建对话历史存储器
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "你是一个知识渊博且乐于助人的AI助手。请用中文回答。请记住之前的对话内容，保持对话的连贯性。"),
            ("human", "{user_input}"),
            ("ai", "{chat_history}")
        ])

    def model_changed(self, model_name):
        """模型改变时的处理"""
        # 清除当前对话历史
        self.clear_history()
        # 重新初始化模型
        self.llm = ChatOpenAI(
            model_name=model_name,
            openai_api_base="http://192.168.2.54:9015/v1/",
            openai_api_key="NA",
            temperature=0.7,
            max_tokens=150
        )
        self.chat_history.append(f"已切换到模型: {model_name}")

    def send_message(self):
        """发送消息"""
        question = self.input_field.text().strip()
        if not question:
            return
            
        # 清空输入框
        self.input_field.clear()
        
        # 显示用户问题
        self.chat_history.append(f"\n用户: {question}")
        
        # 禁用输入和发送按钮
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        self.is_first_ai_chunk = True
        
        # 创建并启动聊天线程
        self.chat_thread = ChatThread(
            self.llm,
            self.prompt_template,
            question + " 请用中文回答，字数控制在150字左右。",
            self.memory,
            self.stream_checkbox.isChecked()
        )
        self.chat_thread.response_signal.connect(self.update_response)
        self.chat_thread.finished_signal.connect(self.chat_finished)
        self.chat_thread.start()

    def update_response(self, text):
        """更新响应文本"""
        if self.stream_checkbox.isChecked():
            cursor = self.chat_history.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            if self.is_first_ai_chunk:
                # 在流式响应的第一块中添加换行符
                # 这确保了AI的响应在用户的消息后从新行开始。
                cursor.insertText("\nAI: " + text)
                self.is_first_ai_chunk = False
            else:
                cursor.insertText(text)
            self.chat_history.setTextCursor(cursor) # 更新小部件的游标
            self.chat_history.ensureCursorVisible() # 滚动以显示新文本
        else:
            # 非流式：'text' 是完整响应。
            # self.chat_history.append 将在需要时在 "AI: " 之前添加换行符，
            # 并确保 "AI: {text}" 独占一行。
            self.chat_history.append(f"AI: {text}")

    def chat_finished(self, success, message):
        """聊天完成后的处理"""
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        if not success:
            QMessageBox.critical(self, "错误", message)
        else:
            self.chat_history.append("\n--- 对话完成 ---")

    def stop_chat(self):
        """停止当前对话"""
        if self.chat_thread and self.chat_thread.isRunning():
            self.chat_thread.stop()
            self.chat_thread.wait()
            self.chat_history.append("\n--- 对话已停止 ---")
            self.chat_finished(True, "对话已停止")

    def clear_history(self):
        """清除对话历史"""
        self.memory.clear()
        self.chat_history.clear()
        self.chat_history.append("--- 对话历史已清除 ---")

def main():
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()