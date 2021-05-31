import tkinter as tk
import time
window = tk.Tk()
window.title('my window')
window.geometry('375x200')

var1 = tk.StringVar()
label = tk.Label(window,bg='yellow',width=4,textvariable=var1)
label.pack()

var2 = tk.StringVar()
var2.set([11,22,33,44])

listbox = tk.Listbox(window,listvariable=var2)
def print_selection():
    value = listbox.get(listbox.curselection())
    var1.set(value)
btn1 = tk.Button(window,text='print selection',width=15,height=2,command=print_selection)
btn1.pack()
list_items=[1,2,3,4]
for item in list_items:
    listbox.insert('end',item)
listbox.insert(1,'first')
listbox.insert(2,'second')
listbox.pack()
listbox.delete(2)



window.mainloop()