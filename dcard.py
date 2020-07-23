import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

Base_url = 'https://www.dcard.tw/search?query='
need = sys.argv[2] #關鍵字
forum = sys.argv[1] #看板
url = Base_url + need + '&forum=' + forum

try:
    fil = int(sys.argv[3])
except:
    fil = 0

#
chromedriver = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(chromedriver,options=options)
driver.get(url)  # 前往這個網址

i = 2
k = 0
record = 0 #have any request?
while i > 0:
    Base_xpath = "/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div["+str(i)+"]/article[1]"
    try:
        need = driver.find_element(By.XPATH, Base_xpath + "/h2[1]/a[1]")
        href = need.get_attribute('href')
        need = driver.find_element(By.XPATH, Base_xpath + "/h2[1]/a[1]/span[1]")
        title = need.get_attribute('innerHTML')
        need = driver.find_element(By.XPATH, Base_xpath + "/div[3]/div[1]/div[1]/div[2]")
        heart = need.text
        i += 1
        record = 1
        if int(heart) >= fil:
            print("愛心數： " + heart, '\n', title, href)
    except:
        try:
            need = driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div["+str(i)+"]")
            i += 1
            k = 0
        except:
            if record == 0:
                print("No result !")
                break
            ans = input("next_page ? (Y/N)")
            while ans != 'Y' and ans != 'N':
                ans = input("next_page ? (Y/N)")

            if ans == 'Y':
                js = "var q=document.documentElement.scrollTop=100000"
                driver.execute_script(js)
                time.sleep(3)
                k += 1
                if k > 1:
                    print("No result !")
                    break
            else:
                print("ok")
                break
