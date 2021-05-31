import requests
from bs4 import BeautifulSoup as bs
import re

r = requests.get('https://tw.yahoo.com/')
#print(r.headers)
if r.status_code == requests.codes.ok:
    print('start=========================')
    soup = bs(r.text,'html.parser')
    
    #stories = soup.find_all('a')
    for s in stories:
        print('標題: '+s.text)
        
        print('網址: '+s.get('href'))
