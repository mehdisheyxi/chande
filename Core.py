import requests
from bs4 import BeautifulSoup
import fake_useragent



#create random user_agent for website
url = 'https://www.tgju.org/'

def get_prices(url):
    class_name = [
        'market-price',
        'high',
        'market-low',
        'market-high',
        'market-time'
    ]
    ua = fake_useragent.UserAgent()
    headers = {'user-agent': ua.random}
    response = requests.get(url, headers=headers)
    soap = BeautifulSoup(response.text,'html.parser')
    price = soap.find_all('td',attrs={'class':class_name})
    return price
    # if price:
    #     raw_price = price.text.strip()  # حذف فضای خالی اول و آخر
    #     clean_price = raw_price.replace(',', '')
    #
    #     try:
    #         price_int = int(clean_price)
    #         return (f'this is final OK:{price_int:,}\n xobe ??!!')
    #     except ValueError:
    #         return (f'NOT OK:{clean_price}')
    # else:
    #     return ('NOT FOUND')









print(get_prices(url))