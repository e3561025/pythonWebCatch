import requests
from bs4 import BeautifulSoup

# Google 搜尋 URL
google_url = 'https://www.google.com.tw/search'

# 查詢參數
my_params = {'q': '寒流'}

# 下載 Google 搜尋結果
r = requests.get(google_url, params = my_params)

# 確認是否下載成功
if r.status_code == requests.codes.ok:
  # 以 BeautifulSoup 解析 HTML 原始碼
  soup = BeautifulSoup(r.text, 'html.parser')

  # 觀察 HTML 原始碼
  a=(soup.prettify())
  with open('yahoo.txt','w',encoding='UTF-8') as f:
    f.write(a)
    f.close()
    print('end')
    
  # 以 CSS 的選擇器來抓取 Google 的搜尋結果
  items = soup.select('div.g > h3.r ')
  for i in items:
    # 標題
    print("標題：" + i.text)
    # 網址
    #print("網址：" + i.get('href'))
print('success')