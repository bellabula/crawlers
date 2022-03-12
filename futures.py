import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def crawl(date):
    r = requests.get('https://www.taifex.com.tw/cht/3/futContractsDate?queryDate={}%2F{}%2F{}'.format(date.year, date.month, date.day))
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            table = soup.find('table', class_='table_f')
            rows = table.find_all('tr')
        except AttributeError:
            print('no data for', date.date())
            return
        
        data = {}
        for row in rows[3:]:
            d = list(row.stripped_strings)

            if d[0] == '期貨':
                break

            if len(d) == 15:
                product = d[1]
                row_data = d[1:]
            else:
                row_data = [product] + d

            row_data = row_data[:2] + [int(d.replace(',', '')) for d in row_data[2:]]
            col_name = ['商品', '身份別', '交易多方口數', '交易多方契約金額', '交易空方口數', '交易空方契約金額', '交易多空淨額口數','交易多空淨額契約金額',
                        '未平倉多方口數', '未平倉多方契約金額', '未平倉空方口數', '未平倉空方契約金額', '未平倉多空淨額口數','未平倉多空淨額契約金額']

            # product - who - what
            product = row_data[0]
            who = row_data[1]
            contents = {col_name[i]:row_data[i] for i in range(2, len(row_data))}

            if product not in data:
                data[product] = {who:contents}
            else:
                data[product][who] = contents
        return data
    else:
        print('connection error')

date = datetime.today()
get_days = 5 # 期貨交易所只有近3年資料 ()
data = {}
while True:
    daily_data = crawl(date)
    if daily_data == None:
        pass
    else:
        data[date.strftime('%Y/%m/%d')] = daily_data
    date = date - timedelta(days=1)
    if date < datetime.today() - timedelta(days=get_days):
        break
