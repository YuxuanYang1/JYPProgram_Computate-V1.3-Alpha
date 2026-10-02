# display.py(V1.3-public)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QTextEdit, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal

import config

# 配色
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4fc3f7"
INPUT_BG = "#2a2a2a"
BORDER_COLOR = "#3a3a3a"


class DisplayWindow(QWidget):
    """通用显示页：排行榜、历史记录、错题本"""
    
    back_to_menu = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("显示")
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                font-family: "Consolas", "Microsoft YaHei";
                font-size: 14px;
            }}
            QLabel#title {{
                font-size: 18px;
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
                font-size: 13px;
            }}
            QPushButton {{
                background-color: {INPUT_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                padding: 8px 16px;
                color: {TEXT_COLOR};
            }}
            QPushButton:hover {{
                border: 1px solid {ACCENT_COLOR};
                color: {ACCENT_COLOR};
            }}
            QPushButton#back {{
                border: 1px solid #ff6b6b;
                color: #ff6b6b;
            }}
            QPushButton#back:hover {{
                background-color: #ff6b6b;
                color: {BG_COLOR};
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)
        
        # 顶部
        top_layout = QHBoxLayout()
        self.label_title = QLabel("显示")
        self.label_title.setObjectName("title")
        top_layout.addWidget(self.label_title)
        top_layout.addStretch()
        self.btn_back = QPushButton("返回")
        self.btn_back.setObjectName("back")
        self.btn_back.clicked.connect(self.back_to_menu.emit)
        top_layout.addWidget(self.btn_back)
        layout.addLayout(top_layout)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {BORDER_COLOR};")
        layout.addWidget(line)
        
        # 内容
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)
        
        self.setLayout(layout)
    
    def show_rank(self):
        """显示排行榜"""
        self.label_title.setText("排行榜")
        if len(config.NameList) == 0:
            self.text_area.setText("暂无用户数据。")
            return
        rank = sorted(zip(config.NameList, config.ScoreList),
                      key=lambda x: x[1], reverse=True)
        lines = []
        for i, (name, score) in enumerate(rank[:20], 1):
            lines.append(f"{i:>2}. {name:<15} {score}分")
        self.text_area.setText("\n".join(lines))
    
    def show_history(self):
        """显示当前用户的历史记录"""
        self.label_title.setText("历史记录")
        user = config.CurrentUser
        if user not in config.HistoryList or not config.HistoryList[user]:
            self.text_area.setText("暂无历史记录。")
            return
        records = config.HistoryList[user]
        lines = []
        total_correct = total_wrong = 0
        total_time = 0
        for i, r in enumerate(records, 1):
            lines.append(
                f"{i:>2}. {r['mode']} | 正确{r['correct']} 错误{r['wrong']} "
                f"| 用时{r['time']:.2f}s | 得分{r['score']}"
            )
            total_correct += r["correct"]
            total_wrong += r["wrong"]
            total_time += r["time"]
        lines.append("")
        lines.append(f"总计：正确{total_correct} 错误{total_wrong} 总用时{total_time:.2f}s")
        self.text_area.setText("\n".join(lines))
    
    def show_wrong(self):
        """显示当前用户的错题本"""
        self.label_title.setText("错题本")
        user = config.CurrentUser
        if user not in config.WrongList or not config.WrongList[user]:
            self.text_area.setText("错题本是空的！")
            return
        records = config.WrongList[user]
        lines = []
        for i, r in enumerate(records, 1):
            lines.append(f"{i:>2}. {r['question']}")
            lines.append(f"    正确答案：{r['correct']}    你的答案：{r['your']}")
        self.text_area.setText("\n".join(lines))
