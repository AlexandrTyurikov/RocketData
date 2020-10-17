import requests
from bs4 import BeautifulSoup as bs
import json

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
    'accept': '*/*'
}
url_mebelshara = "https://www.mebelshara.ru/contacts"
date = []


def mebelshara_pars():
    request = requests.get(url_mebelshara, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        salons_info = soup.find_all('div', attrs={'class': 'shop-list-item'})
        for salon in salons_info:
            date.append({
                'address': salon['data-shop-address'],
                'latlon': [float(salon['data-shop-latitude']), float(salon['data-shop-longitude'])],
                'name': salon['data-shop-name'],
                'phones': salon['data-shop-phone'],
                'working_hours': f"{salon['data-shop-mode1']} {salon['data-shop-mode2']}"
            })
    with open('data_site_1.json', 'w', encoding='utf-8) as file:
        json.dump(date, file, indent=4, ensure_ascii=False)


mebelshara_pars()
