import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.dcard.tw/topics/%E7%86%B1%E9%96%80')
root_url = 'https://www.dcard.tw'
soup = BeautifulSoup(r.text, 'html.parser')
spans = soup.find_all('article', class_='tgn9uw-0 dRhFWg')

def alltopic():
    for span in spans:
        url = root_url + span.find('a', class_='tgn9uw-3').get('href')
        title = span.find('a', class_='tgn9uw-3').text
        feedback = span.find_all('div', class_='uj732l-2 jWxgsr')
        feedback= [s.text for s in feedback]
        emoji = feedback[0]
        comment = feedback[1]
        print(f'{url}\n{title}\nemoji: {emoji}, comment: {comment}')


def max_emoji_topic():
    emoji_max = 0
    for span in spans:
        feedback = span.find_all('div', class_='uj732l-2 jWxgsr')
        feedback= [s.text for s in feedback]
        emoji = int(feedback[0])
        if emoji>emoji_max:
            emoji_max = emoji
            comment = feedback[1]
            url = root_url + span.find('a', class_='tgn9uw-3').get('href')
            title = span.find('a', class_='tgn9uw-3').text
        else:
            continue
        print(f'{url}\n{title}\nemoji: {emoji}, comment: {comment}')

# https://www.dcard.tw/f/mood/p/228780098
# 拜託上熱門，平鎮大火，我在準備今年的消防特考
# emoji: 33521, comment: 951
if __name__ == '__main__':
    alltopic()
    max_emoji_topic()