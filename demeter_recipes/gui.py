# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 22:07:45 2024

@author: AldenYellowhorse
"""

import tkinter as tk
from tkinter import Canvas, Tk
from datetime import date, timedelta


class GUI:
    """Initialize the window in this class and run the core application."""

    def __init__(self):
        """Initialize the gui object and start the UI."""
        self.root = Tk()
        self.root.state('zoomed')
        self.root.title('Demeter Recipes')

        # This dictionary contains several different options for configuring
        # the GUI.
        options = {'dark': '#241023',
                   'med': '#6B0504',
                   'light': '#A3320B',
                   'grey': '#D4D4D4',
                   'left bar width': 300,
                   'top bar height': 200,
                   'text offset': (100, 100),
                   'y spacing': 150,             # vertical spacing in calendar
                   'x spacing': 200,             # horizontal spacing calendar
                   'num weeks': 6,               # weeks to display
                   'days in week': 7,
                   'monday starts week': False,  # is monday the first day
                   }

        self.left_bar(self.root, options)
        self.top_bar(self.root, options)
        self.calendar(self.root, options)
        self.get_dates(options)
        self.root.mainloop()

    def left_bar(self, root, options):
        """Given the root tkinter object, paint the left section containing the
        logo, the search bar, meal widgets and labels."""
        canvas = Canvas(root, width=options['left bar width'],
                        bg=options['dark'])
        canvas.pack(anchor=tk.NW, fill=tk.Y, expand=False, side=tk.LEFT)

    def top_bar(self, root, options):
        """Given the root tkinter object, paint the top bar and text name for
        the calendar."""
        canvas = Canvas(root, height=options['top bar height'],
                        bg=options['light'])
        canvas.pack(anchor=tk.NW, fill=tk.X, expand=False, side=tk.TOP)
        canvas.create_text(options['text offset'],
                           text="Calendar",
                           fill="white",
                           font='satoshi 24')

    def get_dates(self, options):
        """Get the list of calendar dates to print to the screen based on
        today's date."""
        today = date.today()
        day = timedelta(days=1)
        if options['monday starts week']:
            to_sunday = timedelta(days=today.weekday())
        else:
            to_sunday = timedelta(days=today.weekday() + 1)
        first_sunday = today - to_sunday - 7*day
        num_days = options['num weeks'] * 7
        days = [first_sunday + i*day for i in range(num_days)]
        return days

    def calendar(self, root, options):
        """Create the calendar."""
        canvas = Canvas(root, bg=options['grey'])
        canvas.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
        days = self.get_dates(options)

        for i in range(options['num weeks']):
            height = i * options['y spacing']
            if i > 0:
                canvas.create_line((0, height), (2000, height), width=2,
                                   fill=options['dark'])
            for j in range(options['days in week']):
                position = ((j + 1)*options['x spacing'], height + 20)
                date_num = str(days[7*i + j].day)
                if date_num == '1':
                    date_num += ' ' + days[7*i + j].strftime('%B')
                canvas.create_text(position, text=str(date_num),
                                   fill=options['dark'],
                                   font='satoshi')


g = GUI()
