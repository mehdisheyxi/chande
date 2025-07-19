import sys
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi

user_agent = UserAgent()
ua = user_agent.random
url = "https://www.tgju.org/"

# گرفتن اطلاعات بازار
def get_market_data():
    headers = {'User-Agent': ua}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    markets = {
        "price_usdt": "USDT$",
        "price_eur": "EURO",
        "sekeb": "IMAM-COIN",
        "bitcoin": "BTC",
        "geram18": "GOLD",
        "sugar": "Sugar",
        "copper": "Copper",
        "cocoa": "Cocoa",
        "coffee": "Coffee"
    }

    data = {}
    for key, label in markets.items():
        row = soup.find('tr', {"data-market-row": key})
        if row:
            low = row.find('td', class_='market-low')
            high = row.find('td', class_='market-high')
            price = row.find('td', class_='market-price')

            if low and high and price:
                data[label] = (
                    low.text.strip(),
                    high.text.strip(),
                    price.text.strip()
                )
    return data

# نمایش داده‌ها در جدول
def fill_table(table, labels, data_dict):
    table.setRowCount(len(labels))
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Low", "High", "Live"])

    for i, label in enumerate(labels):
        table.setVerticalHeaderItem(i, QTableWidgetItem(label))
        if label in data_dict:
            low, high, price = data_dict[label]
            table.setItem(i, 0, QTableWidgetItem(low))
            table.setItem(i, 1, QTableWidgetItem(high))
            table.setItem(i, 2, QTableWidgetItem(price))
        else:
            # در صورت نبود داده
            table.setItem(i, 0, QTableWidgetItem("N/A"))
            table.setItem(i, 1, QTableWidgetItem("N/A"))
            table.setItem(i, 2, QTableWidgetItem("N/A"))

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI/main_window.ui", self)

        self.main_labels = ["USDT$", "EURO", "IMAM-COIN", "BTC", "GOLD"]
        self.other_labels = ["Sugar", "Copper", "Cocoa", "Coffee"]

        # بارگذاری اولیه
        self.refresh_tables()

        # اتصال دکمه‌های رفرش
        self.pushButton.clicked.connect(self.refresh_tables)
        self.pushButton_2.clicked.connect(self.refresh_tables)

    def refresh_tables(self):
        data = get_market_data()
        fill_table(self.tableWidget, self.main_labels, data)
        fill_table(self.tableWidget_2, self.other_labels, data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())