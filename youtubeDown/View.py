import tkinter as tk
import getVideo

video = getVideo.getVideo()
window = tk.Tk()
window.geometry('700x500')



radioList=[]
radioVar = tk.StringVar()
fr1 = tk.Frame(window,width=500,height=200)
fr2 = tk.Frame(window,width=500)

def create():

    for i in radioList:
        i.destroy()
    
    index=video.search(searchVar.get())
    for i in range(0,len(index)):
        radio = tk.Radiobutton(fr2,variable=radioVar,text=str(index[i]),value=i)
        radio.pack(anchor='w')
        radioList.append(radio)
def down():
    video.down(int(radioVar.get()),pathVar.get())
searchVar = tk.StringVar(value='search url')
search = tk.Entry(fr1,width=50,textvariable=searchVar)
pathVar = tk.StringVar(value='path')
path = tk.Entry(fr1,width=50,textvariable=pathVar)
searchbtnText = tk.StringVar(value='search')
searchbtn = tk.Button(fr1,textvariable=searchbtnText,command=create)
downText = tk.StringVar(value='down')
down = tk.Button(fr1,textvariable=downText,command=down)

search.grid(column=0,row=0,sticky='w')
path.grid(column=0,row=1,sticky='w')
searchbtn.grid(column=1,row=0,sticky='e',padx=5,pady=5)
down.grid(column=1,row=1,sticky='e',padx=5)
fr1.pack(pady=10)
fr2.pack(ipadx=500,ipady=300)


window.mainloop()