import requests
from bs4 import BeautifulSoup
import progressbar

def write_file(filname, data, other_text=None):
    with open(filname, 'w', encoding='utf-8') as f:
        if bool(other_text):
            f.write(other_text)
        for c in data:
            f.write(f'{c}:{len(data[c])}筆\n\t{data[c]}\n')


def get_dcard_comment(url, savefile=None):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.text
    feedback = soup.find('div', class_='fiw2dr-2 euXXTa')
    mood = int(feedback.text.split('・')[0])
    count_com = int(feedback.text.split()[1])
    all_com = {}
    del_com = 0
    bar = progressbar.ProgressBar(max_value=count_com)
    for i in range(1, count_com+1): 
        r1 = requests.get(f'{url}/b/{i}')
        if r1.status_code == requests.codes.ok:
            soup1 = BeautifulSoup(r1.text, 'html.parser')
            dcard = soup1.find('span', class_='cax7qe-2 hKAjCB')
            com = soup1.find('div', class_='phqjxq-0 iJJmxb')
            if dcard.text in all_com:
                all_com[dcard.text].append(com.text)
            else:
                all_com[dcard.text] = [com.text]
        else:
            del_com += 1
        bar.update(i)
    # save to file
    if bool(savefile):
        remain_com = count_com - del_com
        doc = f'{title}\n{url}\n心情:{mood}  留言:{count_com} (其中{del_com}筆留言被刪除或隱藏)\n以下{remain_com}筆留言:\n'
        write_file(savefile, all_com, doc)
        out = f'{remain_com}筆留言存於 {savefile}'
    else:
        out = f'未下載留言'
    print(title)
    print(f'心情:{mood}  留言:{count_com} (其中{del_com}筆留言被刪除或隱藏)\n{out}')
    return all_com

if __name__=='__main__':
    get_dcard_comment('https://www.dcard.tw/f/mood/p/228780098', 'mood_228780098.txt')


