from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import urllib

q=urllib.parse.quote('貓咪')
print(q)

url= "https://www.google.com.tw/search?q="+q
driver = webdriver.PhantomJS(executable_path='phantomjs')
driver.get(url)
pageSource = driver.page_source
soup = bs(pageSource,'lxml')
result = soup.select('#resultStats')
for i in result:
    print(i.text)
print(len(result))
print(result)    



driver.close()

"""                     
from selenium import webdriver
from bs4 import BeautifulSoup

url = 'https://www.google.com.tw/#q=%E8%9F%B2%E5%B8%AB'

driver = webdriver.PhantomJS(executable_path='phantomjs')  # PhantomJS
driver.get(url)  # 把網址交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource, 'lxml')  # 解析器接手
result = soup.select('#resultStats')[0].get_text()  # 「約有 1,550,000,000 項結果」
print('蟲師', result)


"""