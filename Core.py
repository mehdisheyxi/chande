import requests
from bs4 import BeautifulSoup
import fake_useragent



#create random user_agent for website
ua = fake_useragent.UserAgent()
headers = {'user-agent': ua.random}

url = 'https://www.tgju.org/'
response = requests.get(url, headers=headers)

soap = BeautifulSoup(response.text,'html.parser')
price = soap.find('td',class_='market-price')


if price:
    raw_price = price.text.strip()  # حذف فضای خالی اول و آخر
    clean_price = raw_price.replace(',', '')

    try:
        price_int = int(clean_price)
        print(f'this is final OK:{price_int:,}')
    except ValueError:
        print(f'NOT OK:{clean_price}')
else:
    print('NOT FOUND')



