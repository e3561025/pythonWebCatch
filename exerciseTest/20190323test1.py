import tkinter as tk

window = tk.Tk()
window.title('my window')
window.geometry('200x300')

e = tk.Entry(window,show='*')
e.pack()
t=tk.Text(window,height=2)
t.pack()

def insert_point():
    var = e.get()
    t.insert(1.0,var)#插入最前端
    t.insert('insert',var)#插入選取的位置
def insert_end():
    var = e.get()
    t.insert('end',var)#插入最後面

btn1 = tk.Button(window,text='insert point',width=15,height=2,command=insert_point)
btn1.pack()
btn2 = tk.Button(window,text='insert end',command=insert_end)
btn2.pack()

window.mainloop()