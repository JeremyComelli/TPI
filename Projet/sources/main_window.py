from tkinter import *
import tkinter.filedialog as filedialog
from PIL import Image

#todo faire marcher PIL
class MainWindow:
    def __init__(self, conf):
        self.config = conf

        self.window_name = self.config['window_name']
        self.window_size = self.config['window_size']
        self.main_ui = Tk()
        self.main_ui.title(self.window_name)
        self.main_ui.geometry(self.window_size)

        self.filetypes = [("PNG", "*.png"), ("JPG", "*.jpg")]

        self.label_value = StringVar()
        self.label_value.set("AAAAAAAAAAAAH")

        self.cv = Canvas()
        self.cv.pack()

        self.label = Label(self.main_ui, textvariable=self.label_value)
        self.label.pack()

        button_open = Button(self.main_ui, text="Open File", command=self.open_select_dialog)
        button_open.pack()

        pic = Image.open("C:\\Users\\Jeremy.COMELLI\\Desktop\\Screenshot_2.png", "r")
        self.cv.create_image(10, 10, image=pic)

        self.main_ui.mainloop()

    def open_select_dialog(self):
        self.main_ui.filename = filedialog.askopenfilename(filetypes=self.filetypes)
        print("button clicked")
        self.label_value.set(self.main_ui.filename)

    def load_image(self, path):
        pic = open(path)

