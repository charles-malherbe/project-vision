def select_files():
    filetypes = (
        ('PNG files', '*.png'),
        ('JPEG files', '*.jpeg'),
        ('JPG files', '*.jpg'),
        ('All files', '*.*')
    )

    filenames = fd.askopenfilenames(
        title='Choisir un fichier',
        initialdir='/',
        filetypes=filetypes,
    )


open_button = tk.Button(
    root,
    text='Choisir une image',
    command=select_files,
)

open_button.pack(expand=True)