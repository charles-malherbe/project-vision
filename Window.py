from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from Recognizer import *

class Window(Tk, ):
    def __init__(self):
        super(Window, self).__init__()
        # Répertoire des images à comparer
        self.images_path = "images_library"
        self.title('Identification de logo')
        self.resizable(False, False)
        self.geometry('800x800')
        self.iconbitmap('includes/icon.ico')
        self.labelFrame = ttk.LabelFrame(self, text="Choisir une image")
        self.button()

    def button(self):
        self.button = ttk.Button(self, text="Choisir une image", command=self.file_dialog)
        self.button.grid(column=1, row=1, padx=350, pady=50)

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Sélectionnez une image", filetype=(
        ("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("JPG files", "*.jpg"), ("ALL files", "*.*")))
        self.show_image()
        self.recognizer = Recognizer(self.filename, self.images_path)
        self.show_text()

    def show_image(self):
        self.load = Image.open(self.filename)
        self.render = ImageTk.PhotoImage(self.load.resize((500, 500), Image.ANTIALIAS))
        self.img = Label(self, image=self.render)
        self.img.image = self.render
        self.img.grid(column=1, row=2, padx=50, pady=0)

    def show_text(self):
        font = ('Calibri 18 bold')
        self.text = Label(self, text=self.recognizer.type, font=font)
        self.text.grid(column=1, row=3, padx=50, pady=50)