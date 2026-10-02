# practice.py(V1.3-Alpha)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import time
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QLineEdit, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal

import config
from ols import CreateNumber, BasicOperationJudge, CreateDecimalNumber, CreateMixedNumber
from data import save_history, save_data

# 配色
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4fc3f7"
INPUT_BG = "#2a2a2a"
BORDER_COLOR = "#3a3a3a"
ERROR_COLOR = "#ff6b6b"
SUCCESS_COLOR = "#66bb6a"


class PracticeWindow(QWidget):
    # 信号：返回菜单
    back_to_menu = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("答题")
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                font-family: "Consolas", "Microsoft YaHei";
                font-size: 14px;
            }}
            QLabel#question {{
                font-size: 36px;
                font-weight: bold;
                color: {ACCENT_COLOR};
            }}
            QLabel#score {{
                font-size: 13px;
                color: #999999;
            }}
            QLabel#status_ok {{
                font-size: 14px;
                color: {SUCCESS_COLOR};
            }}
            QLabel#status_err {{
                font-size: 14px;
                color: {ERROR_COLOR};
            }}
            QLineEdit {{
                background-color: {INPUT_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                padding: 8px;
                color: {TEXT_COLOR};
                font-size: 18px;
            }}
            QLineEdit:focus {{
                border: 1px solid {ACCENT_COLOR};
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
            QPushButton:pressed {{
                background-color: {ACCENT_COLOR};
                color: {BG_COLOR};
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
        
        # 状态变量
        self.order = "+"
        self.orderprime = "+"
        self.start = 1
        self.end = 10
        self.PartScore = 0
        self.CorrectCount = 0
        self.WrongCount = 0
        self.TotalTime = 0
        self.NumberA = 0
        self.NumberB = 0
        self.this_question_wrong = False
        self.StartTime = 0
        
        # 主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)
        
        # 顶部：模式名 + 返回按钮
        top_layout = QHBoxLayout()
        self.label_mode = QLabel("整数加法")
        self.label_mode.setStyleSheet(f"font-size: 16px; color: {ACCENT_COLOR};")
        top_layout.addWidget(self.label_mode)
        top_layout.addStretch()
        self.btn_back = QPushButton("返回")
        self.btn_back.setObjectName("back")
        self.btn_back.clicked.connect(self.on_back)
        top_layout.addWidget(self.btn_back)
        layout.addLayout(top_layout)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {BORDER_COLOR};")
        layout.addWidget(line)
        
        layout.addStretch()
        
        # 题目
        self.label_question = QLabel("3 + 5 = ?")
        self.label_question.setObjectName("question")
        self.label_question.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_question)
        
        layout.addSpacing(20)
        
        # 答案输入
        input_layout = QHBoxLayout()
        input_layout.addStretch()
        self.input_answer = QLineEdit()
        self.input_answer.setFixedWidth(200)
        self.input_answer.setAlignment(Qt.AlignCenter)
        self.input_answer.returnPressed.connect(self.on_submit)
        input_layout.addWidget(self.input_answer)
        input_layout.addStretch()
        layout.addLayout(input_layout)
        
        layout.addSpacing(15)
        
        # 提交按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_submit = QPushButton("提 交")
        self.btn_submit.setFixedWidth(150)
        self.btn_submit.clicked.connect(self.on_submit)
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        layout.addSpacing(10)
        
        # 状态提示
        self.label_status = QLabel("")
        self.label_status.setObjectName("status_ok")
        self.label_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_status)
        
        layout.addStretch()
        
        # 分隔线
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet(f"color: {BORDER_COLOR};")
        layout.addWidget(line2)
        
        # 底部：得分统计
        self.label_score = QLabel("得分：0    正确：0    错误：0")
        self.label_score.setObjectName("score")
        layout.addWidget(self.label_score)
        
        self.setLayout(layout)
    
    def start_practice(self, order, start=None, end=None, support_negative=False,
                       real_order=None, decimals=2, mixed_difficulty=1,
                       mixed_include_div=False, mixed_allow_neg=False):
        self.order = order

        if order == "decimal":
            self.real_order = real_order
            self.decimals = decimals
            names = {"+": "小数加法", "-": "小数减法", "*": "小数乘法", "/": "小数除法"}
            self.label_mode.setText(names.get(real_order, "小数运算"))
        elif order == "mixed":
            self.real_order = "mixed"
            self.mixed_difficulty = mixed_difficulty
            self.mixed_include_div = mixed_include_div
            self.mixed_allow_neg = mixed_allow_neg
        else:
            self.real_order = order
            names = {"+": "整数加法", "-": "整数减法", "*": "整数乘法", "/": "整数除法"}
            self.label_mode.setText(names.get(order, "练习"))

        if start is not None and end is not None:
            self.start = start
            self.end = end
        else:
            self.start = 1
            self.end = 10

        if order == "-" and support_negative:
            self.orderprime = "-op"
        else:
            self.orderprime = order

        self.PartScore = 0
        self.CorrectCount = 0
        self.WrongCount = 0
        self.TotalTime = 0
        self.label_status.setText("")
        self.update_score()
        self.next_question()

    def next_question(self):
        if self.order == "decimal":
            self.NumberA, self.NumberB = CreateDecimalNumber(
                self.real_order, self.start, self.end, self.decimals
            )
            self.label_question.setText(
                f"{self.NumberA} {self.real_order} {self.NumberB} = ?")
            self.current_expr = None
            self.current_answer = BasicOperationJudge(
                self.real_order, self.NumberA, self.NumberB)
        elif self.order == "mixed":
            expr, answer = CreateMixedNumber(
                self.start, self.end, self.mixed_difficulty,
                self.mixed_include_div, self.mixed_allow_neg
            )
            self.label_question.setText(f"{expr} = ?")
            self.current_expr = expr
            self.current_answer = answer
        else:
            Numbers = CreateNumber(self.orderprime, self.start, self.end, 2)
            self.NumberA, self.NumberB = Numbers[1], Numbers[0]
            self.label_question.setText(
                f"{self.NumberA} {self.order} {self.NumberB} = ?")
            self.current_expr = None
            self.current_answer = BasicOperationJudge(
                self.order, self.NumberA, self.NumberB)
        self.input_answer.clear()
        self.input_answer.setFocus()
        self.this_question_wrong = False
        self.StartTime = time.time()

    def on_submit(self):
        text = self.input_answer.text().strip()
        if not text:
            return
        try:
            answer = float(text)
        except ValueError:
            self.set_status("请输入数字", error=True)
            return

        EndTime = time.time()
        self.TotalTime += EndTime - self.StartTime

        correct = self.current_answer
        if abs(answer - correct) < 1e-6:
            self.PartScore += 2
            self.set_status(
                f"答对了！用时 {EndTime - self.StartTime:.2f} 秒", error=False)
            self.CorrectCount += 1
            self.update_score()
            self.next_question()
        else:
            if not self.this_question_wrong:
                self.PartScore -= 1
                self.this_question_wrong = True
                if config.CurrentUser:
                    if config.CurrentUser not in config.WrongList:
                        config.WrongList[config.CurrentUser] = []
                    if self.current_expr:
                        q = f"{self.current_expr}=?"
                    else:
                        q = f"{self.NumberA}{self.real_order}{self.NumberB}=?"
                    config.WrongList[config.CurrentUser].append({
                        "question": q,
                        "correct": correct,
                        "your": answer
                    })
                    save_history()
            self.set_status("答错了，请重答", error=True)
            self.WrongCount += 1
            self.update_score()
            self.input_answer.clear()
            self.input_answer.setFocus()

    def set_status(self, text, error=False):
        """设置状态提示"""
        self.label_status.setText(text)
        self.label_status.setObjectName("status_err" if error else "status_ok")
        # 强制刷新样式
        self.label_status.style().unpolish(self.label_status)
        self.label_status.style().polish(self.label_status)
    
    def update_score(self):
        """更新底部得分显示"""
        self.label_score.setText(
            f"得分：{self.PartScore}    正确：{self.CorrectCount}    错误：{self.WrongCount}"
        )
    
    def on_back(self):
        """返回菜单"""
        # 更新总分
        if config.CurrentUser:
            idx = config.NameList.index(config.CurrentUser)
            config.ScoreList[idx] += self.PartScore
            save_data()
            
        # 记录历史
        if config.CurrentUser and (self.CorrectCount + self.WrongCount > 0):
            if config.CurrentUser not in config.HistoryList:
                config.HistoryList[config.CurrentUser] = []
            config.HistoryList[config.CurrentUser].append({
                "mode": self.order,
                "correct": self.CorrectCount,
                "wrong": self.WrongCount,
                "time": round(self.TotalTime, 2),
                "score": self.PartScore
            })
            save_history()
        self.back_to_menu.emit()
