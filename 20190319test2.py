import tkinter as tk
import numpy
from tkinter import ttk
root = tk.Tk()
root.title('wnacg-download')
root.geometry('200x200')
#root.resizable() #禁止使用者調整大小
label = ttk.Label(root,text='hello world')
label.pack() #pack是由上往下擺放
#label.grid(column=0,row=0)
count=0
def clickOK():
    global count
    count = count+1
    label.configure(text='Click OK '+str(count)+' times')
button = ttk.Button(root,text='OK',command=clickOK)
button.pack()
#button.grid(column=1,row=0)



root.mainloop()

