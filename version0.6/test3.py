
import requests
from PIL import ImageTk, Image
from io import BytesIO
import tkinter as tk

window = tk.Tk()
lb = tk.Listbox(window)
lb.insert('end',10)
lb.insert('end',20)
lb.insert('end',30)
lb.insert('end',40)

def onselect(evt):
    w = evt.widget
    print(w)
    index = lb.index(lb.curselection())
    print(type(index))
    print(index)
    value = w.get(index)
    print(str(index)+'ssssssss')

lb.bind('<<ListboxSelect>>',onselect)
lb.pack()

window.mainloop()