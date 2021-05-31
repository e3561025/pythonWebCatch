# coding=UTF-8
from PIL import Image, ImageTk, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog
import io
import threading
import time
import os.path
from os.path import basename
import urllib.request
import http.cookiejar
import http.cookies
import requests
import ssl
import json
import re
import ctypes
import cv2
import numpy as np
import socket
from tkinter import messagebox

if os.name == 'nt':
    font_type = "arial.ttf"
elif os.name == 'posix':
    font_type = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
else: 
    font_type = "arial.ttf"

loginpage = 'http://www.pixiv.net/login.php/'
loginposturl = 'https://accounts.pixiv.net/api/login?lang=zh_tw'
hosturl = 'https://www.pixiv.net/'
searchUrl = 'https://www.pixiv.net/search.php'
limit = 4000
threadLines = 5
nowThreadLines = 0

def Mbox(title, text, style):
    if os.name == 'nt':
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    else:
        return tkMessageBox.showwarning(title, text)

def getKey(item):
	return item['book_num']

class MultiImageBox(tk.Toplevel):
    def __init__(self, master, opener, urlList, nameList):
        tk.Toplevel.__init__(self)
        self.geometry("400x300")
        self.title(nameList[0])
        self.urlList = urlList
        self.nameList = nameList
        self.opener = opener
        self.master = master
        
        self.imageView = tk.Label(self)
        self.imageView.grid(row=0, column=1,)

        self.nextImageButton = tk.Button(self)
        self.nextImageButton['text'] = "=>"
        self.nextImageButton['command'] = self.nextImage
        self.nextImageButton.grid(row=1, column=3)

        self.indexLabel = tk.Label(self)
        self.indexLabel['text'] = '1/' + str(len(urlList) + 1)
        self.indexLabel.grid(row=1, column=1)

        self.fontImageButton = tk.Button(self)
        self.fontImageButton['text'] = "<="
        self.fontImageButton['command'] = self.frontImage
        self.fontImageButton.grid(row=1, column=0)

        self.imageList = [Image.new('RGB', (300, 300))] * len(urlList)
        self.tkImageList = [ImageTk.PhotoImage(Image.new('RGB', (1, 1)))] * len(urlList)
        self.imageIndex = 0
        self.setImage(self.imageIndex)
        self.resizable(False, False)

        for i in range(len(urlList)) :
            threading._start_new_thread(self.loadImage, (i,))

    def loadImage(self, index):
        def computeWidthAndHeight(imgWidth, imgHeight, maxWidth, maxHeight):
            width = 0
            height = 0
            if imgWidth > imgHeight :
                width = maxWidth
                height = imgHeight / imgWidth * maxWidth
                pass
            else :
                width = imgWidth / imgHeight * maxHeight
                height = maxHeight
                pass
            return (int(width), int(height))

        if(not(os.path.isfile(self.nameList[index]))):
            if(self.urlList[index] == None) :
                return
            res = self.opener.open(self.urlList[index])
            soup = BeautifulSoup(res.read(), 'html.parser')
            find = soup.find('img')
            byteIO = io.BytesIO(self.opener.open(find.attrs['src']).read());
            self.imageList[index] = (Image.open(byteIO))
            self.imageList[index].convert('RGBA')
            self.imageList[index].save(self.nameList[index])
            byteIO.close()
        else :
            self.imageList[index] = (Image.open(self.nameList[index])) #TODO
            
        width, height = self.imageList[index].size
        width, height = computeWidthAndHeight(width, height, 
                                              self.master.winfo_screenwidth() / 2 - self.nextImageButton.winfo_height() * 5, 
                                              self.master.winfo_screenheight() - self.nextImageButton.winfo_width() * 5)
        self.imageList[index] = self.imageList[index].resize((width, height))
        self.tkImageList[index] = ImageTk.PhotoImage(self.imageList[index])
        if index == self.imageIndex:
            self.setImage(index)

    def nextImage(self):
        if self.imageIndex + 1 == len(self.urlList):
            Mbox("Info", "this is the last image", 0)
            return 

        self.imageIndex += 1;
        self.setImage(self.imageIndex)

    def frontImage(self):
        if self.imageIndex == 0:
            Mbox("Info", "this is the home image", 0)
            return 

        self.imageIndex -= 1;
        self.setImage(self.imageIndex)

    def setImage(self, index) :
        if index < 0 or len(self.urlList) <= index :
            return
        width, height = self.imageList[index].size
        self.geometry(str(width + self.nextImageButton.winfo_width() * 3) + "x" + str(height + self.nextImageButton.winfo_height() * 2))
        self.imageView['image'] = self.tkImageList[index]
        self.indexLabel['text'] = str(index + 1) + '/' + str(len(self.urlList))



