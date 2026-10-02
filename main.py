# main.py(V1.3-public)
import sys
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from data import load_data, load_history
from window import MainWindow

def resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和 PyInstaller 打包后"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后，资源被解压到临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    load_data()
    load_history()
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("icon.ico")))
    app.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e1e;
        }
        QStackedWidget {
            background-color: #1e1e1e;
        }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

