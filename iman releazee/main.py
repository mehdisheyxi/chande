import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class MyApp(QMainWindow):
    url = 'https://www.tgju.org/'

    def __init__(self):
        super().__init__()
        loadUi("UI/main_window2.ui", self)  # مسیر فایل .ui
        self.setWindowTitle("Chande - چندِ؟")
        self.setWindowIcon(QIcon("logo/logochande.png"))

        self.pushButton.clicked.connect(self.refresh)

    def refresh(self):
        try:
            # ساختن User-Agent جعلی
            user_agent = UserAgent()
            ua = user_agent.random

            # ارسال درخواست به سایت
            self.label_21.setText('بروز رسانی...')
            QApplication.processEvents()
            response = requests.get(self.url, headers={'User-Agent': ua})
            if response.status_code != 200:
                self.label_21.setText("❌ اتصال برقرار نشد")
                self.label_9.setText("-")
                self.label_10.setText("-")
                return

            # پردازش HTML
            self.label_21.setText("انلاین 🟢🟢")
            soup = BeautifulSoup(response.text, 'html.parser')

            # پیدا کردن قیمت‌ها بر اساس کلاس
            market_price = soup.find('td', class_='market-price')
            market_high = soup.find('td', class_='market-high')
            market_low = soup.find('td', class_='market-low')

            # بررسی وجود تگ‌ها
            if market_price and market_high and market_low:
                self.label_8.setText(f"💰 {market_price.text.strip()}")
                self.label_9.setText(f"📈{market_high.text.strip()}")
                self.label_10.setText(f"📉{market_low.text.strip()}")
            else:
                self.label_8.setText("❗ اطلاعات یافت نشد")
                self.label_9.setText("-")
                self.label_10.setText("-")

        except Exception as e:
            self.label_8.setText("⚠️ خطای داخلی")
            self.label_9.setText(str(e))
            self.label_10.setText("-")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