class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.login()
        self.createWidgets()
        self.imagesPerPage = 250
        self.makeViewIndex = 0
        self.master = master
        self.resetMakeViewFunction = False
        self.makeViewIndexLock = threading.Lock()
        self.makeViewThreadNumLock = threading.Lock()
        self.maxImageThread = 3
        self.imageThreadNum = 0
        self.buttons = []
        self.illustList = []
        self.fileFloderName = ""
        self.haveNaxt = [False, False]
        self.tkImage = [ImageTk.PhotoImage(Image.new("RGBA", (240, 240), (255, 255, 255, 0)))] * self.imagesPerPage
        threading._start_new_thread(self.makeView, ())

    def canvasMouseWheelEvent(self, event) :
        if event.delta < 0:
            self.canvas.yview_scroll(3, tk.UNITS)
        else:
            self.canvas.yview_scroll(-3, tk.UNITS)
    def createWidgets(self):
        self.input          = tk.Entry(self) 
        self.input['width'] = 60
        self.input.grid(row=0, column=1, columnspan=6)

        self.searchButton = tk.Button(self)
        self.searchButton['text'] = 'search'
        self.searchButton.grid(row=0, column=8,)
        self.searchButton['command'] = lambda : self.searchStart()

        self.loadFileButton = tk.Button(self)
        self.loadFileButton['text'] = 'open from file'
        self.loadFileButton.grid(row=0, column=9,)
        self.loadFileButton['command'] = lambda : self.openFile()

        self.safeModeCheckButtonVar = tk.IntVar()
        self.safeModeCheckButton = tk.Checkbutton(self, variable=self.safeModeCheckButtonVar)
        self.safeModeCheckButton['text'] = 'safe mode'
        self.safeModeCheckButton.grid(row=7, column=8,)

        self.r18ModeCheckButtonVar  = tk.IntVar()
        self.r18ModeCheckButton = tk.Checkbutton(self, variable=self.r18ModeCheckButtonVar)
        self.r18ModeCheckButton['text'] = 'r-18 mode'
        self.r18ModeCheckButton.grid(row=8, column=8,)

        self.saveButton = tk.Button(self)
        self.saveButton['text'] = 'save images'
        self.saveButton.grid(row=8, column=1,)
        self.saveButton['command'] = lambda : threading._start_new_thread(self.saveAllImages, (frame.minBookNum.get(), ));
        
        self.minBookNumStringVar = tk.StringVar()
        self.minBookNumStringVar.trace('w', self.minBookNumTrace)

        self.minBookNum = tk.Entry(self, textvariable=self.minBookNumStringVar)
        self.minBookNum['width'] = 60
        self.minBookNum.grid(row=7, column=1,)

        self.nextPageButton = tk.Button(self)
        self.nextPageButton['text'] = ">>"
        self.nextPageButton['command'] = self.nextPage
        self.nextPageButton.grid(row=7, column=2)

        self.fontPageButton = tk.Button(self)
        self.fontPageButton['text'] = "<<"
        self.fontPageButton['command'] = self.fontPage
        self.fontPageButton.grid(row=7, column=0)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=1, column=2, sticky='NS')
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=self.scrollbar.set, height=500)
        self.canvas.grid(row=1, column=1)

        self.bind("<MouseWheel>", self.canvasMouseWheelEvent)
        self.canvas.bind("<MouseWheel>", self.canvasMouseWheelEvent)
        self.scrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior,\
                                                anchor='nw')
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior) 

        def __window_size_change(event):
            self.canvas.configure(height=self.master.winfo_height() - 84)
        self.master.bind('<Configure>', __window_size_change)

    def openFile(self) :
        if self.haveNaxt[1] == True :
            Mbox("Info", "Operation is not ended")
            return
        file = filedialog.askopenfilename(filetypes=(("Json files", "*.json"), ))
        if file == "":
            return

        self.makeViewIndexLock.acquire()
        try :
            self.illustList = json.load(open(file, 'rt', encoding='utf-8'))
        except :
            Mbox("Error", "this is not a json file", 0)
            self.makeViewIndexLock.release()
            return

        try:
            self.illustList[0]['artistName']
            self.illustList[0]['illustName']
            self.illustList[0]['illustNum']
            self.illustList[0]['smallImageFileName']
            self.illustList[0]['hugeImageFileName']
            self.illustList[0]['book_num']
            self.illustList[0]['illustUrl']
            self.illustList[0]['smallImgUrl']
        except NameError:
            Mbox("Error", "file error", 0)
            self.illustList=[]
            self.makeViewIndexLock.release()
            return
        self.makeViewIndexLock.release()
        self.input.delete(0, len(self.input.get()))
        self.input.insert(0, os.path.splitext(basename(file))[0])
        self._flushPage(1)

    def login(self):

        def makeOpener(head = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xmlk, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Referer':'http://www.pixiv.net/'
        }, cookiejar = http.cookiejar.CookieJar()):
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            handler = urllib.request.HTTPSHandler(context=context)
            opener = urllib.request.build_opener(handler, urllib.request.HTTPCookieProcessor(cookiejar))
            header = []
            for key, value in head.items():
                elem = (key, value)
                header.append(elem)
            opener.addheaders = header
            return opener

        #login to pixiv
        id = 'thisismyxxx24@gmail.com'
        passwd = '3d1e2aehky2qwfui20vz'

        loginList = {
            'return_to' : 'https://www.pixiv.net/',
            'pixiv_id' : id,
            'password' : passwd,
            'ref' : '',
            'source' : 'accounts',
            'captcha' : '',
            'g_recaptcha_response': '',
            'post_key' : ''
        }

        cj = http.cookiejar.CookieJar()
        self.opener = makeOpener(cookiejar=cj)
        res = self.opener.open(loginpage)
        soup = BeautifulSoup(res.read(), 'html.parser')
        find = soup.find('input', attrs = {'name' : 'post_key'})
        post_key = find.attrs['value']
        loginList['post_key'] = post_key

        postData = urllib.parse.urlencode(loginList).encode()
        self.opener.open(loginposturl, postData)

    def searchStart(self):
        searchStr = self.input.get()
        if not self.haveNaxt[1] and searchStr is not '':
            url = 'https://www.pixiv.net/search.php?word=' + urllib.parse.quote(searchStr) + '&order=date_d'
            if self.r18ModeCheckButtonVar.get() ^ self.safeModeCheckButtonVar.get() == 0:
                self.fileFloderName=""
                pass
            elif self.r18ModeCheckButtonVar.get() == 1:
                url += '&mode=r18'
                self.fileFloderName="_r18"
            elif self.safeModeCheckButtonVar.get() == 1:
                url += '&mode=safe'
                self.fileFloderName="_safe"

            self.haveNaxt[0] = True
            self.haveNaxt[1] = True
            self.illustList = []
            self._flushPage(1)
            threading._start_new_thread(self.makeillustList, (url, searchStr, ))
        
    def _make_illust_list(self, imageItems, searchStr):
        if (not(os.path.exists('./' + searchStr + self.fileFloderName + '/'))):
            os.makedirs('./' + searchStr + self.fileFloderName +'/')
        if (not(os.path.exists('./' + searchStr + self.fileFloderName + '/huge'))):
            os.makedirs('./' + searchStr + self.fileFloderName + '/huge')
    
        infos = json.loads(imageItems.find('input', id='js-mount-point-search-result-list')['data-items']);
        for info in infos:
        
            artistName          = info['userName']
            illustName          = info['illustTitle']
            illustNum           = info['illustId']
            filename            = re.sub(r"[\\\*\?/|<>:\"\x00-\x1F]", ".", artistName + '-' + illustName + '-' + str(illustNum))
            smallImageFileName  = './'+ searchStr + self.fileFloderName +'/' + filename + '.jpg'
            hugeImageFileName   = './' + searchStr + self.fileFloderName + '/huge/' + filename + '.png'
            book_num            = info['bookmarkCount']
            smallImgUrl         = info['url']

            print(book_num)
            self.illustList.append(
                              {'artistName' : artistName,   'illustName'            : illustName,\
                               'illustNum'  : illustNum,    'smallImageFileName'    : smallImageFileName, 'hugeImageFileName' : hugeImageFileName, \
                               'book_num'   : book_num,     'illustUrl'             : 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(illustNum),
                               'smallImgUrl': smallImgUrl}
                )
                                                            #use thread to open it

    def makeillustList(self, url, searchStr):
        searchStr = self.input.get()
        searchStr = re.sub(r"[\\\*\?/|<>:\"\x00-\x1F]", "", searchStr)
        response = None
        while True:
            while True:
                try:
                    response = self.opener.open(url, timeout=2)
                    soup = BeautifulSoup(response.read(), 'html.parser')
                    break;
                except :
                    continue

            self._make_illust_list(soup, searchStr)
            nextPage = soup.find('a', {'rel' : 'next'}, class_='_button')
            if nextPage is None :
                break
            url = searchUrl + nextPage['href']
        self.haveNaxt[0] = False

        while not self.haveNaxt[1]:
            time.sleep(1)
        self.illustList = sorted(self.illustList, key=getKey, reverse=True)
        f = open(searchStr + self.fileFloderName + '.json', 'wt', encoding='utf-8')
        s = json.dumps(self.illustList, ensure_ascii=False)
        f.write(s)
        f.close()
        i = 0
        print('sorting')
        frame._flushPage(1)
        Mbox("OK", "Search Finish", 0)
        print('finish')
        self.haveNaxt[1] = False
        
    def minBookNumTrace(self, *args):
        self.minBookNumStringVar.set(re.sub(r'[^0-9]', '', self.minBookNumStringVar.get()))

    def nextPage(self):
        if self.imagesPerPage + self.makeViewIndex > len(self.illustList):
            Mbox("Info", "this is the last page", 0)
            return 

        self.makeViewIndexLock.acquire()
        self.canvas.yview_moveto(0)
        self.resetMakeViewFunction = True
        self.makeViewIndex += self.imagesPerPage
        self.makeViewIndexLock.release()

    def fontPage(self):
        if self.makeViewIndex - self.imagesPerPage < 0:
            Mbox("Info", "this is the home page", 0)
            return 

        self.makeViewIndexLock.acquire()
        self.canvas.yview_moveto(0)
        self.resetMakeViewFunction = True
        self.makeViewIndex -= self.imagesPerPage
        self.makeViewIndexLock.release()

    def setPage(self, pageIndex):
        if self.imagesPerPage * (pageIndex - 1) < 0 or self.imagesPerPage * (pageIndex - 1) > len(self.illustList) :
            Mbox("Info", "Error page index", 0)
            return
        if self.imagesPerPage * (pageIndex - 1) == self.makeViewIndex :
            return
        
        self.makeViewIndexLock.acquire()
        self.canvas.yview_moveto(0)
        self.resetMakeViewFunction = True
        self.makeViewIndex = self.imagesPerPage * (pageIndex - 1)
        self.makeViewIndexLock.release()

    def _flushPage(self, pageIndex) :
        if self.imagesPerPage * (pageIndex - 1) < 0 or self.imagesPerPage * (pageIndex - 1) > len(self.illustList) :
            Mbox("Info", "Error page index", 0)
            return
        
        self.makeViewIndexLock.acquire()
        self.canvas.yview_moveto(0)
        self.resetMakeViewFunction = True
        self.makeViewIndex = self.imagesPerPage * (pageIndex - 1)
        self.makeViewIndexLock.release()

    def makeView(self):

        def loadImages(illustinfo, index):
            if (not(os.path.isfile(illustinfo['smallImageFileName']))):
                arr = np.asarray(bytearray(self.opener.open(illustinfo['smallImgUrl']).read()), dtype=np.uint8)
                img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                arr.tofile(illustinfo['smallImageFileName'])
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                d = ImageDraw.Draw(img)
                if len(img.mode) < 3 :
                    color=(255)
                else :
                    color=(255,0,0,0)
                d.text((img.width / 2, img.height/ 2 * 1.5), str(illustinfo['book_num']), fill=color, font=ImageFont.truetype(font_type, size=40))
                del d
                self.tkImage[index] = ImageTk.PhotoImage(img)
                self.buttons[index]['image'] = self.tkImage[index]
            else:
                img = Image.open(illustinfo['smallImageFileName'])
                d = ImageDraw.Draw(img)
                if len(img.mode) < 3:
                    color=(255)
                else :
                    color=(255,0,0,0)
                d.text((img.width / 2, img.height/ 2 * 1.5), str(illustinfo['book_num']), fill=color, font=ImageFont.truetype(font_type, size=40))
                del d
                self.tkImage[index] = ImageTk.PhotoImage(img)
                self.buttons[index]['image'] = self.tkImage[index]

            self.makeViewThreadNumLock.acquire()
            self.imageThreadNum -= 1
            self.makeViewThreadNumLock.release()

        i = 0
        while True:

            self.makeViewIndexLock.acquire()
            if self.resetMakeViewFunction :
                i = 0
                self.resetMakeViewFunction = False
            self.makeViewIndexLock.release()

            if self.imageThreadNum >= self.maxImageThread or not i < self.imagesPerPage or not i + self.makeViewIndex < len(self.illustList):
                time.sleep(0.2)
                continue

            #self.makeViewIndexLock.acquire()
            if i < len(self.buttons):
                self.buttons[i]['command'] = lambda illustInfo = self.illustList[i + self.makeViewIndex] : threading._start_new_thread(self.showImage, (illustInfo, ))
                if self.buttons[i]['image'] == '':
                    self.buttons[i]['image'] = self.tkImage[i]
            else:
                self.buttons.append(tk.Button(self.interior, height=200,
                                                width=200,
                                                image=self.tkImage[i],
                                                command=lambda illustInfo = self.illustList[i + self.makeViewIndex] : threading._start_new_thread(self.showImage, (illustInfo, ))))
                self.buttons[i].grid(row=int(i/5), column=i%5)
                self.buttons[i].bind("<MouseWheel>", self.canvasMouseWheelEvent)

            self.buttons[i].bind("<Button-3>", lambda event, illlustUrl=self.illustList[i + self.makeViewIndex]['illustUrl'] : self.cloneTextToClipboard(illlustUrl))
            self.makeViewThreadNumLock.acquire()
            self.imageThreadNum += 1
            threading._start_new_thread(loadImages, (self.illustList[i + self.makeViewIndex], i))
            self.makeViewThreadNumLock.release()

            #self.makeViewIndexLock.release()
            i = i + 1

    def cloneTextToClipboard(self, text) :
        self.clipboard_clear()
        self.clipboard_append(text)
        Mbox("ok", "cloned url", 0)

    def singalImage(self, findres):
        arr = np.asarray(bytearray(self.opener.open(findres).read()), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return img

    def showImage(self, illustInfo):

        def computeWidthAndHeight(imgWidth, imgHeight, maxWidth, maxHeight):
            width = 0
            height = 0
            if imgWidth > imgHeight :
                width = maxWidth
                height = imgHeight / imgWidth * maxWidth
                pass
            else :
                width = imgWidth / imgHeight * maxHeight
                height = maxHeight
                pass
            return (int(width), int(height))

        def showImage(img, filename):
            cv2.namedWindow(filename, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO);
            imgsize = computeWidthAndHeight(len(img[0]), len(img), self.master.winfo_screenwidth() / 2, self.master.winfo_screenheight())
            cv2.resizeWindow(filename, imgsize)
            cv2.moveWindow(filename, 0, 0)
            cv2.imshow(filename, img)
            cv2.waitKey(-1)
            cv2.destroyWindow(filename)

        filename = illustInfo['hugeImageFileName']
        if (not(os.path.isfile(filename))):
            if 'PageCount' not in illustInfo:
                response = self.opener.open('http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(illustInfo['illustNum']))
                data  = response.read().decode('utf-8')
                if not data.find('ugoira') == -1:
                    illustInfo['PageCount'] = -1
                    Mbox("Sorry", "I can not show gif, illust id is " + str(illustInfo['illustNum']), 0)
                    return

                start = data.find('"' + str(illustInfo['illustNum']) + '":')
                start = data[start:].find('"pageCount":') + start + 12
                end   = data[start:].find(',') + start
                illustInfo['PageCount'] = int(data[start:end])

            if illustInfo['PageCount'] == -1:
                Mbox("Sorry", "I can not show gif, illust id is " + str(illustInfo['illustNum']), 0)
                return

            #normal image
            if illustInfo['PageCount'] == 1:
                start = data.find('"original":"') + 12
                end   = data[start:].find('"') + start
                img = self.singalImage(data[start:end].replace('\\', ''))
                cv2.imencode('.png', img)[1].tofile(filename)
                showImage(img, filename)
                return

            filenameList = []
            imageUrlList = []
            for i in range(illustInfo['PageCount']):
                if i == 0:
                    fn=filename
                else:
                    fn = filename[0 : len(filename) - 4] + '-' + str(i) + filename[len(filename) - 4 : len(filename)] # <filename> - <str(i)> .png

                filenameList.append(fn)
                imageUrlList.append('https://www.pixiv.net/member_illust.php?mode=manga_big&illust_id='+str(illustInfo['illustNum'])+'&page='+str(i))
                i = i + 1

            multiImageBox = MultiImageBox(self.master, self.opener, imageUrlList, filenameList)
            #threading._start_new_thread(multiImageBox.mainloop, ())
            return

        if os.path.isfile(filename[0 : len(filename) - 4] + '-' + str(1) + filename[len(filename) - 4 : len(filename)]) :
            filenameList = [filename]
            __filename = filename[0 : len(filename) - 4] + '-'
            __extenstion = filename[len(filename) - 4 : len(filename)]
            i = 1
            while os.path.isfile(__filename + str(i) + __extenstion) :
                filenameList.append(__filename + str(i) + __extenstion)
                i += 1

            imageUrlList = [None] * len(filenameList)
            multiImageBox = MultiImageBox(self.master, self.opener, imageUrlList, filenameList)
            return
        img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), cv2.IMREAD_COLOR)
        showImage(img, filename)
        cv2.waitKey(-1)
        cv2.destroyWindow(filename)

    def saveAllImages(self, minBookNum):
        global limit
        global threadLines
        global nowThreadLines

        def saveImage(illustInfo):
            global nowThreadLines
            filename = illustInfo['hugeImageFileName']
            if (not(os.path.isfile(filename))):
                if 'PageCount' not in illustInfo:
                    while True:
                        try:
                            response = self.opener.open('http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(illustInfo['illustNum']), timeout=4)
                            data  = response.read().decode('utf-8')
                            break
                        except (urllib.error.URLError, socket.timeout) as e:
                            continue
                    if not data.find('ugoira') == -1:
                        illustInfo['PageCount'] = -1
                        nowThreadLines -= 1
                        return

                    start = data.find('"' + str(illustInfo['illustNum']) + '":')
                    start = data[start:].find('"pageCount":') + start + 12
                    end   = data[start:].find(',') + start
                    illustInfo['PageCount'] = int(data[start:end])

                if illustInfo['PageCount'] == 1:
                    start = data.find('"original":"') + 12
                    end   = data[start:].find('"') + start
                    img = self.singalImage(data[start:end].replace('\\', ''))
                    cv2.imencode('.png', img)[1].tofile(filename)
                    print("saving " + str(illustInfo['illustNum']))
                    nowThreadLines -= 1
                    return

                for i in range(illustInfo['PageCount']):
                    if i == 0:
                        fn = filename
                    else:
                        fn = filename[0 : len(filename) - 4] + '-' + str(i) + filename[len(filename) - 4 : len(filename)]
                    if (not (os.path.isfile(fn))):
                        while True:
                            try:
                                res = self.opener.open('https://www.pixiv.net/member_illust.php?mode=manga_big&illust_id='+str(illustInfo['illustNum'])+'&page='+str(i))
                                soup = BeautifulSoup(res.read(), 'html.parser')
                                break
                            except urllib.error.HTTPError:
                                continue
                        print("saving " + str(illustInfo['illustNum']) + '-' + str(i))
                        find = soup.find('img')
                        byteIO = io.BytesIO(self.opener.open(find.attrs['src']).read());
                        img = (Image.open(byteIO))
                        img.convert('RGBA')
                        img.save(fn)
                        byteIO.close()
                nowThreadLines -= 1
                return
            nowThreadLines -= 1

        if minBookNum == "" or int(minBookNum) == 0 :
            Mbox("Error", "Please input book number", 0)
            return

        minBookNum = int(minBookNum)

        if self.haveNaxt[1] is True:
            Mbox("Error", "Operation has not ended", 0)
            return;
        self.haveNaxt[1] = True
        index = 0
        while index < limit and index < len(self.illustList) and self.illustList[index]['book_num'] > minBookNum:
            if nowThreadLines > threadLines:
                time.sleep(2)
            else:
                nowThreadLines += 1
                threading._start_new_thread(saveImage, (self.illustList[index],))
                index += 1
        Mbox("Successful", "Save All Images", 0);
        self.haveNaxt[1] = False

root = tk.Tk()
root.resizable(False,True)
frame = Application(master=root)
frame.mainloop()
