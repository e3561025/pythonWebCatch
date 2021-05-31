import img2pdf
import os
from PIL import Image

files = os.listdir()
files = sorted(files)
img=[]
for name in files:
    if(name.endswith("jpg") or name.endswith("png") or name.endswith("JPG") or name.endswith("PNG")):
        img.append(Image.open(name).convert('RGB'))

path = os.getcwd()
path = path.split("\\")
fileName = path[len(path)-1]
img1 = img[0]
img.pop(0)
img1.save(fileName+".pdf",save_all=True, append_images=img)
