import requests
from bs4 import BeautifulSoup

def get_stock_price():
    while True:
        stock_code = input('請輸入要查詢的股號(q to quit): ')
        print('')
        if stock_code == 'q':
            print('感謝使用!')
            break
        elif ',' in stock_code:
            stock_code = stock_code.split(',')
        else:
            stock_code = [stock_code]

        for code in stock_code:
            try:
                url = f'https://tw.stock.yahoo.com/quote/{int(code)}.TW'
                r = requests.get(url)
                if r.status_code == requests.codes.ok:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    li = soup.find_all('li', class_='price-detail-item')
                    stock = {'股名': f'{soup.h1.text}({soup.h1.next_sibling.text})', '更新時間':soup.time.span.next_sibling.text}
                    info = dict(zip([l.find_all('span')[0].text for l in li], [l.find_all('span')[1].text for l in li]))
                    stock.update(info)
                    for key, value in stock.items():
                        print(f'{key}: {value}')
                    print('')
                else:
                    print(f'{int(code)}未找到資料\n')
            except ValueError:
                print(f'{code} 並非數字, 請輸入股號\n')
                continue

if __name__ == '__main__':
    get_stock_price()
