from tkinter import *
from tkinter import messagebox
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
from sources import NeuralNet
from random import shuffle
from PIL import ImageGrab
from scipy import misc
import numpy

class MainWindow:
    def __init__(self, conf):
        self.config = conf

        self.window_name = self.config['window_name']
        self.window_size = self.config['window_size']

        # Accepted files for the program
        self.filetypes = [("Fichiers JPEG & PNG", ("*.jpg", "*.png"))]

        Neural_interface = NeuralNet.NeuralNetwork()

        # Images which are displayed on the canvas are also saved as a numpy array, so we can manipulate them and use the array for NN processing
        self.image = None


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

        # Binding esc key to a function that halts the program, disabled for release
        if bool(self.config['devmode']):
            self.root.bind("<Escape>", self.close_window)

        # Instantiating widgets
        # TODO: pour l'instant, la fenêtre n'est pas resizable. Si elle le devient, il faudra trouver un moyen de faire marcher tout ça
        self.main_frame = Frame(self.root, width=400, bg="#8a0be5")
        self.menu_frame = Frame(self.root, bg="#48f442")
        self.cv = Canvas(self.main_frame, bg="#4286f4", height=self.wa_height, width=str(int(self.wa_width) - int(self.menu_width)))

        # Selection box
        self.rect = RectTracker(self.cv, self.root, self.config)
        self.select_start = None

        # Creating menu buttons
        self.open_button = Button(self.menu_frame, text="Ouvrir...", command=self.open_select_dialog, width=22)
        self.save_button = Button(self.menu_frame, text="Enregistrer sous...", command=self.save_image, width=22)
        self.recognize_button = Button(self.menu_frame, text="Reconnaître la sélection", command=self.recognize_selection, width=22)
        self.crop_button = Button(self.menu_frame, text="Recadrer", command=self.crop_selection, width=22)

        # Placing widgets on the window
        self.main_frame.grid(column=0, row=0)
        self.menu_frame.grid(column=1, row=0, columnspan=2, ipadx=20, ipady=20, sticky=N)
        self.cv.grid(column=0, row=0)

        self.open_button.grid(column=0, row=0, pady=5, rowspan=2, sticky=W)
        self.save_button.grid(column=0, row=2, pady=5, rowspan=2, sticky=E)
        self.recognize_button.grid(column=0, row=4, pady=5, rowspan=2, sticky=E)
        self.crop_button.grid(column=0, row=6, pady=5, rowspan=2)

        ## TODO: REMOVE ##
        self.load_image("bleh")
        ## ##

        self.root.mainloop()

    def recognize_selection(self):
        messagebox.showinfo("Réseau Neuronal non disponible")

    def crop_selection(self):
        if self.rect.width is not 0 and self.rect.height is not 0:
            self.image.crop(self.image.save_np_as_image(self.rect.get_select_origin((self.image.origin_x, self.image.origin_y)), (self.rect.width, self.rect.height)))
            self.cv.delete(self.image)
            self.image.add_to_canvas()
            self.rect.delete()
        else:
            messagebox.showinfo("Impossible de recadrer", "Veuillez sélectionner une zone à recadrer")

    def open_select_dialog(self):
        self.load_image(filedialog.askopenfilename(filetypes=self.filetypes))

    def save_image(self):
        path = filedialog.asksaveasfilename(confirmoverwrite=True, filetypes=self.filetypes)
        if path is not "":
            if self.rect.width is not 0 and self.rect.height is not 0:
                self.image.save_np_as_image(self.rect.get_select_origin((self.image.origin_x, self.image.origin_y)), (self.rect.width, self.rect.height), path)
            else:
                self.image.save_np_as_image([self.image.origin_x, self.image.origin_y], path)

    def load_image(self, path, multiple=False):
        if path is not "":
            if multiple is True:
                # TODO: implémenter le chargement d'images multiples pour le collage
                print("Error, multiple image selection is not yet implemented")
            else:

                ## TODO: REMOVE ##
                path = "C:\\Users\\Jeremy.COMELLI\\Desktop\\Pingu.jpg"
                ##

                # Creating an image object
                np_image = NumpyImage(path, self.root, self.cv)

                # Image object is added to our list
                self.image = np_image

            # Finally, every image is added onto the canvas
            self.image.add_to_canvas()

        self.root.update_idletasks()
        self.root.update()

    @staticmethod
    def close_window(event):
        print("event registered")

        if event.keysym == "Escape":
            print("escape recognized")
            exit()


