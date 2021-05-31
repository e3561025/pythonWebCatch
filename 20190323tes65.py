from tkinter import *

root = Tk()
root.title('Model Definition')
root.resizable(width=FALSE, height=FALSE)
root.geometry('{}x{}'.format(460, 350))

top_frame = Frame(root, bg='cyan', width = 450, height=50, pady=3).grid(row=0, columnspan=3)
Label(top_frame, text = 'Model Dimensions').grid(row = 0, columnspan = 3)
Label(top_frame, text = 'Width:').grid(row = 1, column = 0)
Label(top_frame, text = 'Length:').grid(row = 1, column = 2)
entry_W = Entry(top_frame).grid(row = 1, column = 1)
entry_L = Entry(top_frame).grid(row = 1, column = 3)
#Label(top_frame, text = '').grid(row = 2, column = 2)

center = Frame(root, bg='gray2', width=50, height=40, padx=3, pady=3).grid(row=1, columnspan=3)
ctr_left = Frame(center, bg='blue', width=100, height=190).grid(column = 0, row = 1, rowspan = 2)
ctr_mid = Frame(center, bg='yellow', width=250, height=190, padx=3, pady=3).grid(column = 1, row=1, rowspan=2)
ctr_right = Frame(center, bg='green', width=100, height=190, padx=3, pady=3).grid(column = 2, row=1, rowspan=2)

btm_frame = Frame(root, bg='white', width = 450, height = 45, pady=3).grid(row = 3, columnspan = 3)
btm_frame2 = Frame(root, bg='lavender', width = 450, height = 60, pady=3).grid(row = 4, columnspan = 3)


root.mainloop()