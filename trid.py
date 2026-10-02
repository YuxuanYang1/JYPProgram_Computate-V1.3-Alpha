# trid.py(V1.3-Alpha)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QRadioButton,
                             QButtonGroup, QLineEdit)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# 配色
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4fc3f7"
INPUT_BG = "#2a2a2a"
BORDER_COLOR = "#3a3a3a"


class DecimalDialog(QDialog):
    """小数运算设置对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("小数运算设置")
        self.resize(380, 420)
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
                padding: 4px;
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
            QLineEdit:disabled {{
                background-color: #1a1a1a;
                color: #555555;
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

        self.result_data = None  # (order, decimals, start, end)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        # 标题
        title = QLabel("小数运算设置")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 运算类型
        label_op = QLabel("运算类型")
        label_op.setObjectName("section")
        layout.addWidget(label_op)

        op_layout = QHBoxLayout()
        self.op_group = QButtonGroup()
        self.radio_add = QRadioButton("加法")
        self.radio_sub = QRadioButton("减法")
        self.radio_mul = QRadioButton("乘法")
        self.radio_div = QRadioButton("除法")
        self.radio_add.setChecked(True)
        self.op_group.addButton(self.radio_add, 0)
        self.op_group.addButton(self.radio_sub, 1)
        self.op_group.addButton(self.radio_mul, 2)
        self.op_group.addButton(self.radio_div, 3)
        op_layout.addWidget(self.radio_add)
        op_layout.addWidget(self.radio_sub)
        op_layout.addWidget(self.radio_mul)
        op_layout.addWidget(self.radio_div)
        layout.addLayout(op_layout)

        # 难度
        label_diff = QLabel("难度")
        label_diff.setObjectName("section")
        layout.addWidget(label_diff)

        diff_layout = QVBoxLayout()
        self.diff_group = QButtonGroup()
        self.radio_easy = QRadioButton("简单（1~10，1位小数）")
        self.radio_mid = QRadioButton("中等（1~100，2位小数）")
        self.radio_hard = QRadioButton("困难（1~1000，3位小数）")
        self.radio_custom = QRadioButton("自定义")
        self.radio_easy.setChecked(True)
        self.diff_group.addButton(self.radio_easy, 0)
        self.diff_group.addButton(self.radio_mid, 1)
        self.diff_group.addButton(self.radio_hard, 2)
        self.diff_group.addButton(self.radio_custom, 3)
        diff_layout.addWidget(self.radio_easy)
        diff_layout.addWidget(self.radio_mid)
        diff_layout.addWidget(self.radio_hard)
        diff_layout.addWidget(self.radio_custom)
        layout.addLayout(diff_layout)

        # 自定义范围（默认禁用）
        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("起始值："))
        self.input_start = QLineEdit("1")
        self.input_start.setFixedWidth(80)
        self.input_start.setEnabled(False)
        range_layout.addWidget(self.input_start)
        range_layout.addWidget(QLabel("末值："))
        self.input_end = QLineEdit("10")
        self.input_end.setFixedWidth(80)
        self.input_end.setEnabled(False)
        range_layout.addWidget(self.input_end)
        range_layout.addStretch()
        layout.addLayout(range_layout)

        # 自定义小数位数（默认禁用）
        dec_layout = QHBoxLayout()
        dec_layout.addWidget(QLabel("小数位数："))
        self.input_dec = QLineEdit("2")
        self.input_dec.setFixedWidth(80)
        self.input_dec.setEnabled(False)
        dec_layout.addWidget(self.input_dec)
        dec_layout.addStretch()
        layout.addLayout(dec_layout)

        # 选自定义时启用
        def on_diff_changed():
            is_custom = self.radio_custom.isChecked()
            self.input_start.setEnabled(is_custom)
            self.input_end.setEnabled(is_custom)
            self.input_dec.setEnabled(is_custom)
        self.diff_group.buttonClicked.connect(on_diff_changed)

        # 错误提示
        self.label_error = QLabel("")
        self.label_error.setStyleSheet("color: #ff6b6b; font-size: 12px;")
        self.label_error.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_error)

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
        """确定"""
        # 运算类型
        op_id = self.op_group.checkedId()
        order_map = {0: "+", 1: "-", 2: "*", 3: "/"}
        order = order_map[op_id]

        # 难度
        diff_id = self.diff_group.checkedId()
        if diff_id == 0:
            start, end, decimals = 1, 10, 1
        elif diff_id == 1:
            start, end, decimals = 1, 100, 2
        elif diff_id == 2:
            start, end, decimals = 1, 1000, 3
        else:
            # 自定义
            try:
                start = int(self.input_start.text())
                end = int(self.input_end.text())
                decimals = int(self.input_dec.text())
            except ValueError:
                self.label_error.setText("必须输入整数")
                return
            if end <= start:
                self.label_error.setText("末值必须大于起始值")
                return
            if not (1 <= decimals <= 4):
                self.label_error.setText("小数位数必须在 1~4 之间")
                return

        self.result_data = (order, decimals, start, end)
        self.accept()
