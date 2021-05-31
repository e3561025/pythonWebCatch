import tkinter as tk

window = tk.Tk()
window.geometry('500x500')
fr1 = tk.Frame(window,width=100,height=50,bg='blue')
fr2 = tk.Frame(window,width=100,height=50,bg='red')

var1 = tk.StringVar()
var1.set('ssssssssssssss')
var2 = tk.StringVar()
var2.set('ttt')
btn1 = tk.Button(fr1,width=10,textvariable=var1)
btn2 = tk.Button(fr2,width=10,textvariable=var2)

btn1.place(x=0,y=0)
btn2.place(x=0,y=0)


fr1.place(x=0,y=0)
fr2.place(x=0,y=100)

window.mainloop()