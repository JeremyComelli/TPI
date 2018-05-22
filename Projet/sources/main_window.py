from tkinter import *
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
from random import shuffle
from PIL import ImageGrab


def groups(glist, numPerGroup=2):
    result = []
    i = 0
    cur = []
    for item in glist:
        if not i < numPerGroup:
            result.append(cur)
            cur = []
            i = 0
        cur.append(item)
        i += 1
    if cur:
        result.append(cur)
    return result


def average(points):
    aver = [0,0]

    for point in points:
        aver[0] += point[0]
        aver[1] += point[1]

    return aver[0]/len(points), aver[1]/len(points)


class MainWindow:
    def __init__(self, conf):
        self.config = conf

        self.window_name = self.config['window_name']
        self.window_size = self.config['window_size']

        # Accepted files for the program
        self.filetypes = [("Fichiers JPEG & PNG", ("*.jpg", "*.png"))]

        self.canvas_elements = list

        self.select_start = None
        self.select_end = None

        # Work area size
        self.wa_width, self.wa_height = str.split(self.config['work_area_dimensions'], ",")

        # Menu width
        self.menu_width = self.config['menu_width']

        # Instanciating main window (root)
        self.root = Tk()
        self.root.title(self.window_name)
        self.root.resizable(False, False)
        self.root.geometry(self.window_size)
        self.root.canvas_elements = list()
        # Main window has focus by default
        self.root.focus_set()
        # Binding esc key to a function that halts the program
        self.root.bind("<Escape>", self.close_window)

        # Instantiating widgets
        # TODO: pour l'instant, la fenêtre n'est pas resizable. Si elle le devient, il faudra trouver un moyen de faire marcher tout ça
        self.main_frame = Frame(self.root, width=400, bg="#8a0be5")
        self.menu_frame = Frame(self.root, bg="#48f442")
        self.cv = Canvas(self.main_frame, bg="#4286f4", height=self.wa_height, width=str(int(self.wa_width) - int(self.menu_width)))

        # Selection box
        self.rect = RectTracker(self.cv, self.root)

        # Creating menu buttons
        self.open_button = Button(self.menu_frame, text="Ouvrir...", command=self.open_select_dialog, width=22)
        self.save_button = Button(self.menu_frame, text="Enregistrer sous...", command=self.open_save_dialog, width=22)
        self.recognize_button = Button(self.menu_frame, text="Reconnaître la sélection", command=self.open_select_dialog, width=22)
        self.new_collage_button = Button(self.menu_frame, text="Nouveau Collage", command=self.open_select_dialog, width=22)

        # Placing widgets on the window
        self.main_frame.grid(column=0, row=0)
        self.menu_frame.grid(column=1, row=0, columnspan=2, ipadx=20, ipady=20, sticky=N)
        self.cv.grid(column=0, row=0)

        self.open_button.grid(column=0, row=0, pady=5, rowspan=2, sticky=W)
        self.save_button.grid(column=0, row=2, pady=5, rowspan=2, sticky=E)
        self.recognize_button.grid(column=0, row=4, pady=5, rowspan=2, sticky=E)
        self.new_collage_button.grid(column=0, row=6, pady=5, rowspan=2)

        # End of code by ©Sunjay Varma

        self.root.mainloop()

    def open_select_dialog(self):
        print("button clicked")
        self.load_image(filedialog.askopenfilename(filetypes=self.filetypes))

    def open_save_dialog(self):
        print("button clicked")
        self.save_image(filedialog.asksaveasfilename(confirmoverwrite=True, filetypes=[("Fichier JPEG", "*.jpg")]))

    def load_image(self, path, multiple=False):
        if path is not "":
            if multiple is True:
                # TODO: implémenter le chargement d'images multiples pour le collage
                self.canvas_elements.append(Image.open(path, "r"))
                self.root.canvas_elements.append(ImageTk.PhotoImage(self.canvas_elements[0]))
            else:
                self.canvas_elements = []
                self.root.canvas_elements = []
                self.canvas_elements.append(Image.open(path, "r"))
                self.root.canvas_elements.append(ImageTk.PhotoImage(self.canvas_elements[0]))
        for pic in self.root.canvas_elements:
            self.cv.create_image(50, 50, image=pic, anchor='nw')



        self.root.update_idletasks()
        self.root.update()

    def save_image(self, path):
        if path is not "":
            self.pic.save(path)

    @staticmethod
    def close_window(event):
        print("event registered")

        if event.keysym == "Escape":
            print("escape recognized")
            exit()


