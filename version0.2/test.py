import tkinter as tk

window = tk.Tk()

a = tk.StringVar()
a.set('sssss')
text = tk.Entry(window,textvariable=a)

text.pack()
s = tk.StringVar()
s.set('aaaaa')
def btnclick():
    string = text.get()
    print(type(string))
    print(string)

btn = tk.Button(window,textvariable=s,command=btnclick)
btn.pack()



window.mainloop()