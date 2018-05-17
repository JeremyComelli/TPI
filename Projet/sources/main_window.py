from tkinter import *
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk


class MainWindow:
    def __init__(self, conf):
        self.config = conf

        self.window_name = self.config['window_name']
        self.window_size = self.config['window_size']

        # Accepted files for the program
        self.filetypes = [("Fichiers JPEG & PNG", ("*.jpg", "*.png"))]

        # Work area size
        self.wa_width, self.wa_height = str.split(self.config['work_area_dimensions'], ",")

        # Menu width
        self.menu_width = self.config['menu_width']

        # Instanciating main window (root)
        self.root = Tk()
        self.root.title(self.window_name)
        self.root.resizable(False, False)
        self.root.geometry(self.window_size)

        # Main window has focus by default
        self.root.focus_set()
        # Binding esc key to a function that halts the program
        self.root.bind("<Escape>", self.close_window)

        # expand=True, fill=BOTH
        '''self.label_value = StringVar()
        self.label_value.set("This is a label")
        self.label = Label(self.root, textvariable=self.label_value)
        self.label.pack()'''

        # Instantiating widgets
        # TODO: pour l'instant, la fenêtre n'est pas resizable. Si elle le devient, il faudra trouver un moyen de faire marcher tout ça
        self.main_frame = Frame(self.root, width=400, bg="#8a0be5")
        self.menu_frame = Frame(self.root, bg="#48f442")
        self.cv = Canvas(self.main_frame, bg="#4286f4", height=self.wa_height, width=str(int(self.wa_width) - int(self.menu_width)))

        self.open_button = Button(self.menu_frame, text="Ouvrir...", command=self.open_select_dialog, width=22)
        self.save_button = Button(self.menu_frame, text="Enregistrer sous...", command=self.open_select_dialog, width=22)
        self.recognize_button = Button(self.menu_frame, text="Reconnaître la sélection", command=self.open_select_dialog, width=22)
        self.new_collage_button = Button(self.menu_frame, text="Nouveau Collage", command=self.open_select_dialog, width=22)

        # Placing widgets on the window
        self.main_frame.grid(column=0, row=0)
        self.menu_frame.grid(column=1, row=0, ipadx=20, ipady=20, sticky=N)
        self.cv.grid(column=0, row=0)
        self.open_button.grid(column=0, row=0, pady=5, rowspan=2, sticky=E)
        self.save_button.grid(column=0, row=2, pady=5, rowspan=2, sticky=E)
        self.recognize_button.grid(column=0, row=4, pady=5, rowspan=2, sticky=E)
        self.new_collage_button.grid(column=0, row=6, pady=5, rowspan=2, sticky=E)

        self.root.mainloop()

    def open_select_dialog(self):
        print("button clicked")
        self.load_image(filedialog.askopenfilename(filetypes=self.filetypes))

    def load_image(self, path):
        if path is not "":
            pic = Image.open(path, "r")
            self.root.picture = ImageTk.PhotoImage(pic)
            print("Image loaded")
            self.cv.create_image(50, 50, image=self.root.picture, anchor='nw')
            self.root.update_idletasks()
            self.root.update()

    @staticmethod
    def close_window(event):
        print("event registered")

        if event.keysym == "Escape":
            print("escape recognized")
            exit()
