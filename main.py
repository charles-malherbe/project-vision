from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

class Window(Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.title('Identification de fruits et légumes')
        self.resizable(False, False)
        self.geometry('800x800')
        self.iconbitmap('images/pics.ico')

        self.labelFrame = ttk.LabelFrame(self, text = "Choisir une image")
        self.button()


    def button(self):
        self.button = ttk.Button(self, text = "Choisir une image", command = self.fileDialog)
        self.button.grid(column = 1, row = 1, padx = 350, pady = 50)


    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir =  "/", title = "Sélectionnez une image", filetype = (("jpeg files","*.jpg"),("all files","*.*")) )

root = Window()
root.mainloop()