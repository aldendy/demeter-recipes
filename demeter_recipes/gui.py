# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 22:07:45 2024

@author: AldenYellowhorse
"""

from tkinter import Tk, ttk


class GUI:
    """Initialize the window in this class and run the core application."""

    def __init__(self):
        """Initialize the gui object and start the UI."""
        self.root = Tk()
        frm = ttk.Frame(self.root, padding=10)
        frm.grid()
        ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
        ttk.Button(frm, text="Quit", command=self.root.destroy).grid(column=1,
                                                                     row=0)
        self.root.mainloop()
