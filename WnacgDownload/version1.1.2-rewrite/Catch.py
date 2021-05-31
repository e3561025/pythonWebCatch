
from bs4 import BeautifulSoup
import requests
import zipfile,io,os,re
class webCatch:
        #首頁網址
        origin_url = 'https://www.wnacg.org'
        search_url = 'https://www.wnacg.org/search/'
        title=[]
        href=[]
        pic=[]
        #紀錄當前url, nextpage要用
        currentText=''
        
        #開始搜尋
        def search(self,word):
                self.title.clear()
                self.href.clear()
                self.pic.clear()
                dic = {'q':word,'f':'_all','s':'create_time_DESC'}
                text = requests.get(self.search_url,params=dic).text
                self.currentText = text
                return self.hrefAndTitleGet(text)

        def getPicture(self,index):
                url = 'https:'+self.pic[index]
                stream=requests.get(url).content
                return stream

        def hrefAndTitleGet(self,text):
                soup = BeautifulSoup(text,'lxml')
                mylist = soup.select('div.pic_box > a')
                pic = soup.select('div.pic_box > a > img')
                for i in mylist:
                        name = i.get('title')
                        name = re.sub('<.*?>', '', name)
                        self.title.append(name)
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

                

        def choose(self,index,path):
                #取得選取漫畫之title & href
                name = self.title[index]   
                url = self.href[index]
                print(url)
                #進入選取漫畫之網址
                text = requests.get(self.origin_url+url).text
                soup = BeautifulSoup(text,'lxml')
                #進入下載網頁
                url = soup.select('a.btn')[2].get('href')
                string = soup.select('div.userwrap > h2')[0].string
                #取得zip檔網址
                text = requests.get(self.origin_url+url).text
                ziplist = BeautifulSoup(text,'lxml').select('a.down_btn')[0].get('href')
                print(ziplist)
                #取得zip 資料流
                zipurl = requests.get('http:'+ziplist,stream=True)
                content_size = int(zipurl.headers['content-length'])
                chunk_size=1024
                #開始下載
                with open(path+'/'+name+'.temp','wb') as f:
                        for i in zipurl.iter_content(chunk_size):
                                f.write(i)
                        print(name+'\n\n it is end')
                os.rename(path+'/'+name+'.temp',path+'/'+name+'.rar')
        
