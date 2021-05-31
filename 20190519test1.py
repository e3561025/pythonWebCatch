import requests
from bs4 import BeautifulSoup as bs
res = requests.get('https://ani.gamer.com.tw/')

print(res.text)