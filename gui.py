
import tkinter as tk
import threading

from cluster import Cluster, cluster
from stargen import Star, generate_stars

from math import floor
from random import random
from time import sleep

class Application(tk.Frame):

    def __init__(self, 
    master: tk.Frame = None, 
    width: int = None, 
    height: int = None):
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height
        self.star_list = None
        self.cluster_list = None
        self.clusters = None
        self.diameter_range = (4, 6)
        self.pack()
        self.set_up()

        self.move_after_id = None
        
    def set_up(self):
        self.create_canvas()
        self.create_menu()
        self.create_draw_button()
        self.create_quit_button()

        self.create_n_textbox()
        self.create_constellation_textbox()
        self.create_probability_textbox()
        self.create_velocity_textbox()

        self.create_error_label()

    def create_canvas(self):
        if self.width is None:
            self.width = 1500
        if self.height is None:
            self.height = 800
        
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

    def create_constellation_textbox(self):
        self.const_textvar = tk.StringVar()
        self.const_label = tk.Label(
            self.menu,
            text = 'Number of Constellations:'
        )
        self.const_textbox = tk.Entry(
            self.menu,
            width = '4',
            textvariable = self.const_textvar
        )
        self.const_textvar.set(20)
        self.const_label.pack(side = 'left', fill = 'y')
        self.const_textbox.pack(side = 'left', fill = 'y')

    def create_probability_textbox(self):
        self.prob_textvar = tk.StringVar()
        self.prob_label = tk.Label(
            self.menu,
            text = 'Inclusion Probability:'
        )
        self.prob_textbox = tk.Entry(
            self.menu,
            width = '4',
            textvariable = self.prob_textvar
        )
        self.prob_textvar.set(0.9)
        self.prob_label.pack(side = 'left', fill = 'y')
        self.prob_textbox.pack(side = 'left', fill = 'y')

    def create_velocity_textbox(self):
        self.velocity_textvar = tk.StringVar()
        self.velocity_label = tk.Label(
            self.menu,
            text = 'Velocity (x,y)'
        )
        self.velocity_textbox = tk.Entry(
            self.menu,
            width = 6,
            textvariable = self.velocity_textvar
        )
        self.velocity_textvar.set('1,1')
        self.velocity_label.pack(side = 'left', fill = 'y')
        self.velocity_textbox.pack(side = 'left', fill = 'y')

    def create_error_label(self):
        self.error_textvar = tk.StringVar()
        self.error_label = tk.Label(
            self.menu,
            textvariable = self.error_textvar,
            fg = 'red'
        )
        self.error_textvar.set('')
        self.error_label.pack(side = 'right', fill = 'y', padx = '10')

    def move_stars(self):
        for star in self.star_list:
            star.move()
        
        self.canvas.delete('all')
        for star in self.star_list:
            self._draw_star(star, 'white')
        
        for constellation in self.clusters:
            self._draw_constellation(constellation, 'white')
        
        self.move_after_id = self.master.after(10, self.move_stars)
    
    def draw(self):
        # Stop the animation
        if not self.move_after_id is None:
            self.master.after_cancel(self.move_after_id)
            
        # Begin error checking section
        try: 
            n = int(self.n_textvar.get())
        except:
            self.error_textvar.set('Number of stars not an integer')
            return

        try: 
            constellations = int(self.const_textvar.get())
        except:
            self.error_textvar.set('Number of constellations not an integer')
            return

        if constellations > n:
            self.error_textvar.set('Stars must be greater than constellations')
            return

        try:
            probability = float(self.prob_textvar.get())
            if probability > 1.0 or probability < 0.0:
                self.error_textvar.set('Probability must be between 0 and 1')
                return
        except:
            self.error_textvar.set('Inclusion probability is not a float')
            return

        try:
            values = self.velocity_textvar.get().split(',')
            if len(values) < 2:
                self.error_textvar.set('Ensure there are two values for velocity, separated by ","')
                return
            velocity = (float(values[0]), float(values[1]))
        except:
            self.error_textvar.set('Could not set velocity. Ensure both values are floats')
            return

        # End error checking section
        self.error_textvar.set('')
        self.canvas.delete('all')

        # We only want rounded numbers in the list of stars
        self.star_list = generate_stars(n, (self.width, self.height), velocity, should_floor=True)
        for star in self.star_list:
            self._draw_star(star, 'white')

        # Generate the lists to be clustered
        self.cluster_list = [star for star in self.star_list if random() < probability]

        # Cluster all of the stars together using agglomerative clustering
        self.clusters = cluster(self.cluster_list, constellations, probability)

        for clust in self.clusters:
            clust.generate_map()

        # Start the movement thread
        self.move_stars()

    def _draw_star(self, star: Star, color: str):
        x = star.get_x()
        y = star.get_y()

        diameter_diff = self.diameter_range[1] - self.diameter_range[0]
        diameter = self.diameter_range[0] + int(round(diameter_diff * star.get_z()))

        start_x = floor(x - (diameter / 2))
        start_y = floor(y - (diameter / 2))

        self.canvas.create_oval(
            start_x,
            start_y,
            start_x + diameter,
            start_y + diameter,
            fill = color
        )

    def _draw_constellation(self, const: Cluster, color: str):
        for star, other in const.mapping:
            self.canvas.create_line(
                star.get_x(), star.get_y(),
                other.get_x(), other.get_y(),
                fill = color
            )