
import tkinter as tk

from cluster import Cluster, cluster
from stargen import Star, generate_stars

from math import floor

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
        self.pack()
        self.set_up()
        
    def set_up(self):
        self.create_canvas()
        self.create_menu()
        self.create_draw_button()
        self.create_quit_button()

        self.create_n_textbox()
        self.create_constellation_textbox()
        self.create_probability_textbox()

        self.create_error_label()

    def create_canvas(self):
        if self.width is None:
            self.width = 1200
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

    def create_error_label(self):
        self.error_textvar = tk.StringVar()
        self.error_label = tk.Label(
            self.menu,
            textvariable = self.error_textvar,
            fg = 'red'
        )
        self.error_textvar.set('')
        self.error_label.pack(side = 'right', fill = 'y', padx = '10')
    
    def draw(self):
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

        # End error checking section
        self.error_textvar.set('')
        self.canvas.delete('all')

        # We only want rounded numbers in the list of stars
        self.star_list = generate_stars(n, (self.width, self.height), should_floor=True)
        for star in self.star_list:
            self._draw_star(star, 'white')

        # Cluster all of the stars together using agglomerative clustering
        clusters = cluster(self.star_list, constellations, probability)

        for clust in clusters:
            self._draw_constellation(clust, 'white')

    def _draw_star(self, star: Star, color: str):
        x = star.get_x()
        y = star.get_y()

        # Define some arbitrary radius
        diameter = 5

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
        connected = [[star, False] for star in const.stars]

        dist = lambda s1, s2: abs(s1.get_x() - s2.get_x()) + abs(s1.get_y() - s2.get_y())

        for tup in connected:
            distances = [(dist(tup[0], item[0]), item) for item in connected if item != tup]

            min_dist = min(distances, key=lambda item: item[0])

            if min_dist[1][1]:
                distances.remove(min_dist)
                min_dist = min(distances, key=lambda item: item[0])

            star = tup[0]
            other = min_dist[1][0]

            self.canvas.create_line(
                star.get_x(), star.get_y(),
                other.get_x(), other.get_y(),
                fill = color
            )

            tup[1] = True
            min_dist[1][1] = True