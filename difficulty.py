# difficulty.py(V1.3-Alpha)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QLineEdit, QFrame)
from PyQt5.QtCore import Qt

import config

# 配色
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4fc3f7"
INPUT_BG = "#2a2a2a"
BORDER_COLOR = "#3a3a3a"
ERROR_COLOR = "#ff6b6b"


class DifficultyDialog(QDialog):
    
    def __init__(self, order, parent=None):
        super().__init__(parent)
        self.order = order
        self.setWindowTitle("选择难度")
        self.resize(400, 450)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                font-family: "Consolas", "Microsoft YaHei";
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {INPUT_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                padding: 10px;
                color: {TEXT_COLOR};
                text-align: left;
                padding-left: 20px;
            }}
            QPushButton:hover {{
                border: 1px solid {ACCENT_COLOR};
                color: {ACCENT_COLOR};
            }}
            QPushButton:pressed {{
                background-color: {ACCENT_COLOR};
                color: {BG_COLOR};
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
            QLabel {{
                color: {TEXT_COLOR};
            }}
        """)
        
        self.result_range = None
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(8)
        
        title = QLabel("选择难度")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {ACCENT_COLOR};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        # 默认难度档位
        for k, v in config.Difficulty.items():
            btn = QPushButton(f"{k}. {v['name']}（{v['start']}~{v['end']}）")
            btn.clicked.connect(lambda checked, key=k: self.choose_default(key))
            layout.addWidget(btn)
        
        layout.addSpacing(10)
        
        # 自定义
        btn_custom = QPushButton("0. 自定义")
        btn_custom.clicked.connect(self.show_custom)
        layout.addWidget(btn_custom)
        
        # 自定义区域（默认隐藏）
        self.custom_widget = QFrame()
        custom_layout = QVBoxLayout()
        custom_layout.setContentsMargins(0, 0, 0, 0)
        
        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("起始值："))
        self.input_start = QLineEdit()
        range_layout.addWidget(self.input_start)
        range_layout.addWidget(QLabel("末值："))
        self.input_end = QLineEdit()
        range_layout.addWidget(self.input_end)
        custom_layout.addLayout(range_layout)
        
        btn_ok = QPushButton("确定")
        btn_ok.clicked.connect(self.choose_custom)
        custom_layout.addWidget(btn_ok)
        
        self.custom_widget.setLayout(custom_layout)
        self.custom_widget.setVisible(False)
        layout.addWidget(self.custom_widget)
        
        layout.addStretch()

        # 减法选择
        from PyQt5.QtWidgets import QCheckBox
        self.support_negative = False
        if order == "-":
            self.check_negative = QCheckBox("支持负数出现（仅减法）")
            self.check_negative.setStyleSheet(f"color: {TEXT_COLOR};")
            layout.addWidget(self.check_negative)
        
        # 取消
        btn_cancel = QPushButton("取消")
        btn_cancel.clicked.connect(self.reject)
        layout.addWidget(btn_cancel)
        
        self.setLayout(layout)
    
    def choose_default(self, key):
        """选择默认难度"""
        v = config.Difficulty[key]
        self.result_range = (v["start"], v["end"])
        if self.order == "-":
            self.support_negative = self.check_negative.isChecked()
        self.accept()

    def show_custom(self):
        """显示自定义输入"""
        self.custom_widget.setVisible(True)
    
    def choose_custom(self):
        try:
            start = float(self.input_start.text())
            end = float(self.input_end.text())
        except ValueError:
            return
        if end <= start:
            return
        self.result_range = (int(start), int(end))
        if self.order == "-":
            self.support_negative = self.check_negative.isChecked()
        self.accept()
