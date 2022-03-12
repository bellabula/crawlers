from asyncio.windows_events import NULL
from email import header
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

def crawl(date):
    r = requests.get('https://www.taifex.com.tw/cht/3/futContractsDate?queryDate={}%2F{}%2F{}'.format(date.year, date.month, date.day))
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        if soup.find_all('td', class_='13red'):
            out = NULL
        else:
            table = soup.find('table', class_='table_f')
            rows = table.find_all('tr')
            first_colname = ['']*3
            for _ in list(rows.pop(0).stripped_strings):
                first_colname += [_] * 6
            second_colname = ['']*3
            for _ in list(rows.pop(0).stripped_strings):
                second_colname += [_] * 2
            third_colname = [th.text for th in rows.pop(0).find_all('th')]
            data = []
            row_count = 1
            for row in rows:
                ths = row.find_all('th')
                if row_count%3 == 1 :
                    d_head = [th.text.strip() for th in row.find_all('th')]
                    if len(d_head) == 3:
                        pass
                    else:
                        d_head = [d_head[0]]*(3-len(d_head)) + d_head
                else:
                    d_head = d_head[:2] + [row.find_all('th')[-1].text.strip()]

                d = d_head + [td.text.strip() for td in row.find_all('td')]
                row_count += 1
                data.append(d)
                # raise SystemExit
            out = [first_colname, second_colname, third_colname] + data
    else:
        print('connection error')
    return out

date = datetime.today()
get_days = 5 # 期貨交易所只有近3年資料 ()
while True:
    data = crawl(date)
    if data == NULL:
        print(date.date(), '例假日查無資料')
    else:
        df = pd.DataFrame(data)
        df.to_csv(f'futures_{date.date()}.csv', index=False, header=False)
    date = date - timedelta(days=1)
    if date < datetime.today() - timedelta(days=get_days):
        break