import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi  # لود کردن فایل .ui

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI/main_window.ui", self)  # نام فایل .ui را تنظیم کن


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
#