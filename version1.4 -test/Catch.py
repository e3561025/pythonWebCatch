
from bs4 import BeautifulSoup
import re
import requests
import zipfile,io
import random
from io import BytesIO
from PIL import Image
from checkR18 import CheckR18
class webCatch:
        #首頁網址
        origin_url = 'https://www.wnacg.org'
        title=[]
        href=[]
        pic=[]
        #紀錄當前url, nextpage要用
        currentText=''
                
        def __init__(self):
                self.checkR18model = CheckR18()
        #開始搜尋
        def search(self,word):
                self.title.clear()
                self.href.clear()
                self.pic.clear()
                dic = {'sname':word}
                text = requests.get(self.origin_url+'/albums.html',params=dic).text
                self.currentText = text
                return self.hrefAndTitleGet(text)

        def getPicture(self,index):
                #url = self.origin_url+self.pic[index]
                url = 'https:'+self.pic[index]
                #print(url)
                stream=requests.get(url).content
                return stream

        def hrefAndTitleGet(self,text):
                soup = BeautifulSoup(text,'lxml')
                mylist = soup.select('div.pic_box > a')
                pic = soup.select('div.pic_box > a > img')
                for i in mylist:
                        self.title.append(i.get('title'))
                        self.href.append(i.get('href'))
                for i in pic:
                        self.pic.append(i.get('src'))
                        #print(i.get('src'))
                return self.title        

        def nextOrPre(self,tag):
                text = str(BeautifulSoup(self.currentText,'lxml').find_all(class_='f_left paginator')[0])
                soup = BeautifulSoup(text,'lxml')
                #上一頁
                if(tag==0):
                        hrefList=soup.select('span.prev > a')
                        if(len(hrefList)!=0):
                                self.href.clear()
                                self.title.clear()
                                self.pic.clear()
                                href = hrefList[0].get('href')
                                self.currentText = requests.get(self.origin_url+href).text
                                return self.hrefAndTitleGet(self.currentText)
                        return []
                if(tag==1):
                        hrefList=soup.select('span.next > a')
                        if(len(hrefList)!=0):
                                self.href.clear()
                                self.title.clear()
                                self.pic.clear()
                                href = hrefList[0].get('href')
                                self.currentText = requests.get(self.origin_url+href).text
                                return self.hrefAndTitleGet(self.currentText)
                        return []

                
        def checkR18Pic(self,index):
                url = self.href[index]
                soup = BeautifulSoup(requests.get(self.origin_url+url).text,'lxml')
                checkList=soup.select('li.gallary_item div.pic_box img')
                checkPicNum=5
                checkPicContent=[]
                randNum=[]
                
                if len(checkList) >=checkPicNum:
                        num=set()
                        while len(num)<checkPicNum:
                                num.add(random.randint(0,len(checkList)-1))
                        randNum=list(num)
                else:
                        randNum=list(range(0,len(checkList)))
                for i in randNum:
                        checkPicContent.append(requests.get('https:'+checkList[i].get('src')).content)
                #print('the flag num is : ',len(checkPicContent))
                flag=self.checkR18model.checkR18(checkPicContent)
                return flag
                        
                

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
        
