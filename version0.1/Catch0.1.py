
from bs4 import BeautifulSoup
import re
import requests
import zipfile,io

#首頁網址
origin_url = 'https://www.wnacg.org'


#開始搜尋
def search(word):
    dic = {'sname':word}
    text = requests.get(origin_url+'/albums.html',params=dic).text
    soup = BeautifulSoup(text,'lxml')
    mylist = soup.select('div.pic_box > a')
    tag=1
    title=[]
    href=[]
    for i in mylist:
        
        print(str(tag)+'. '+i.get('title')+' : '+i.get('href'))
        tag+=1
tag = int(input('input the want item : '))    
url = mylist[tag-1].get('href')
text = requests.get(origin_url+url).text
soup = BeautifulSoup(text,'lxml')
url = soup.select('a.downloadbtn')[0].get('href')
string = soup.select('div.userwrap > h2')[0].string
text = requests.get(origin_url+url).text
ziplist = BeautifulSoup(text,'lxml').select('a.down_btn')[0].get('href')
print(ziplist)
zipurl = requests.get(ziplist,stream=True)
content_size = int(zipurl.headers['content-length'])
chunk_size=1024

with open('D:/python_Test/python-design/test.rar','wb') as f:
    for i in zipurl.iter_content(chunk_size):
        f.write(i)
print('\n\n it is end')
     
