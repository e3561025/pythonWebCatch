from bs4 import BeautifulSoup
import requests
import tkinter as tk
import time
from PIL import Image,ImageTk
"""
text = requests.get('https://www.wnacg.org/albums-index-page-1-sname-cat.html').text

soup = BeautifulSoup(text,'lxml')
print(type(soup))
a=soup.find_all(class_='f_left paginator')[0]
print(a)
print(type(a))
print('\n\n\n')
b=BeautifulSoup(str(a),'lxml')

print(b.prettify())
print(type(b))
c = b.select('span.prev > a')
if(len(c)==0):
    print('沒有上一頁')

print(c)
"""
window = tk.Tk()
window.geometry('500x500')
lbvar =tk.StringVar()
lbvar.set([11,22,33,44,66,88,22,4455,56])

lb = tk.Listbox(window,listvariable=lbvar)
lb.insert('end',10)
lb.insert('end',10)
lb.insert('end',10)
lb.insert('end',10)

def btnfun():
    lb.delete(0,'end')

btn = tk.Button(window,textvariable=tk.StringVar(value='clear'),command=btnfun)
btn.pack()
mylist=[20,3,4,5,68,9,25]
lb.insert('end',mylist)

#lb.delete(0,'end')
lb.insert('end',15)
lb.pack()

label  =tk.Label(window,width=20,bg='#000000')

path = './0ba5b9816cd0d2716d999837af784cf9.JPG'
pic = Image.open(path).resize((150,300),Image.ANTIALIAS)
flag = ImageTk.PhotoImage(pic)
label.config(image=flag)
label.pack(ipady=80)
window.mainloop()
