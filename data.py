#data(V1.3-public)
import json
import os
import config

def save_data():
    data = {
        "NameList": config.NameList,
        "KeyList": config.KeyList,
        "ScoreList": config.ScoreList
    }
    with open(config.DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if os.path.exists(config.DATA_FILE):
        try:
            with open(config.DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            config.NameList = data["NameList"]
            config.KeyList = data["KeyList"]
            config.ScoreList = data["ScoreList"]
        except (json.JSONDecodeError, KeyError):
            print("[警告]数据文件损坏，使用默认初始数据")

def save_history():
    data = {
        "HistoryList": config.HistoryList,
        "WrongList": config.WrongList,
        "Achievements": config.Achievements
    }
    with open(config.HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_history():
    if os.path.exists(config.HISTORY_FILE):
        try:
            with open(config.HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            config.HistoryList = data.get("HistoryList", {})
            config.WrongList = data.get("WrongList", {})
            config.Achievements = data.get("Achievements", {})
        except (json.JSONDecodeError, KeyError):
            print("[警告]历史文件损坏，使用默认空数据")