class RectTracker:
    ''' Created by ©Sunjay Varma on Mon, 27 Sep 2010 (MIT)
        Heavily modified by Jeremy Comelli on 18.05.2018
        Pasted from http://code.activestate.com/recipes/577409-python-tkinter-canvas-rectangle-selection-box/'''

    def __init__(self, canvas, root):
        self.root = root

        # TODO: s
        self.select_topleft = [100, 100]
        self.height, self.width = 200, 100
        self.lastx, self.lasty = None, None
        self.active_side = None
        self.canvas = canvas
        self.item = None
        self.item = self.draw()
        self.set_even_handler()

    def draw(self, delta=0):
        """Draws the rectangle"""
        self.move_side(delta)
        return self.canvas.create_rectangle(self.select_topleft[0], self.select_topleft[1], self.select_topleft[0] + self.width, self.select_topleft[1] + self.height, width=2)

    def move_side(self, delta):
        if self.active_side is 0:
            self.select_topleft[1] += delta
            self.height -= delta
        elif self.active_side is 1:
            self.width += delta
        elif self.active_side is 2:
            self.height += delta
        elif self.active_side is 3:
            self.select_topleft[0] += delta
            self.width -= delta
        else:
            print("Error, no active side")

    def set_even_handler(self):
        """Setup automatic drawing"""
        self.canvas.bind("<Button-1>", self.__get_mouse_focus, '+')
        self.canvas.bind("<B1-Motion>", self.__update, '+')
        self.canvas.bind("<ButtonRelease-1>", self.__stop, '+')
        self.canvas.bind('<Motion>', self.cool_design, '+')

    # This function is used to determine which side of the selection box is clicked on, by comparing mouse's XY to each side's XY
    def __get_mouse_focus(self, event):
        if self.select_topleft[1] - 3 < event.y < self.select_topleft[1] + 4 and self.select_topleft[0] < event.x < self.select_topleft[0] + self.width:
            self.active_side = 0
            print("Top Side")
        elif self.select_topleft[0] + self.width - 3 < event.x < self.select_topleft[0] + self.width + 4 and self.select_topleft[1] < event.y < self.select_topleft[1] + self.height:
            self.active_side = 1
            print("Right Side")
        elif self.select_topleft[1] + self.height - 3 < event.y < self.select_topleft[1] + self.height + 4 and self.select_topleft[0] < event.x < self.select_topleft[0] + self.width:
            self.active_side = 2
            print("Bottom Side")
        elif self.select_topleft[0] - 3 < event.x < self.select_topleft[0] + 4 and self.select_topleft[1] < event.y < self.select_topleft[1] + self.height:
            self.active_side = 3
            print("Left Side")
        else:
            self.active_side = None
            print("No Active side")

        self.start_x = event.x
        self.start_y = event.y

    def __update(self, event):
        delta_x = event.x - self.start_x
        delta_y = event.y - self.start_y
        change = 0
        if self.active_side is 0 or self.active_side is 2:
            change = delta_y
        elif self.active_side is 1 or self.active_side is 3:
            change = delta_x

        self.canvas.delete(self.item)

        self.item = self.draw(change)
        self.start_x, self.start_y = event.x, event.y
        # self._command(self.start, (event.x, event.y))
        self.select_end = (event.x, event.y)

    def __stop(self, event):
        # Makes the rectangle disappear once mouse1 is released
        self.start_x, self.start_y = None, None

        # TODO: bouger ça dans une méthode dédiée
        # To save the image, we use PIL to get a screenshot of the specified coordinates
        # We also have to add the window position, and the number of pixels on the side of the window
        # This is kind of a workaround, and it won't work if the window border size changes, like on W10 or any other os really
        # ImageGrab.grab().crop((self.root.winfo_x() + self.select_start[0] + 9, self.root.winfo_y() + self.select_start[1] + 31, self.root.winfo_x() + self.select_end[0] + 7, self.root.winfo_y() + self.select_end[1] + 29)).save("C:\\Users\\Jeremy.COMELLI\\Desktop\\test.png")

        # Code by ©Sunjay Varma
        x, y = None, None

    def cool_design(self, event):
        global x, y
        self.kill_xy()

        dashes = [3, 2]
        x = self.canvas.create_line(event.x, 0, event.x, 1000, dash=dashes, tags='no')
        y = self.canvas.create_line(0, event.y, 1000, event.y, dash=dashes, tags='no')

        # Here we change the cursor, according to it's position
        if self.select_topleft[1] - 3 < event.y < self.select_topleft[1] + 4 and self.select_topleft[0] < event.x < self.select_topleft[0] + self.width or self.select_topleft[1] + self.height - 3 < event.y < self.select_topleft[1] + self.height + 4 and self.select_topleft[0] < event.x < self.select_topleft[0] + self.width:
            self.canvas.configure(cursor="sb_v_double_arrow")
        elif self.select_topleft[0] - 3 < event.x < self.select_topleft[0] + 4 and self.select_topleft[1] < event.y < self.select_topleft[1] + self.height or self.select_topleft[0] + self.width - 3 < event.x < self.select_topleft[0] + self.width + 4 and self.select_topleft[1] < event.y < self.select_topleft[1] + self.height:
            self.canvas.configure(cursor="sb_h_double_arrow")
        else:
            self.canvas.configure(cursor="arrow")

    def kill_xy(self, event=None):
        self.canvas.delete('no')
