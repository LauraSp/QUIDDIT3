"""My Version of using Tkinter
"""
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from QAllExceptions import *
from QTclWindowBasics import *


class QTclBaseWindow(QTclWindowBasics, tk.Frame):
    """base class for tcl driven windows
    inherit this for your own windows
    """

    def mainloop(self):
        """ Enter the main loop"""
        self.root.mainloop()

    def __init__(self, title):
        #NoDefaultRoot()
        self.root = tk.Tk() 
        super().__init__(self.root, padx=5, pady=5)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.resizable(True, True)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.make_gui(title)
        self.loaded()

    def setwintitle(self, title):
        """Sets the title of your main window
        """
        self.root.title(title)

    def loaded(self):
        raise TclWinBaseUsageException("Override me! Always override loaded method")

    def make_gui(self, title):
        raise TclWinBaseUsageException("Override me! Always override make_gui method")
        
    def make_menu(self, menubar, title, itemlib):     
        submenu = tk.Menu(menubar, tearoff=0)
        for item in itemlib:
            submenu.add_command(label=item, command=itemlib[item])
            
        menubar.add_cascade(label=title, menu=submenu)
        
        return submenu
       

    
