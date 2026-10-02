#config(V1.3-Alpha)
NameList = []
KeyList = []
ScoreList = []

import os
import sys

def get_base_dir():
    """获取程序所在目录，兼容开发环境和打包后"""
    if getattr(sys, 'frozen', False):
        # 打包后，exe 所在目录
        return os.path.dirname(sys.executable)
    else:
        # 开发环境，当前文件所在目录
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()

DATA_FILE = os.path.join(BASE_DIR, "user_data.json")
HISTORY_FILE = os.path.join(BASE_DIR, "user_history.json")

ADMIN_KEY_HASH = '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'
#即admin123

Specificians = ["结束", "返回", "退出登录"]
BasicSeries = {
    "1.1": "+",
    "1.2": "-",
    "1.3": "*",
    "1.4": "/",
    "2.1": "mixed",
    "2.2": "decimal",
}
Difficulty = {
    "1": {"name": "5以内的", "start": 1, "end": 5},
    "2": {"name": "10以内的运算", "start": 1, "end": 10},
    "3": {"name": "20以内的运算", "start": 0, "end": 20},
    "4": {"name": "100以内的运算", "start": 0, "end": 100},
    "5": {"name": "10000以内的运算", "start": 0, "end": 10000},
    "6": {"name": "极限模式", "start": -100000000, "end": 100000000}
}

CurrentUser = ""

HistoryList = {}
WrongList = {}
Achievements = {}
