from bs4 import BeautifulSoup
import re
import requests
#text = '<img alt="[绅士仓库汉化] [ノラネコノタマ (<em>雪野</em>みなと)] 義父と義兄と奴隷な私 4 [DL版]" src="//t3.wnacg.org/data/t/1199/60/16204833424231.jpg">'
text = requests.get('http://www.wnacg.org/photos-index-aid-119960.html').text

soup = BeautifulSoup(text,'lxml')
soup.get










#mylist = soup.select('img')
#print(mylist[0].get('src'))
# text = '[绅士仓库汉化] [ノラネコノタマ (<em>雪野</em>みなと)] 義父と義兄と奴隷な私 4 [DL版]'
# temp = re.sub('<.*?>', '', text)
# print(temp)
