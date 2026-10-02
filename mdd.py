# mdd.py(V1.3-Alpha)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QRadioButton,
                             QButtonGroup, QCheckBox)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# 配色
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4fc3f7"
INPUT_BG = "#2a2a2a"
BORDER_COLOR = "#3a3a3a"


class MixedDialog(QDialog):
    """混合运算设置对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("混合运算设置")
        self.resize(400, 320)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                font-family: "Consolas", "Microsoft YaHei";
                font-size: 14px;
            }}
            QLabel#title {{
                font-size: 16px;
                font-weight: bold;
                color: {ACCENT_COLOR};
            }}
            QLabel#section {{
                font-size: 13px;
                color: #999999;
                margin-top: 8px;
            }}
            QRadioButton {{
                color: {TEXT_COLOR};
                padding: 6px;
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

        self.result_difficulty = 1

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        # 标题
        title = QLabel("混合运算设置")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 难度
        label_diff = QLabel("难度")
        label_diff.setObjectName("section")
        layout.addWidget(label_diff)

        self.diff_group = QButtonGroup()
        self.radio_easy = QRadioButton("简单（2个运算符，不含括号）")
        self.radio_mid = QRadioButton("中等（2个运算符，含括号）")
        self.radio_hard = QRadioButton("困难（3个运算符，含括号）")
        self.radio_easy.setChecked(True)
        self.diff_group.addButton(self.radio_easy, 1)
        self.diff_group.addButton(self.radio_mid, 2)
        self.diff_group.addButton(self.radio_hard, 3)
        layout.addWidget(self.radio_easy)
        layout.addWidget(self.radio_mid)
        layout.addWidget(self.radio_hard)

        self.check_div = QCheckBox("包含除法")
        self.check_div.setStyleSheet(f"color: {TEXT_COLOR};")
        layout.addWidget(self.check_div)
        self.check_neg = QCheckBox("允许负数结果")
        self.check_neg.setStyleSheet(f"color: {TEXT_COLOR};")
        layout.addWidget(self.check_neg)

        layout.addStretch()

        # 按钮
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("确定")
        btn_ok.clicked.connect(self.on_ok)
        btn_cancel = QPushButton("取消")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def on_ok(self):
        self.result_difficulty = self.diff_group.checkedId()
        self.result_include_div = self.check_div.isChecked()
        self.result_allow_neg = self.check_neg.isChecked()
        self.accept()
        return
