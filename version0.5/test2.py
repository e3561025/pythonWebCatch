
import requests
from PIL import ImageTk, Image
from io import BytesIO
import tkinter as tk

window = tk.Tk()
data=requests.get('https://www.wnacg.org//t2.wnacg.download/data/t/0721/17/15526021386717.jpg')
stream = data.content
#pic = Image.open(BytesIO(stream))
picture = ImageTk.PhotoImage(Image.open(BytesIO(stream)))

label = tk.Label(window)
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