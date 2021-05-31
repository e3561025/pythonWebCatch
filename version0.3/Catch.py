
from bs4 import BeautifulSoup
import re
import requests
import zipfile,io
class webCatch:
        #首頁網址
        origin_url = 'https://www.wnacg.org'
        title=[]
        href=[]
        #紀錄當前url, nextpage要用
        currentUrl=''

        #開始搜尋
        def search(self,word):
                self.title.clear()
                self.href.clear()
                dic = {'sname':word}
                text = requests.get(self.origin_url+'/albums.html',params=dic).text
                self.currentUrl = text
                return self.hrefAndTitleGet(text)

        def hrefAndTitleGet(self,text):
                soup = BeautifulSoup(text,'lxml')
                mylist = soup.select('div.pic_box > a')
                
                for i in mylist:
                        self.title.append(i.get('title'))
                        self.href.append(i.get('href'))
                return self.title        

        def nextOrPre(self,tag):
                soup = BeautifulSoup()

        def choose(self,index,path):
                #取得選取漫畫之title & href
                name = self.title[index]   
                url = self.href[index]
                #進入選取漫畫之網址
                text = requests.get(self.origin_url+url).text
                soup = BeautifulSoup(text,'lxml')
                #進入下載網頁
                url = soup.select('a.downloadbtn')[0].get('href')
                string = soup.select('div.userwrap > h2')[0].string
                #取得zip檔網址
                text = requests.get(self.origin_url+url).text
                ziplist = BeautifulSoup(text,'lxml').select('a.down_btn')[0].get('href')
                print(ziplist)
                #取得zip 資料流
                zipurl = requests.get(ziplist,stream=True)
                content_size = int(zipurl.headers['content-length'])
                chunk_size=1024
                #開始下載
                with open(path+'/'+name+'.rar','wb') as f:
                        for i in zipurl.iter_content(chunk_size):
                                f.write(i)
                        print('\n\n it is end')
        
