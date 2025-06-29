import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi  # لود کردن فایل .ui

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI/main_window2.ui", self)  # نام فایل .ui را تنظیم کن
        self.setWindowTitle("chande")
        self.setWindowIcon(QIcon("logo/logochande.png"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
#
