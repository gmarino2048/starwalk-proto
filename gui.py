
import tkinter as tk

class Application(tk.Frame):

    def __init__(self, 
    master: tk.Frame = None, 
    width: int = None, 
    height: int = None):
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height
        self.pack()
        self.set_up()
        
    def set_up(self):
        self.create_canvas()
        self.create_menu()
        self.create_draw_button()
        self.create_quit_button()

        self.create_n_textbox()

    def create_canvas(self):
        if self.width is None:
            self.width = 600
        if self.height is None:
            self.height = 400
        
        self.canvas = tk.Canvas(
            self,
            bg = 'black',
            width = self.width,
            height = self.height
        )

        self.canvas.pack(side = 'top')

    def create_menu(self):
        self.menu = tk.LabelFrame(
            self,
            bg = 'gray'
        )

        self.menu.pack(
            fill = 'both',
            side = 'bottom'
        )

    def create_draw_button(self):
        self.draw_button = tk.Button(
            self.menu,
            text = "Draw",
            command = self.draw
        )
        self.draw_button.pack(side='left', fill='y', padx='10')

    def create_quit_button(self):
        self.quit_button = tk.Button(
            self.menu,
            text = "Quit",
            command = self.quit
        )
        self.quit_button.pack(side='right', fill='y')

    def create_n_textbox(self):
        self.n_textvar = tk.StringVar()
        self.n_label = tk.Label(
            self.menu,
            text = 'Number of stars:'
        )
        self.n_textbox = tk.Entry(
            self.menu,
            width = '4',
            textvariable = self.n_textvar
        )
        self.n_textvar.set('200')
        self.n_label.pack(side = 'left', fill='y')
        self.n_textbox.pack(side = 'left', fill='y')
    
    def draw(self):
        print("Not yet implemented")