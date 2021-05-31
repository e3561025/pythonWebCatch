import os
import tkinter

root = tkinter.Tk()
root.geometry('500x500')
L = tkinter.Listbox(root,selectmode=tkinter.SINGLE)
gifsdict = {}

dirpath = 'D:\\python_Test\\python-design\\picture\\'
for gifname in os.listdir(dirpath):
    if not gifname[0].isdigit(): 
       continue
    print(gifname)
    gifpath = os.path.join(dirpath, gifname)
    gif = tkinter.PhotoImage(file=gifpath)
    gifsdict[gifname] = gif
    L.insert(tkinter.END, gifname)

L.pack()
img = tkinter.Label(root,width=20,height=20)
img.pack()
def list_entry_clicked(*ignore):
    imgname = L.get(L.curselection()[0])
    img.config(image=gifsdict[imgname])
L.bind('<ButtonRelease-1>', list_entry_clicked)
root.mainloop()