class NumpyImage:
    def __init__(self, path, root, canvas, origin=[0, 0]):
        self.root = root
        self.cv = canvas

        # Here we add a small offset, because for some reason the canvas starts outside of the frame
        self.origin_x = origin[0] + 2
        self.origin_y = origin[1] + 2
        self.width, self.height = 0, 0

        self.path = path
        self.image_np = None
        self.image_tk = None

        self.load()

    def crop(self, new_np):
        print("Cropping stuff")
        self.image_tk = ImageTk.PhotoImage(Image.fromarray(new_np))
        self.image_np = new_np
        self.add_to_canvas()

    def load(self):
        self.image_np = misc.imread(self.path)
        self.image_tk = ImageTk.PhotoImage(Image.fromarray(self.image_np))
        self.width, self.height = self.image_tk.width(), self.image_tk.height()
        print("PhotoImage: " + str(self.image_tk.width()) + ", " + str(self.image_tk.height()))
        print("width, height: " + str(self.width) + ", " + str(self.height))


    def add_to_canvas(self):
        self.cv.delete(self.image_tk)
        self.cv.create_image(self.origin_x, self.origin_y, image=self.image_tk, anchor='nw')

    def save_np_as_image(self, topleft, size, save_path=-1):
        if size is None:
            print("size is self")
            size = self.width, self.height
        save_width, save_height = size
        print(str(save_width) + ", " + str(save_height))
        save_origin_x, save_origin_y = topleft

        if save_width < 0:
            save_origin_x += save_width
            save_width = abs(save_width) + save_origin_x
        else:
            save_width += save_origin_x

        if save_height < 0:
            save_origin_y += save_height
            save_height = abs(save_height) + save_origin_y
        else:
            save_height += save_origin_y

        if save_path is not -1:
            Image.fromarray(self.image_np[save_origin_y:save_height:1, save_origin_x:save_width:1]).save(save_path)
        else:
            return self.image_np[save_origin_y:save_height:1, save_origin_x:save_width:1]


