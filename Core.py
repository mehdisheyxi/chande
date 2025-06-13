import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

user_agent = UserAgent()
ua = user_agent.random

url = 'https://www.tgju.org/'


def refresh(url):
    pass

def get_price(url):
    headers = {'User-Agent': ua}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return 'Error fetching data'

    soup = BeautifulSoup(response.text, 'html.parser')
    market_price = soup.find('td', class_='market-price')
    market_low = soup.find('td', class_='market-low')
    market_high = soup.find('td', class_='market-high')

    if not (market_price and market_low and market_high):
        return 'Data not found'

    try:
        price_int = int(market_price.text.strip().replace(',', ''))
        low_int = int(market_low.text.strip().replace(',', ''))
        high_int = int(market_high.text.strip().replace(',', ''))

        return f'market-price = {price_int:,}\n' \
               f'low = {low_int:,}\n' \
               f'high = {high_int:,}'
    except ValueError:
        return 'Invalid data format'


print(get_price(url))
