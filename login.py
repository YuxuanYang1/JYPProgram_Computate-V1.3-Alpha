# login.py(V1.3-public)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal

import config
from data import save_data
import hashlib

# 配色
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4fc3f7"
INPUT_BG = "#2a2a2a"
BORDER_COLOR = "#3a3a3a"
ERROR_COLOR = "#ff6b6b"


class LoginWindow(QWidget):
    # 登录成功信号，传递用户名
    login_success = pyqtSignal(str)
    admin_success = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计算练习")
        self.resize(400, 320)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                font-family: "Consolas", "Microsoft YaHei";
                font-size: 14px;
            }}
            QLineEdit {{
                background-color: {INPUT_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                padding: 6px;
                color: {TEXT_COLOR};
            }}
            QLineEdit:focus {{
                border: 1px solid {ACCENT_COLOR};
            }}
            QPushButton {{
                background-color: {INPUT_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                padding: 8px;
                color: {TEXT_COLOR};
            }}
            QPushButton:hover {{
                border: 1px solid {ACCENT_COLOR};
                color: {ACCENT_COLOR};
            }}
            QPushButton:pressed {{
                background-color: {ACCENT_COLOR};
                color: {BG_COLOR};
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)
        
        title = QLabel("计算练习")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {ACCENT_COLOR};")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # 账号
        name_layout = QHBoxLayout()
        name_label = QLabel("账号")
        name_label.setFixedWidth(50)
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("请输入账号名")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.input_name)
        layout.addLayout(name_layout)
        
        # 密码
        key_layout = QHBoxLayout()
        key_label = QLabel("密码")
        key_label.setFixedWidth(50)
        self.input_key = QLineEdit()
        self.input_key.setPlaceholderText("请输入密码")
        self.input_key.setEchoMode(QLineEdit.Password)
        key_layout.addWidget(key_label)
        key_layout.addWidget(self.input_key)
        layout.addLayout(key_layout)
        
        layout.addSpacing(10)
        
        # 按钮
        btn_layout = QHBoxLayout()
        self.btn_login = QPushButton("登 录")
        self.btn_login.clicked.connect(self.on_login)
        self.btn_register = QPushButton("注 册")
        self.btn_register.clicked.connect(self.on_register)
        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_register)
        layout.addLayout(btn_layout)

        # 回车键支持
        self.input_name.returnPressed.connect(self.input_key.setFocus)  # 账号框 → 密码框
        self.input_key.returnPressed.connect(self.on_login)              # 密码框 → 登录
        self.btn_login.setDefault(True)                                   # 默认按钮
        
        # 状态提示
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet(f"color: {ERROR_COLOR}; font-size: 12px;")
        layout.addWidget(self.status)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def on_login(self):
        """登录"""
        name = self.input_name.text().strip()
        key = self.input_key.text()
        
        if not name or not key:
            self.status.setText("账号和密码不能为空")
            return
        
        # 管理员入口
        if name == "admin":
            key_hash = hashlib.sha256(key.encode()).hexdigest()
            if key_hash == config.ADMIN_KEY_HASH:
                self.admin_success.emit()  # ← 发管理员信号
            else:
                self.status.setText("管理员密码不正确")
            return
        
        # 检查账号是否存在
        if name not in config.NameList:
            self.status.setText("账号不存在，请先注册")
            return
        
        # 检查密码
        idx = config.NameList.index(name)
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        if key_hash != config.KeyList[idx]:
            self.status.setText("密码不正确")
            return
        
        # 登录成功
        config.CurrentUser = name
        self.status.setStyleSheet(f"color: {ACCENT_COLOR}; font-size: 12px;")
        self.status.setText(f"欢迎回来，{name}")
        self.login_success.emit(name)
    
    def on_register(self):
        """注册"""
        name = self.input_name.text().strip()
        key = self.input_key.text()
        
        if not name or not key:
            self.status.setText("账号和密码不能为空")
            return
        
        if name in config.NameList:
            self.status.setText("账号已存在，请直接登录")
            return
        
        if not (4 <= len(key) <= 10):
            self.status.setText("密码长度必须为 4-10 字符")
            return
        
        # 注册
        config.NameList.append(name)
        config.KeyList.append(hashlib.sha256(key.encode()).hexdigest())
        config.ScoreList.append(0)
        save_data()
        
        self.status.setStyleSheet(f"color: {ACCENT_COLOR}; font-size: 12px;")
        self.status.setText(f"注册成功，请登录")
