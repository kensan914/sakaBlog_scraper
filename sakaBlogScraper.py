import urllib3
from bs4 import BeautifulSoup
import time;
import re;
import requests
from urllib3.exceptions import InsecureRequestWarning


def continueConfirmation(m):
    print(m['full_kanji'] + 'のブログデータをスクレイピングします。よろしいですか？[yes, no]\n>>> ', end='')
    answer = input()
    if answer == 'yes' or answer == 'y':
        return True
    elif answer == 'no' or answer == 'n':
        print('メンバー検索に戻ります。')
        return False
    else:
        print('不当な値が入力されました。もう一度入力してください。')
        continueConfirmation(m)

sleepTime = 1;
keyList = ['id', 'last_kanji', 'first_kanji', 'full_kanji', 'last_gana', 'first_gana', 'full_gana', 'filename', 'group_id']

print('='*5 + 'KEYAKI-ZAKA & HINATA-ZAKA BLOG SCRAPER' + '='*5)
print('ブログデータのスクレイピングを実行するメンバーを入力してください')
while True:
    print('入力方法：漢字表記もしくはひらがな表記で、苗字または下の名前またはフルネームで入力してください。ex)斎藤\n>>> ', end='')
    serchTxt = input()
    matchMembers = []

    fin = open('memberList.txt', 'rt', encoding='utf-8')
    lines = fin.readlines()
    fin.close()
    for line in lines:
        if serchTxt in line:
            pvsMatchMember = {}
            for key, val in zip(keyList, list(line.split(' '))):
                pvsMatchMember[key] = val
            matchMembers.append(pvsMatchMember)
    if len(matchMembers) == 1:
        member = matchMembers[0]
        if continueConfirmation(member):
            break
    elif len(matchMembers) > 1:
        while True:
            print(serchTxt + 'で検索したところ複数のメンバーが該当しました。以下の選択肢から数字のみを入力してください。')
            for i, matchMember in enumerate(matchMembers):
                print(str(i) + '：' + matchMember['full_kanji'] +'  ', end='')
            print('\n>>> ', end='')
            serchNum = int(input())
            if 0 <= serchNum < len(matchMembers):
                member = matchMembers[serchNum]
                break
            else:
                print('不当な値が入力されました。もう一度入力してください。')
        if continueConfirmation(member):
            break
    else:
        print('「' + serchTxt + '」で検索しましたが該当するメンバーがいませんでした。もう一度入力してください。')

if int(member['group_id']) == 1:
    base_url = 'http://www.keyakizaka46.com/s/k46o/diary/member/list?ima=0000&ct=' + member['id'] + '&page=' #欅ver
else:
    base_url = 'https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=' + member['id'] + '&page=' #日向ver
upLimit = 100

fout = open('sakaBlogOutput/'+member['filename']+'_blog.txt', 'wt', encoding='utf-8')

imgTag_ptn = '<img.*/>'
imgTag_rePtn = re.compile(imgTag_ptn)

urllib3.disable_warnings(InsecureRequestWarning)
http = urllib3.PoolManager()
for page in range(upLimit):
    print('now scraping page', page, '...')

    url = base_url + str(page)
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data, 'html.parser')

    if int(member['group_id']) == 1:
        article_tags  = soup.find_all('div', class_='box-article')
    else:
        article_tags  = soup.find_all('div', class_='c-blog-article__text')
    if len(article_tags) == 0:
        print("finished!!")  
        break
    for article_tag in article_tags:
        article = ''
        for article_child in article_tag.childGenerator():
            if str(article_child) == '<br/>' or str(article_child) == '<br>':
                article += '\n'
            elif not imgTag_rePtn.match(str(article_child)):
                article += str(article_child).replace('\n', '')
        if '<' in article or '>' in article:
            article_soup = BeautifulSoup(article, 'html.parser')
            for br in article_soup.find_all("br"):
                br.replace_with("\n")
            new_article = article_soup.getText()
            print(new_article, file=fout)
        else:
            print(article, file=fout)
    time.sleep(sleepTime)
    
fout.close()
