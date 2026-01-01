import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.uic import loadUi

import requests
from bs4 import BeautifulSoup


def resource_path(relative_path):
    """
    مسیر امن برای اجرا در حالت عادی و exe (PyInstaller)
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def safe_text(tag):
    """
    اگر tag None باشه، "-" برگردونه، در غیر اینصورت متنش
    """
    return tag.text.strip() if tag else "-"


class MyApp(QMainWindow):
    url = 'https://www.tgju.org/'

    def __init__(self):
        super().__init__()

        # load main ui
        loadUi(resource_path("UI/main_window2.ui"), self)

        self.setWindowTitle("Chande - چندِ؟")
        self.setWindowIcon(QIcon(resource_path("logo/logochande.png")))

        self.pushButton.clicked.connect(self.refresh)
        self.actionabout_us.triggered.connect(self.about)

    def refresh(self):
        try:
            self.label_21.setText('بروزرسانی...')
            QApplication.processEvents()

            # User-Agent ثابت برای exe
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            response = requests.get(self.url, headers={'User-Agent': ua}, timeout=10)

            if response.status_code != 200:
                self.label_21.setText("❌ اتصال برقرار نشد")
                return

            self.label_21.setText("آنلاین 🟢")
            soup = BeautifulSoup(response.text, 'html.parser')

            # دلار
            market_price_dolar = soup.find('td', class_='market-price')
            market_high_dolar = soup.find('td', class_='market-high')
            market_low_dolar = soup.find('td', class_='market-low')

            # یورو
            market_price_urou = soup.select_one(
                '#main tr:nth-child(2) td.market-price'
            )
            market_high_urou = soup.select_one(
                '#main tr:nth-child(2) td.market-high'
            )
            market_low_urou = soup.select_one(
                '#main tr:nth-child(2) td.market-low'
            )

            # سکه امامی
            market_price_coin_emam = soup.select_one(
                '#coin-table > tbody > tr:nth-child(1) > td:nth-child(2)'
            )
            market_high_coin_emam = soup.select_one(
                '#coin-table > tbody > tr:nth-child(1) > td:nth-child(5)'
            )
            market_low_coin_emam = soup.select_one(
                '#coin-table > tbody > tr:nth-child(1) > td:nth-child(4)'
            )

            # سکه بانکی
            market_price_coin_bank = soup.select_one(
                '#coin-table > tbody > tr:nth-child(2) > td:nth-child(2)'
            )
            market_high_coin_bank = soup.select_one(
                '#coin-table > tbody > tr:nth-child(2) > td:nth-child(5)'
            )
            market_low_coin_bank = soup.select_one(
                '#coin-table > tbody > tr:nth-child(2) > td:nth-child(4)'
            )

            # بروزرسانی label ها با safe_text
            self.label_8.setText(f"💰 {safe_text(market_price_dolar)}")
            self.label_9.setText(f"📈 {safe_text(market_high_dolar)}")
            self.label_10.setText(f"📉 {safe_text(market_low_dolar)}")

            self.label_17.setText(f"💰 {safe_text(market_price_urou)}")
            self.label_14.setText(f"📈 {safe_text(market_high_urou)}")
            self.label_11.setText(f"📉 {safe_text(market_low_urou)}")

            self.label_18.setText(f"💰 {safe_text(market_price_coin_emam)}")
            self.label_15.setText(f"📈 {safe_text(market_high_coin_emam)}")
            self.label_12.setText(f"📉 {safe_text(market_low_coin_emam)}")

            self.label_19.setText(f"💰 {safe_text(market_price_coin_bank)}")
            self.label_16.setText(f"📈 {safe_text(market_high_coin_bank)}")
            self.label_13.setText(f"📉 {safe_text(market_low_coin_bank)}")

        except Exception as e:
            self.label_8.setText("⚠️ خطای داخلی")
            self.label_21.setText(str(e))
            print("Error:", e)

    def about(self):
        self.about_window = AboutUs()
        self.about_window.show()


class AboutUs(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(resource_path("UI/about.ui"), self)
        self.setWindowTitle("About us")
        self.setWindowIcon(QIcon(resource_path("logo/logochande.png")))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
