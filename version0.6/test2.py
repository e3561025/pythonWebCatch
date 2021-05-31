
import requests
from PIL import ImageTk, Image
from io import BytesIO
import tkinter as tk
import test2_1
window = tk.Tk()

a = test2_1.A()

stream = a.a()
pic = Image.open(BytesIO(stream))
pic = pic.resize((50,100),Image.ANTIALIAS)
picture = ImageTk.PhotoImage(pic)

label = tk.Label(window,bg='#000000')
label.config(image=picture)
label.pack()
window.mainloop()
"""
import tkinter as tk
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO
 
root = tk.Tk()
img_url = "https://www.wnacg.org//t2.wnacg.download/data/t/0721/17/15526021386717.jpg"
response = requests.get(img_url)
img_data = response.content
img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
panel = tk.Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")
root.mainloop()

"""