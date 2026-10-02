#menu.py(V1.3-Alpha)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTabWidget, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal

import config

# 配色
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4fc3f7"
INPUT_BG = "#2a2a2a"
BORDER_COLOR = "#3a3a3a"


class MenuWindow(QWidget):
    mode_selected = pyqtSignal(str)
    logout = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计算练习")
        self.resize(500, 500)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                font-family: "Consolas", "Microsoft YaHei";
                font-size: 14px;
            }}
            QLabel#title {{
                font-size: 22px;
                font-weight: bold;
                color: {ACCENT_COLOR};
            }}
            QLabel#info {{
                font-size: 13px;
                color: #999999;
            }}
            QTabWidget::pane {{
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                background-color: {BG_COLOR};
            }}
            QTabBar::tab {{
                background-color: {INPUT_BG};
                color: {TEXT_COLOR};
                border: 1px solid {BORDER_COLOR};
                padding: 8px 20px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {ACCENT_COLOR};
                color: {BG_COLOR};
            }}
            QTabBar::tab:hover {{
                border: 1px solid {ACCENT_COLOR};
                color: {ACCENT_COLOR};
            }}
            QPushButton {{
                background-color: {INPUT_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                padding: 12px;
                color: {TEXT_COLOR};
                text-align: left;
                padding-left: 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                border: 1px solid {ACCENT_COLOR};
                color: {ACCENT_COLOR};
            }}
            QPushButton:pressed {{
                background-color: {ACCENT_COLOR};
                color: {BG_COLOR};
            }}
            QPushButton#logout {{
                border: 1px solid #ff6b6b;
                color: #ff6b6b;
                text-align: center;
                padding-left: 12px;
            }}
            QPushButton#logout:hover {{
                background-color: #ff6b6b;
                color: {BG_COLOR};
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)
        
        # 标题
        title = QLabel("计算练习")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 用户信息
        self.label_user = QLabel()
        self.label_user.setObjectName("info")
        self.label_user.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_user)
        
        # Tab 控件
        self.tabs = QTabWidget()
        
        # 整数四则运算 Tab
        self.tab_basic = QWidget()
        basic_layout = QVBoxLayout()
        basic_layout.setSpacing(8)
        basic_layout.setContentsMargins(15, 15, 15, 15)
        
        self.btn_1_1 = QPushButton("1.1  整数加法")
        self.btn_1_2 = QPushButton("1.2  整数减法")
        self.btn_1_3 = QPushButton("1.3  整数乘法")
        self.btn_1_4 = QPushButton("1.4  整数除法")
        
        self.btn_1_1.clicked.connect(lambda: self.mode_selected.emit("1.1"))
        self.btn_1_2.clicked.connect(lambda: self.mode_selected.emit("1.2"))
        self.btn_1_3.clicked.connect(lambda: self.mode_selected.emit("1.3"))
        self.btn_1_4.clicked.connect(lambda: self.mode_selected.emit("1.4"))
        
        for btn in [self.btn_1_1, self.btn_1_2, self.btn_1_3, self.btn_1_4]:
            basic_layout.addWidget(btn)
        basic_layout.addStretch()
        self.tab_basic.setLayout(basic_layout)
        
        # 小学进阶 Tab
        self.tab_advanced = QWidget()
        adv_layout = QVBoxLayout()
        adv_layout.setSpacing(8)
        adv_layout.setContentsMargins(15, 15, 15, 15)
        
        self.btn_2_1 = QPushButton("2.1  混合运算")
        self.btn_2_2 = QPushButton("2.2  小数运算")
        
        self.btn_2_1.clicked.connect(lambda: self.mode_selected.emit("2.1"))
        self.btn_2_2.clicked.connect(lambda: self.mode_selected.emit("2.2"))
        
        for btn in [self.btn_2_1, self.btn_2_2]:
            adv_layout.addWidget(btn)
        adv_layout.addStretch()
        self.tab_advanced.setLayout(adv_layout)
        
        # 统计查看 Tab
        self.tab_stats = QWidget()
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(8)
        stats_layout.setContentsMargins(15, 15, 15, 15)
        
        self.btn_rank = QPushButton("3.1  排行榜")
        self.btn_history = QPushButton("3.2  历史记录")
        self.btn_wrong = QPushButton("3.3  错题本")
        
        self.btn_rank.clicked.connect(lambda: self.mode_selected.emit("3.1"))
        self.btn_history.clicked.connect(lambda: self.mode_selected.emit("3.2"))
        self.btn_wrong.clicked.connect(lambda: self.mode_selected.emit("3.3"))
        
        for btn in [self.btn_rank, self.btn_history, self.btn_wrong]:
            stats_layout.addWidget(btn)
        stats_layout.addStretch()
        self.tab_stats.setLayout(stats_layout)
        
        # 加入 Tab
        self.tabs.addTab(self.tab_basic, "整数四则")
        self.tabs.addTab(self.tab_advanced, "小学进阶")
        self.tabs.addTab(self.tab_stats, "统计")
        
        layout.addWidget(self.tabs)
        
        layout.addSpacing(10)
        
        # 退出登录
        self.btn_logout = QPushButton("退出登录")
        self.btn_logout.setObjectName("logout")
        self.btn_logout.clicked.connect(self.logout.emit)
        layout.addWidget(self.btn_logout)
        
        self.setLayout(layout)
    
    def refresh(self):
        """刷新用户信息显示"""
        user = config.CurrentUser
        if user in config.NameList:
            idx = config.NameList.index(user)
            score = config.ScoreList[idx]
            self.label_user.setText(f"当前用户：{user}    总分：{score}")
        else:
            self.label_user.setText(f"当前用户：{user}")
