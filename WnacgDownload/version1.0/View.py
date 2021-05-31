import tkinter as tk
from  Catch import webCatch
from io import BytesIO
from PIL import Image,ImageTk
import os
import tkinter.filedialog as filedialog
catch = webCatch()
#創建底板
"""
----------------------------------window
    _________________________
    |Entry-儲存位址          |  --path
    ___________  ____________
    |Entry-搜尋| |Button-下載|  -----fr1(search , down)

    _________________  ______
    |               | |Label | -----fr2(lb , fr3)
    |               | |圖片  |              fr3( pic , nextPage)
    | Listbox       | |______|
    | 漫畫列表       | |btn-  |
    |               | |下一頁 |
    |_______________| |______|

----------------------------------

"""
window = tk.Tk()
window.title('wnacg-download')
window.geometry('1000x500')

frPath = tk.Frame(window)
fr1 = tk.Frame(window)
fr2 = tk.Frame(window)

#儲存檔案的路徑
pathText = tk.StringVar()
pathText.set('path')
path = tk.Entry(frPath,textvariable=pathText,width=115,bg='#71c2ff')


    
pathbtnText = tk.StringVar()
pathbtnText.set('path-choose')
def pathChoose():
    select = filedialog.askdirectory()
    pathText.set(select)
pathbtn = tk.Button(frPath,textvariable=pathbtnText,width=20,command=pathChoose)


#listbox 列出漫畫名稱的載具
lbVar = tk.StringVar()
lbVar.set([])
lb = tk.Listbox(fr2,width=100,bg='#e8fc74',listvariable=lbVar)

# fr3擺放 pic & nextpage
fr3 = tk.Frame(fr2)
pic = tk.Label(fr3,bg='black')


#lb監聽事件
def onselect(evt):
    select = lb.curselection()
    if(select!=tuple()):
        index = lb.index(lb.curselection())
        stream = catch.getPicture(index)
        #print(stream)
        picture = Image.open(BytesIO(stream))
        picture = picture.resize((222,296),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(picture)
        pic.config(image=photo)
        pic.image=photo
    #print('sssssssssssssssssss')
lb.bind('<<ListboxSelect>>',onselect)

# listbox 所選的index
index=-1

#搜尋的關鍵字 & 下載按鈕
searchText = tk.StringVar()
searchText.set('input the search')
search = tk.Entry(fr1,textvariable=searchText,width=110,bg='#96f394')
searchbtnText = tk.StringVar()
searchbtnText.set('search')
def searchClick():
    lb.delete(0,'end')
    text = search.get()
    urllist=catch.search(text)
    print('start search')
    for i in urllist:
        #print(i)
        lb.insert('end',i)
searchbtn = tk.Button(fr1,textvariable=searchbtnText,width=10,bg='#eea980',command=searchClick)

#換上一頁使用函數
def prePageFunction():
    prelist=catch.nextOrPre(0)
    if(prelist!=[]):
        lb.delete(0,'end')
        for i in prelist:
            lb.insert('end',i)
#換下一頁使用函數
def nextPageFunction():
    nextlist=catch.nextOrPre(1)
    #print(nextlist)
    if(nextlist!=[]):
        lb.delete(0,'end')
        for i in nextlist:
            lb.insert('end',i)
def clear():
    lb.delete(0,'end')

#fr4--上一頁+下一頁+clear btn
fr4 = tk.Frame(window)
#換上一頁
prePageText = tk.StringVar(value='上一頁')
prePage = tk.Button(fr4,textvariable=prePageText,width=10,bg='#96f394',command=prePageFunction)
#換下一頁
nextPageText = tk.StringVar(value='下一頁')
nextPage = tk.Button(fr4,width=10,bg='#96f394',textvariable=nextPageText,command=nextPageFunction)
#Clear
clearText = tk.StringVar(value='clear')
clearbtn = tk.Button(fr4,width=10,bg='#96f394',textvariable=clearText,command=clear)

#下載選取的listbox index
def listChoose():
    if(os.path.exists(path.get())):
        index=lb.index(lb.curselection())
        catch.choose(index,path.get())
    else :
        pathText.set(path.get()+'***your path is not exist!!!***')
down = tk.Button(fr1,text='download',width=10,bg='#eea980',command=listChoose)

#擺放位置
path.grid(column=0,row=0)
pathbtn.grid(column=1,row=0)
frPath.place(x=0,y=0)


search.grid(column=0,row=0)
searchbtn.grid(column=1,row=0,padx=3)
down.grid(column=2,row=0,padx=3)
fr1.place(x=5,y=25)


pic.pack(ipady=30)
prePage.grid(column=0,row=0,ipadx=10)
nextPage.grid(column=1,row=0,ipadx=10,padx=10)
clearbtn.grid(column=2,row=0,ipadx=10)

lb.pack(side='left',anchor='nw',ipady=100)
fr3.pack(side='right',anchor='ne',padx=10)
fr2.place(x=5,y=65)
fr4.place(x=5,y=450)
window.mainloop()