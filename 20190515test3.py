class num:
    a=0
    def add(self):
        self.a=self.a+1
        return self.a
    def get(self):
        return self.a
import tkinter as tk

window  = tk.Tk()
a = num()

labelList=[]
for i in range(0,10):
    label = tk.Label(window,text=('test'+str(a.get())))
    a.add()
    labelList.append(label)
    label.pack()
def close():
    if len(labelList)!=0:
        labelList[0].destroy()
        labelList.remove(labelList[0])
btn = tk.Button(window,command=close,text='btnClose')
btn.pack()
def add():
    label = tk.Label(window,text=('test'+str(a.get())))
    a.add()
    labelList.append(label)
    label.pack()
btnAdd = tk.Button(window,command=add,text='btnAdd')
btnAdd.pack()
window.mainloop()
