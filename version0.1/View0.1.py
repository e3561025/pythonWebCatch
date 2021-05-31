import tkinter as tk

window = tk.Tk()
window.title('wnacg-download')
window.geometry('500x500')
fr1 = tk.Frame(window)
fr2 = tk.Frame(window)

pathText = tk.StringVar()
pathText.set('path')
path = tk.Entry(window,textvariable=pathText,width=53,bg='#71c2ff')
path.place(x=5,y=5)

searchText = tk.StringVar()
searchText.set('input the search')
search = tk.Entry(fr1,textvariable=searchText,width=40,bg='#96f394')
down = tk.Button(fr1,text='download',width=10,bg='#eea980')
search.grid(column=0,row=0)
down.grid(column=1,row=0,padx=10)
fr1.place(x=5,y=25)

#取得選取的listbox index
def printChoose():
    print(lb.index(lb.curselection()))
lb = tk.Listbox(fr2,width=40,bg='#e8fc74')
fr3 = tk.Frame(fr2,width=20)
pic = tk.Label(fr3,width=10,bg='#000000')
nextPage = tk.Button(fr3,width=10,bg='#96f394')
pic.pack(side='top',ipady=40,pady=10)
nextPage.pack(ipady=10)

lb.pack(side='left',anchor='w',ipady=100)
fr3.pack(side='right',anchor='ne',padx=10)
fr2.place(x=5,y=65)

