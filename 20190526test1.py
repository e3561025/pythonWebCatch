import tkinter as tk
from PIL import Image,ImageTk
window = tk.Tk()
window.geometry('700x700')
canvas  = tk.Canvas(window,bg='#00ff80',width=620,height=620,scrollregion=(0,0,700,700))
frame= tk.Frame(canvas,bg='#71c2ff')
vbar = tk.Scrollbar(canvas,orient=tk.VERTICAL)
vbar.place(x=500,width=20,height=500)
vbar.configure(command=canvas.yview)
hbar = tk.Scrollbar(canvas,orient=tk.HORIZONTAL)
hbar.place(x =0,y=500,width=500,height=20)
hbar.configure(command=canvas.xview)
canvas.config(xscrollcommand=hbar.set,yscrollcommand=vbar.set)
#canvas.create_window((0,0),window=frame)
for i in range(0,10):
    btn = tk.Button(frame,text='ss')
    btn.pack()
frame.place(x=0,y=0,width=500,height=500)
canvas.pack()

window.mainloop()
