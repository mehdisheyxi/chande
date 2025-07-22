import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget

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
        self.actionabout_us.triggered.connect(self.about)

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
            # dolar
            market_price_dolar = soup.find('td', class_='market-price')
            market_high_dolar = soup.find('td', class_='market-high')
            market_low_dolar = soup.find('td', class_='market-low')
            # urou
            market_price_urou = soup.select_one(
                '#main > div:nth-child(5) > div.home-fs-row > div.index-tabs.index-tabs-line > div > div.index-tabs-content.currency-overview-content.active.currency-min-font > div.index-tabs-data.bootstrap-fix > div > div.col-12.col-lg-12.col-xl-6.index-tabs-data-col-1 > table > tbody > tr:nth-child(2) > td.market-low')
            market_high_urou = soup.select_one(
                '#main > div:nth-child(5) > div.home-fs-row > div.index-tabs.index-tabs-line > div > div.index-tabs-content.currency-overview-content.active.currency-min-font > div.index-tabs-data.bootstrap-fix > div > div.col-12.col-lg-12.col-xl-6.index-tabs-data-col-1 > table > tbody > tr:nth-child(2) > td.market-high')
            market_low_urou = soup.select_one(
                '#main > div:nth-child(5) > div.home-fs-row > div.index-tabs.index-tabs-line > div > div.index-tabs-content.currency-overview-content.active.currency-min-font > div.index-tabs-data.bootstrap-fix > div > div.col-12.col-lg-12.col-xl-6.index-tabs-data-col-1 > table > tbody > tr:nth-child(1) > td.market-low')
            # emam coin
            market_price_coin_emam = soup.select_one(
                '#main > div:nth-child(5) > div:nth-child(5) > div:nth-child(18) > table > tbody > tr:nth-child(1) > td:nth-child(2)')
            market_high_coin_emam = soup.select_one(
                '#main > div:nth-child(5) > div:nth-child(5) > div:nth-child(18) > table > tbody > tr:nth-child(1) > td:nth-child(5)')
            market_low_coin_emam = soup.select_one(
                '#main > div:nth-child(5) > div:nth-child(5) > div:nth-child(18) > table > tbody > tr:nth-child(1) > td:nth-child(4)')
            # bank coin
            market_price_coin_bank = soup.select_one('#coin-table > tbody > tr:nth-child(2) > td:nth-child(2)')
            market_high_coin_bank = soup.select_one('#coin-table > tbody > tr:nth-child(2) > td:nth-child(5)')
            market_low_coin_bank = soup.select_one('#coin-table > tbody > tr:nth-child(2) > td:nth-child(4)')

            # بررسی وجود تگ‌ها
            if market_price_dolar and market_high_dolar and market_low_dolar and market_price_urou:
                # دلار
                self.label_8.setText(f"💰 {market_price_dolar.text.strip()}")
                self.label_9.setText(f"📈{market_high_dolar.text.strip()}")
                self.label_10.setText(f"📉{market_low_dolar.text.strip()}")
                # یورو
                self.label_17.setText(f"💰 {market_price_urou.text.strip()}")
                self.label_14.setText(f"📈{market_high_urou.text.strip()}")
                self.label_11.setText(f"📉{market_low_urou.text.strip()}")
                # emam coin
                self.label_18.setText(f"💰{market_price_coin_emam.text.strip()}")
                self.label_15.setText(f"📈{market_high_coin_emam.text.strip()}")
                self.label_12.setText(f"📉{market_low_coin_emam.text.strip()}")
                # bank coin
                self.label_19.setText(f"💰{market_price_coin_bank.text.strip()}")
                self.label_16.setText(f"📈{market_high_coin_bank.text.strip()}")
                self.label_13.setText(f"📉{market_low_coin_bank.text.strip()}")
            else:
                self.label_8.setText("❗ اطلاعات یافت نشد")
                self.label_9.setText("-")
                self.label_10.setText("-")
                self.label_17.setText("-")
                self.label_14.setText("-")
                self.label_11.setText("-")

        except Exception as e:
            self.label_8.setText("⚠️ خطای داخلی")
            self.label_22.setText(str(e))
            self.label_10.setText("-")

    def about(self):
        self.about_us = aboutus()
        self.about_us.show()


class aboutus(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('UI/about.ui', self)
        self.setWindowTitle('Aboutus')
        self.setWindowIcon(QIcon("logo/logochande.png"))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
