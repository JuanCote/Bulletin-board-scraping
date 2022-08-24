import random
import time

from bs4 import BeautifulSoup
from requests import get
import lxml, csv


cookies = {
    'ring': 'e889a4023571bba16b1e5388460ea056',
    '_gid': 'GA1.2.2120417587.1660846654',
    '_ga_4Z77EHRZZW': 'GS1.1.1660846666.1.1.1660847106.0.0.0',
    'city': '277',
    '_ga_G0RWKN84TQ': 'GS1.1.1660846654.1.1.1660847172.0.0.0',
    '_ga': 'GA1.1.256518207.1660846654',
}

headers = {
    'authority': 'www.farpost.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,uk;q=0.5',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'ring=e889a4023571bba16b1e5388460ea056; _gid=GA1.2.2120417587.1660846654; _ga_4Z77EHRZZW=GS1.1.1660846666.1.1.1660847106.0.0.0; city=277; _ga_G0RWKN84TQ=GS1.1.1660846654.1.1.1660847172.0.0.0; _ga=GA1.1.256518207.1660846654',
    'dnt': '1',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}


def main():
    chapter = input('Enter chapter ')

    result_data = list()
    for page in range(1, 181):
        url = 'https://www.farpost.ru/' + chapter + f'?page={page}'

        response = get(url, cookies=cookies, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')

        cards = soup.find_all('tr', class_='bull-item bull-item_inline -exact bull-item bull-item_inline')

        for card in cards:
            name = card.find('a', class_='bulletinLink bull-item__self-link auto-shy').text
            try:
                price = card.find('span', class_='price-block__price').text
            except:
                price = 'None'
            try:
                date = card.find('div', class_='date').text
            except:
                date = 'None'
            try:
                views = card.find('span', class_='views nano-eye-text').text
            except:
                views = 'None'

            result_data.append({
                'name': name,
                'price': price,
                'date': date,
                'views': views
            })

        time.sleep(random.randint(3, 5))
        print(f'Page {page} parsed')

    with open(f'result.csv', 'w', newline='', encoding='utf-16') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(
            ('Title', 'Price', 'Date', 'Views')
        )

    with open(f'result.csv', 'a', newline='', encoding='utf-16') as file:
        writer = csv.writer(file, delimiter='\t')
        for elem in result_data:
            writer.writerow(
                (
                    elem['name'],
                    elem['price'],
                    elem['date'],
                    elem['views']
                )
            )


if __name__ == '__main__':
    main()





