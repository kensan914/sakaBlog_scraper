import os
import neologdn
import emoji


def continueConfirmation(m):
    if os.path.isfile('sakaBlogOutput/' + m['filename'] + '_blog.txt'):
        print(m['full_kanji'] + 'のブログデータをクリーニングします。よろしいですか？[yes, no]\n>>> ', end='')
    else:
        print(m['full_kanji'] + 'のブログデータファイルが存在しません。もう一度メンバーを入力してください')
        return False
    answer = input()
    if answer == 'yes' or answer == 'y':
        return True
    elif answer == 'no' or answer == 'n':
        print('メンバー検索に戻ります。')
        return False
    else:
        print('不当な値が入力されました。もう一度入力してください。')
        continueConfirmation(m)

keyList = ['id', 'last_kanji', 'first_kanji', 'full_kanji', 'last_gana', 'first_gana', 'full_gana', 'filename', 'group_id']

print('='*5 + 'KEYAKI-ZAKA & HINATA-ZAKA BLOG FILTER' + '='*5)
print('ブログデータのテキストクリーニングをするメンバーを入力してください')
while True:
    print('入力方法：漢字表記もしくはひらがな表記で、苗字または下の名前またはフルネームで入力してください。ex)斎藤\n>>> ', end='')
    serchTxt = input()
    matchMembers = []

    fin = open('memberList.txt', 'rt')
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


fin2 = open('sakaBlogOutput/' + member['filename'] + '_blog.txt', 'rt', encoding='utf-8')
lines = fin2.readlines()
fin2.close()
fout = open('sakaBlogCorpus/' + member['filename'] + '_blogFiltered.txt', 'wt', encoding='utf-8')

for line in lines:
    i = 0
    for i, l in enumerate(line):
        if l != ' ' and l != '　' and l != '\t':
            break
    line = line[i:]

    if len(line)-1 == 0:
        continue
    line2 = neologdn.normalize(''.join(c for c in line if c not in emoji.UNICODE_EMOJI))
    line3 = line2.lower()
    if '。' in line3:
        existCount = 0
        # for i, l in enumerate(line3):
            # if l == '。':
                # if i+existCount != len(line3)-1:
                    # line3 = line3[:i+existCount+1] + '\n' + line3[i+existCount+1:]
                    # existCount += 1
    fout.write(line3)
fout.close()

print('finished!!')
