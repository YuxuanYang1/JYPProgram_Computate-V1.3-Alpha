#start.py(V1.3-Alpha)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                              QPushButton, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

# 配色
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4fc3f7"
INPUT_BG = "#2a2a2a"
BORDER_COLOR = "#3a3a3a"


class StartWindow(QWidget):
    
    start_game = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计算练习")
        self.resize(500, 450)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                font-family: "Consolas", "Microsoft YaHei";
                font-size: 14px;
            }}
            QLabel#title {{
                font-size: 26px;
                font-weight: bold;
                color: {ACCENT_COLOR};
            }}
            QTextEdit {{
                background-color: {INPUT_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                padding: 10px;
                color: {TEXT_COLOR};
                font-family: "Consolas", "Microsoft YaHei";
                font-size: 15px;
            }}
            QPushButton {{
                background-color: {INPUT_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                padding: 12px;
                color: {TEXT_COLOR};
                font-size: 16px;
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
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)
        
        # 标题
        title = QLabel("计算练习")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        # 滚动公告区域
        self.notice = QTextEdit()
        self.notice.setReadOnly(True)
        self.notice.setFixedHeight(250)
        layout.addWidget(self.notice)
        
        layout.addSpacing(10)
        
        # 开始游戏按钮
        self.btn_start = QPushButton("开 始 练 习")
        self.btn_start.clicked.connect(self.on_start)
        self.btn_start.setDefault(True)
        layout.addWidget(self.btn_start)
        
        self.setLayout(layout)
        
        # 公告内容
        self.notice_lines = [
            "欢迎使用计算练习程序！",
            "",
            "当前版本：V1.3-Alpha",
            "上次更新：2026-10-02",
            "",
            "【功能说明】",
            "· 支持整数加减乘除练习",
            "· 支持混合运算、小数运算",
            "· 支持难度自定义",
            "· 支持计时与统计",
            "· 支持排行榜、历史记录、错题本",
            "",
            "祝您练习愉快！",
            ""
        ]
        
        # 用定时器实现滚动
        self.scroll_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.scroll_notice)
        self.timer.start(800)
    
    def scroll_notice(self):
        """滚动公告：每次显示一部分，循环"""
        display_lines = []
        total = len(self.notice_lines)
        for i in range(min(11, total)):
            idx = (self.scroll_index + i) % total
            display_lines.append(self.notice_lines[idx])
        self.notice.setText("\n".join(display_lines))
        self.scroll_index = (self.scroll_index + 1) % total
    
    def on_start(self):
        """点击开始游戏"""
        self.timer.stop()
        self.start_game.emit()
