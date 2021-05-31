import tkinter as tk
import tkinter.filedialog as filedialog

class Voronoi_diagram:
    def __init__(self,window):
        window.title('Voronoi diagram')
        #window.geometry('600x1000')
        self.canvas = tk.Canvas(window,width=600,height=600,bg='white')
        divideButton = tk.Button(window,text='dividePoint',command=self.divide)
        stepByStepButton = tk.Button(window,text='step by step',command=self.stepByStep)
        clearButton = tk.Button(window,text='clear',command=self.clear)
        readButton = tk.Button(window,text='read',command=self.read)
        saveButton = tk.Button(window,text = 'save',command=self.save)
        self.canvas.pack()
        divideButton.pack()
        stepByStepButton.pack()
        clearButton.pack()
        readButton.pack()
        saveButton.pack()
        window.bind('<Button-1>',self.click)

        



    def divide(self):
        return 0
    def stepByStep(self):
       return 0
    def clear(self):
        self.canvas.delete('all')
        return 0
    def read(self):
        return 0
    def save(self):
        return 0
    def click(self,event):
        x=event.x
        y=event.y
        if x<=600 and y<=600:
            self.canvas.create_oval(x,y,x,y,width=3,fill='black')
            
        
        

window = tk.Tk()
Voronoi_diagram(window)
window.mainloop()