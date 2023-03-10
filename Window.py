from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from PIL import ImageTk, Image

from Recognizer import *


class Window(Tk, ):
    def __init__(self):
        super(Window, self).__init__()
        self.title('Identification de logo')
        self.resizable(False, False)
        self.geometry('800x800')
        self.labelFrame = ttk.LabelFrame(self, text="Choisir une image")
        self.input()
        self.set_button()

    def input(self):
        font = ('Calibri 10')
        label = ttk.Label(self, text='Répertoire où se trouvent les logos à identifier puis sélectionner une image :',
                          width=80, font=font)
        label.grid(column=1, row=0, padx=10, pady=20)
        self.images_path = ttk.Entry(self, width=40)
        self.images_path.insert(0, "./images_library")
        self.images_path.grid(column=1, row=1, pady=0)

    def set_button(self):
        self.button = ttk.Button(self, text="Choisir une image", command=self.file_dialog)
        self.button.grid(column=1, row=2, padx=350, pady=20)

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="./", title="Sélectionnez une image", filetypes=(
            ("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("JPG files", "*.jpg"), ("ALL files", "*.*")))
        self.show_image()
        self.recognizer = Recognizer(self.filename, self.images_path)
        self.show_text()

    def show_image(self):
        self.load = Image.open(self.filename)
        self.render = ImageTk.PhotoImage(self.load.resize((500, 500), Image.ANTIALIAS))
        self.img = Label(self, image=self.render)
        self.img.image = self.render
        self.img.grid(column=1, row=3, padx=50, pady=0)

    def show_text(self):
        font = ('Calibri 18 bold')
        self.text = Label(self, text=self.recognizer.type, font=font)
        self.text.grid(column=1, row=4, padx=50, pady=50)
