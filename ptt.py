import requests
from bs4 import BeautifulSoup
import sys


Base_url = "https://www.ptt.cc/bbs/" + sys.argv[1] + "/search?q="
url = Base_url + sys.argv[2]
# url = 'https://www.ptt.cc/bbs/Food/index.html'
'''
Base_url = "https://www.ptt.cc/bbs/" + 'gossiping' + "/search?q="
url = Base_url + '阿明'
'''

try:
    fil = int(sys.argv[3])
except:
    fil = 0

my_headers = {'cookie': 'over18=1;'}

def get_all_href(url):
    r = requests.get(url, headers = my_headers)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.select("div.title")
    results2 = soup.select("div.nrec")
    for k in range(len(results)):
        a_item = results[k].select_one("a")
        title = results[k].text
        if a_item:
            try:
                num = results2[k].select_one("span").text
                if int(num) >= fil:
                    print("[ 推文數: " + num + "]" + title, 'https://www.ptt.cc' + a_item.get('href'))
            except:
                if fil == 0:
                    print("[推文數: 0]" + title, 'https://www.ptt.cc' + a_item.get('href'))

            #print(title, 'https://www.ptt.cc' + a_item.get('href'))

    '''
    for item in results:
        a_item = item.select_one("a")
        title = item.text
        if a_item:
            print(title, 'https://www.ptt.cc' + a_item.get('href'))
    '''

def next_page(url):
    try:
        r = requests.get(url, headers = my_headers)
        soup = BeautifulSoup(r.text, "html.parser")
        btn = soup.select('div.btn-group > a')
        next_page_href = btn[3]['href']
        next_page_url = 'https://www.ptt.cc' + next_page_href
        url = next_page_url
        return url
    except:
        return 1

i = 0
ans = None
while(i == 0):
    try:
        get_all_href(url=url)
        url = next_page(url)
        if url == 1:
            print("No next page!")
            i += 1
        if i == 0:
            ans = input("next_page ? (Y/N)")
            while ans != 'Y' and ans != 'N':
                ans = input("next_page ? (Y/N)")
            if ans == 'N':
                print("ok")
                i += 1
    except:
        i += 1
        print("no result!")