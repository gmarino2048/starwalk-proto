
import tkinter as tk
from gui import Application

def starwalk():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    print("Starwalk Complete")
    pass

if __name__ == '__main__':
    starwalk()