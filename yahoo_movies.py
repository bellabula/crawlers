import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

url = 'https://movies.yahoo.com.tw/chart.html'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
rows = soup.find_all('div', class_='tr')
colname = list(rows.pop(0).stripped_strings)
contents = []
for row in rows:
    tds = row.find_all('div', class_='td')
    week_rank = tds[0].text.strip()
    lastweek_rank = tds[2].text.strip()
    movie_name = tds[3].text.strip()
    release_date = tds[4].text.strip()
    trailer_address = tds[5].find('a').get('href') if bool(tds[5].find('a')) else ''
    stars = tds[6].text.strip()
    c = [week_rank, lastweek_rank, movie_name, release_date, trailer_address, stars]
    contents.append(c)

contents[0][2] = rows[0].find('h2').text

df = pd.DataFrame(contents, columns=colname)
timestamp = datetime.datetime.now().strftime('%Y%m%d')
df.to_csv(f'movie_rank_{timestamp}.csv', index=False)