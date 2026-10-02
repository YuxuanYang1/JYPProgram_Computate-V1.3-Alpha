# admin.py(V1.3-public)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import hashlib
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QTextEdit, QFrame,
                              QLineEdit, QInputDialog, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal

import config
from data import save_data, save_history

# 配色
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4fc3f7"
INPUT_BG = "#2a2a2a"
BORDER_COLOR = "#3a3a3a"
ERROR_COLOR = "#ff6b6b"


class AdminWindow(QWidget):
    """管理员数据管理窗口"""
    
    back_to_login = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据管理")
        self.resize(600, 500)
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
                padding: 8px;
                color: {TEXT_COLOR};
                text-align: left;
                padding-left: 15px;
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
                text-align: center;
                padding-left: 8px;
            }}
            QPushButton#back:hover {{
                background-color: #ff6b6b;
                color: {BG_COLOR};
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # 顶部
        top_layout = QHBoxLayout()
        title = QLabel("数据管理")
        title.setObjectName("title")
        top_layout.addWidget(title)
        top_layout.addStretch()
        btn_back = QPushButton("返回")
        btn_back.setObjectName("back")
        btn_back.setFixedWidth(80)
        btn_back.clicked.connect(self.back_to_login.emit)
        top_layout.addWidget(btn_back)
        layout.addLayout(top_layout)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {BORDER_COLOR};")
        layout.addWidget(line)
        
        # 用户列表
        self.user_display = QTextEdit()
        self.user_display.setReadOnly(True)
        self.user_display.setFixedHeight(200)
        layout.addWidget(self.user_display)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        self.btn_delete = QPushButton("删除用户")
        self.btn_delete.clicked.connect(self.delete_user)
        self.btn_modify = QPushButton("修改分数")
        self.btn_modify.clicked.connect(self.modify_score)
        self.btn_reset = QPushButton("重置密码")
        self.btn_reset.clicked.connect(self.reset_password)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_modify)
        btn_layout.addWidget(self.btn_reset)
        layout.addLayout(btn_layout)
        btn_layout2 = QHBoxLayout()
        self.btn_history = QPushButton("查看历史")
        self.btn_history.clicked.connect(self.view_history)
        self.btn_wrong = QPushButton("查看错题")
        self.btn_wrong.clicked.connect(self.view_wrong)
        self.btn_clear_history = QPushButton("清空用户历史")
        self.btn_clear_history.clicked.connect(self.clear_history)
        self.btn_clear_wrong = QPushButton("清空用户错题")
        self.btn_clear_wrong.clicked.connect(self.clear_wrong)
        btn_layout2.addWidget(self.btn_history)
        btn_layout2.addWidget(self.btn_wrong)
        btn_layout2.addWidget(self.btn_clear_history)
        btn_layout2.addWidget(self.btn_clear_wrong)
        layout.addLayout(btn_layout2)
        
        self.btn_clear = QPushButton("清空所有数据")
        self.btn_clear.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid #ff6b6b;
                color: #ff6b6b;
            }}
            QPushButton:hover {{
                background-color: #ff6b6b;
                color: {BG_COLOR};
            }}
        """)
        self.btn_clear.clicked.connect(self.clear_all)
        layout.addWidget(self.btn_clear)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.refresh()
    
    def refresh(self):
        """刷新用户列表"""
        if not config.NameList:
            self.user_display.setText("暂无用户。")
            return
        lines = []
        for i, (name, score) in enumerate(zip(config.NameList, config.ScoreList)):
            lines.append(f"{i:>2}. {name:<15} {score}分")
        self.user_display.setText("\n".join(lines))
    
    def ask_index(self, prompt):
        """弹窗问序号，返回 int 或 None"""
        if not config.NameList:
            QMessageBox.warning(self, "提示", "暂无用户。")
            return None
        text, ok = QInputDialog.getText(self, "输入", prompt)
        if not ok or not text.strip().isdigit():
            return None
        idx = int(text.strip())
        if not (0 <= idx < len(config.NameList)):
            QMessageBox.warning(self, "提示", "序号超出范围。")
            return None
        return idx
    
    def delete_user(self):
        idx = self.ask_index("输入要删除的用户序号：")
        if idx is None:
            return
        name = config.NameList[idx]
        confirm = QMessageBox.question(self, "确认", f"确定删除用户 {name}？")
        if confirm == QMessageBox.Yes:
            config.NameList.pop(idx)
            config.KeyList.pop(idx)
            config.ScoreList.pop(idx)
            save_data()
            self.refresh()
            QMessageBox.information(self, "完成", f"已删除用户：{name}")
    
    def modify_score(self):
        idx = self.ask_index("输入要修改的用户序号：")
        if idx is None:
            return
        name = config.NameList[idx]
        text, ok = QInputDialog.getText(self, "输入", f"输入 {name} 的新分数：")
        if not ok or not text.strip():
            return
        try:
            new_score = int(text.strip())
        except ValueError:
            QMessageBox.warning(self, "提示", "分数必须是整数。")
            return
        config.ScoreList[idx] = new_score
        save_data()
        self.refresh()
        QMessageBox.information(self, "完成", f"已修改 {name} 的分数为 {new_score}")
    
    def reset_password(self):
        idx = self.ask_index("输入要重置密码的用户序号：")
        if idx is None:
            return
        name = config.NameList[idx]
        text, ok = QInputDialog.getText(self, "输入", f"输入 {name} 的新密码（4-10字符）：", QLineEdit.Password)
        if not ok or not text:
            return
        if not (4 <= len(text) <= 10):
            QMessageBox.warning(self, "提示", "密码长度必须为 4-10 字符。")
            return
        config.KeyList[idx] = hashlib.sha256(text.encode()).hexdigest()
        save_data()
        self.refresh()
        QMessageBox.information(self, "完成", f"已重置 {name} 的密码")
    
    def clear_all(self):
        confirm = QMessageBox.question(self, "确认", "确定清空所有用户数据？此操作不可恢复！")
        if confirm == QMessageBox.Yes:
            config.NameList.clear()
            config.KeyList.clear()
            config.ScoreList.clear()
            save_data()
            self.refresh()
            QMessageBox.information(self, "完成", "已清空所有数据。")
            
    def view_history(self):
        """查看指定用户的历史记录"""
        text, ok = QInputDialog.getText(self, "输入", "输入用户名（回车显示所有）：")
        if not ok:
            return
        user = text.strip()
        if user and user not in config.HistoryList:
            QMessageBox.information(self, "提示", f"用户 {user} 没有历史记录。")
            return
        if not config.HistoryList:
            QMessageBox.information(self, "提示", "暂无历史记录。")
            return
        
        users = [user] if user else list(config.HistoryList.keys())
        lines = []
        total_correct = total_wrong = 0
        total_time = 0
        for u in users:
            records = config.HistoryList.get(u, [])
            if not records:
                continue
            lines.append(f"【{u}】")
            for i, r in enumerate(records, 1):
                lines.append(f"  {i}. {r['mode']} | 正确{r['correct']} 错误{r['wrong']} | 用时{r['time']:.2f}s | 得分{r['score']}")
                total_correct += r["correct"]
                total_wrong += r["wrong"]
                total_time += r["time"]
        lines.append("")
        lines.append(f"总计：正确{total_correct} 错误{total_wrong} 总用时{total_time:.2f}s")
        self.user_display.setText("\n".join(lines))

    def view_wrong(self):
        """查看指定用户的错题本"""
        text, ok = QInputDialog.getText(self, "输入", "输入用户名（回车显示所有）：")
        if not ok:
            return
        user = text.strip()
        if not config.WrongList:
            QMessageBox.information(self, "提示", "错题本为空。")
            return
        users = [user] if user else list(config.WrongList.keys())
        lines = []
        for u in users:
            records = config.WrongList.get(u, [])
            if not records:
                continue
            lines.append(f"【{u}】")
            for i, r in enumerate(records, 1):
                lines.append(f"  {i}. {r['question']} 正确答案：{r['correct']} 你的答案：{r['your']}")
        self.user_display.setText("\n".join(lines))

    def clear_history(self):
        """清空指定用户的历史记录"""
        if not config.HistoryList:
            QMessageBox.information(self, "提示", "暂无历史记录。")
            return
        text, ok = QInputDialog.getText(self, "输入", "输入要清空的用户名：")
        if not ok:
            return
        user = text.strip()
        if user in config.HistoryList:
            confirm = QMessageBox.question(self, "确认", f"确定清空 {user} 的所有历史？")
            if confirm == QMessageBox.Yes:
                del config.HistoryList[user]
                from data import save_history
                save_history()
                QMessageBox.information(self, "完成", f"已清空 {user} 的历史记录。")
        else:
            QMessageBox.warning(self, "提示", "用户不存在。")

    def clear_wrong(self):
        """清空指定用户的错题本"""
        if not config.WrongList:
            QMessageBox.information(self, "提示", "错题本为空。")
            return
        text, ok = QInputDialog.getText(self, "输入", "输入要清空的用户名：")
        if not ok:
            return
        user = text.strip()
        if user in config.WrongList:
            confirm = QMessageBox.question(self, "确认", f"确定清空 {user} 的所有错题？")
            if confirm == QMessageBox.Yes:
                del config.WrongList[user]
                from data import save_history
                save_history()
                QMessageBox.information(self, "完成", f"已清空 {user} 的错题。")
        else:
            QMessageBox.warning(self, "提示", "用户不存在。")