class RectTracker:
    ''' Created by ©Sunjay Varma on Mon, 27 Sep 2010 (MIT)
        Heavily modified by Jeremy Comelli
        Pasted from http://code.activestate.com/recipes/577409-python-tkinter-canvas-rectangle-selection-box/'''

    def __init__(self, canvas, root, conf):
        self.root = root
        self.config = conf
        self.select_hitbox = int(self.config['select_hitbox'])

        self.select_topleft = [-1, -1]
        self.start = self.select_topleft
        self.height, self.width = 0, 0
        self.wa_width, self.wa_height = str.split(self.config['work_area_dimensions'], ",")
        self.wa_height, self.wa_width = int(self.wa_height), int(self.wa_width)
        self.lastx, self.lasty = None, None
        self.active_side = None
        self.canvas = canvas
        self.item = None
        self.set_even_handler()

    def draw(self, event, delta):
        """Draws the rectangle"""
        if delta is not 0:
            self.move_side(event, delta)
        return self.canvas.create_rectangle(self.select_topleft[0], self.select_topleft[1], self.select_topleft[0] + self.width, self.select_topleft[1] + self.height, width=2)

    def move_side(self, event, delta):
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
        # If no active side is selected, creating a new rectangle from scratch
        else:
            self.width += delta[0]
            self.height += delta[1]

    def set_even_handler(self):
        """Setup automatic drawing"""
        self.canvas.bind("<Button-1>", self.__get_mouse_focus, '+')
        self.canvas.bind("<B1-Motion>", self.__update, '+')
        self.canvas.bind("<ButtonRelease-1>", self.__stop, '+')
        self.canvas.bind('<Motion>', self.cool_design, '+')

    # This function is used to determine which side of the selection box is clicked on, by comparing mouse's XY to each side's XY
    def __get_mouse_focus(self, event):
        if self.select_topleft[1] - self.select_hitbox < event.y < self.select_topleft[1] + self.select_hitbox and self.select_topleft[0] < event.x < self.select_topleft[0] + self.width:
            self.active_side = 0
            print("Top Side")
        elif self.select_topleft[0] + self.width - self.select_hitbox < event.x < self.select_topleft[0] + self.width + self.select_hitbox and self.select_topleft[1] < event.y < self.select_topleft[1] + self.height:
            self.active_side = 1
            print("Right Side")
        elif self.select_topleft[1] + self.height - self.select_hitbox < event.y < self.select_topleft[1] + self.height + self.select_hitbox and self.select_topleft[0] < event.x < self.select_topleft[0] + self.width:
            self.active_side = 2
            print("Bottom Side")
        elif self.select_topleft[0] - self.select_hitbox < event.x < self.select_topleft[0] + self.select_hitbox and self.select_topleft[1] < event.y < self.select_topleft[1] + self.height:
            self.active_side = 3
            print("Left Side")
        elif self.width < 1 and self.select_topleft[1] - self.select_hitbox < event.y < self.select_topleft[1] + self.select_hitbox and self.select_topleft[0] + self.width < event.x < self.select_topleft[0]:
            self.active_side = 0
            print("Top Side")
        elif self.height < 1 and self.select_topleft[0] + self.width - self.select_hitbox < event.x < self.select_topleft[0] + self.width + self.select_hitbox and self.select_topleft[1] + self.height < event.y < self.select_topleft[1]:
            self.active_side = 1
            print("Right Side")

        elif self.width < 1 and self.select_topleft[1] + self.height - self.select_hitbox < event.y < self.select_topleft[1] + self.height + self.select_hitbox and self.select_topleft[0] + self.width < event.x < self.select_topleft[0]:
            self.active_side = 2
            print("Bottom Side")
        elif self.height < 1 and self.select_topleft[0] - self.select_hitbox < event.x < self.select_topleft[0] + self.select_hitbox and self.select_topleft[1] + self.height < event.y < self.select_topleft[1]:
            self.active_side = 3
            print("Left Side")
        elif event.x > 0 and event.y > 0:
            self.active_side = None
            print("No Active side, creating new Rectangle")
            self.canvas.delete(self.item)
            self.width = 0
            self.height = 0
            self.select_topleft[0] = event.x
            self.select_topleft[1] = event.y

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

        if event.x > self.wa_width or event.y > self.wa_width:
            change = 0
        if event.x > self.wa_width:
            delta_x = 0
        if event.y > self.wa_height:
            delta_y = 0

        self.canvas.delete(self.item)
        if self.active_side is not None:
            self.item = self.draw(event, change)
        else:
            self.item = self.draw(event, [delta_x, delta_y])
        self.canvas.update_idletasks()

        self.start_x, self.start_y = event.x, event.y
        # self._command(self.start, (event.x, event.y))
        self.select_end = (event.x, event.y)

    def __stop(self, event):
        # Makes the rectangle disappear once mouse1 is released
        self.start_x, self.start_y = None, None

        # TODO: bouger ça dans une méthode dédiée a bouger dans une méthode dédiée
        # To save the image, we use PIL to get a screenshot of the specified coordinates
        # We also have to add the window position, and the number of pixels on the side of the window
        # This is kind of a workaround, and it won't work if the window border size changes, like on W10 or any other os really
        # ImageGrab.grab().crop((self.root.winfo_x() + self.select_start[0] + 9, self.root.winfo_y() + self.select_start[1] + 31, self.root.winfo_x() + self.select_end[0] + 7, self.root.winfo_y() + self.select_end[1] + 29)).save("C:\\Users\\Jeremy.COMELLI\\Desktop\\test.png")

        # Code by ©Sunjay Varma
        x, y = None, None

    def get_select_origin(self, image_origin):
        image_x = self.select_topleft[0] - image_origin[0]
        image_y = self.select_topleft[1] - image_origin[1]

        return image_x, image_y

    def delete(self):
        self.canvas.delete(self.item)
        self.width, self.height, self.select_topleft = 0, 0, [0, 0]

    def cool_design(self, event):
        global x, y
        self.kill_xy()

        dashes = [3, 2]
        x = self.canvas.create_line(event.x, 0, event.x, 1000, dash=dashes, tags='no')
        y = self.canvas.create_line(0, event.y, 1000, event.y, dash=dashes, tags='no')

        # Here we change the cursor according to which select_box's side it is hovering
        if self.select_topleft[1] - self.select_hitbox < event.y < self.select_topleft[1] + self.select_hitbox and self.select_topleft[0] < event.x < self.select_topleft[0] + self.width or self.select_topleft[1] + self.height - self.select_hitbox < event.y < self.select_topleft[1] + self.height + self.select_hitbox and self.select_topleft[0] < event.x < self.select_topleft[0] + self.width:
            self.canvas.configure(cursor="sb_v_double_arrow")
        elif self.select_topleft[0] - self.select_hitbox < event.x < self.select_topleft[0] + self.select_hitbox and self.select_topleft[1] < event.y < self.select_topleft[1] + self.height or self.select_topleft[0] + self.width - self.select_hitbox < event.x < self.select_topleft[0] + self.width + self.select_hitbox and self.select_topleft[1] < event.y < self.select_topleft[1] + self.height:
            self.canvas.configure(cursor="sb_h_double_arrow")
        elif self.height < 1 and self.select_topleft[0] - self.select_hitbox < event.x < self.select_topleft[0] + self.select_hitbox and self.select_topleft[1] + self.height < event.y < self.select_topleft[1] or self.select_topleft[0] + self.width - self.select_hitbox < event.x < self.select_topleft[0] + self.width + self.select_hitbox and self.select_topleft[1] + self.height < event.y < self.select_topleft[1]:
            self.canvas.configure(cursor="sb_h_double_arrow")
        elif self.width < 1 and self.select_topleft[1] - self.select_hitbox < event.y < self.select_topleft[1] + self.select_hitbox and self.select_topleft[0] + self.width < event.x < self.select_topleft[0] or self.select_topleft[1] + self.height - self.select_hitbox < event.y < self.select_topleft[1] + self.height + self.select_hitbox and self.select_topleft[0] + self.width < event.x < self.select_topleft[0]:
            self.canvas.configure(cursor="sb_v_double_arrow")

        else:
            self.canvas.configure(cursor="arrow")

    def kill_xy(self, event=None):
        self.canvas.delete('no')
