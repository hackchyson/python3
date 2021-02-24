#!/usr/bin/env python3
"""
@project: python3
@file: interest
@author: mike
@time: 2021/2/23
 
@function:
"""
import tkinter
import os
import sys


class MainWindow(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Lays out the frame using the grid layout manager
        self.grid(row=0, column=0)

        self.principal = tkinter.DoubleVar()
        self.principal.set(1000.0)
        self.rate = tkinter.DoubleVar()
        self.rate.set(5.0)
        self.years = tkinter.IntVar()
        self.amount = tkinter.StringVar()

        principal_label = tkinter.Label(self, text='Principle $:',
                                        anchor=tkinter.W,
                                        underline=0)
        principal_scale = tkinter.Scale(self, variable=self.principal,
                                        command=self.update_ui,
                                        from_=100,
                                        to=10000000,
                                        resolution=100,
                                        orient=tkinter.HORIZONTAL)
        rate_label = tkinter.Label(self, text='Rate %:',
                                   underline=0,
                                   anchor=tkinter.W)
        rate_scale = tkinter.Scale(self, variable=self.rate,
                                   command=self.update_ui,
                                   from_=1,
                                   to=100,
                                   resolution=0.25,
                                   digits=5,
                                   orient=tkinter.HORIZONTAL)
        year_label = tkinter.Label(self, text='Years:',
                                   underline=0,
                                   anchor=tkinter.W)
        year_scale = tkinter.Scale(self, variable=self.years,
                                   command=self.update_ui,
                                   from_=1,
                                   to=50,
                                   orient=tkinter.HORIZONTAL)
        amount_label = tkinter.Label(self, text='Amount $', anchor=tkinter.W)
        actual_amount_label = tkinter.Label(self, textvariable=self.amount,
                                            relief=tkinter.SUNKEN,
                                            anchor=tkinter.E)

        principal_label.grid(row=0, column=0, padx=2, pady=2, sticky=tkinter.W)
        principal_scale.grid(row=0, column=1, padx=2, pady=2, sticky=tkinter.EW)
        rate_label.grid(row=1, column=0, padx=2, pady=2, sticky=tkinter.W)
        rate_scale.grid(row=1, column=1, padx=2, pady=2, sticky=tkinter.EW)
        year_label.grid(row=2, column=0, padx=2, pady=2, sticky=tkinter.W)
        year_scale.grid(row=2, column=1, padx=2, pady=2, sticky=tkinter.EW)
        amount_label.grid(row=3, column=0, padx=2, pady=2, sticky=tkinter.W)
        actual_amount_label.grid(row=3, column=1, padx=2, pady=2, sticky=tkinter.EW)

        principal_scale.focus_set()
        self.update_ui()
        parent.bind('<Alt-p>', lambda *ignore: principal_scale.focus_set())
        parent.bind('<Alt-r>', lambda *ignore: rate_scale.focus_set())
        parent.bind('<Alt-y>', lambda *ignore: year_scale.focus_set())
        parent.bind('<Control-q>', self.quit)
        parent.bind('<Escape>', self.quit)

    def update_ui(self, *ignore):
        amount = self.principal.get() * (
                (1 + (self.rate.get() / 100.0)) ** self.years.get()
        )
        self.amount.set(f'{amount:.2f}')

    def quit(self, event=None):
        self.parent.destroy()


application = tkinter.Tk()
path = os.path.join(os.path.dirname(__file__), 'images/')
if sys.platform.startswith('win'):
    icon = path + 'interest.ico'
else:
    icon = '@' + path + 'interest.xbm'
application.iconbitmap(icon)
application.title('Interest')
window = MainWindow(application)
application.protocol('WM_DELETE_WINDOW', window.quit)
application.mainloop()
