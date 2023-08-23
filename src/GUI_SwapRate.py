"""

"""
__author__ = 'Hongpeng Zhang'
__email__ = 'hongpeng.zhang@nmbu.no'

from tkinter import *
from tkinter import ttk
import numpy as np
import numpy_financial as npf
from sympy import *
import SwapRate as SR

class SrWindow():
    def __init__(self):
        self.srwindow = None
        self.createwindow()

    def createwindow(self):
        self.srwindow = Toplevel()  # Create a new toplevel window
        self.srwindow.title("Swap Rate Calculator")
        self.srwindow.geometry('470x150+500+300')
        srframe = ttk.Frame(self.srwindow, padding="3 3 12 12")
        srframe.grid(column=0, row=0)
        self.srwindow.columnconfigure(0, weight=1)
        self.srwindow.rowconfigure(0, weight=1)

        # Define entries for variables
        s1 = StringVar()
        s1_entry = ttk.Entry(srframe, width=7, textvariable=s1)
        s1_entry.grid(column=2, row=1)

        s2 = StringVar()
        s2_entry = ttk.Entry(srframe, width=7, textvariable=s2)
        s2_entry.grid(column=4, row=1)

        s3 = StringVar()
        s3_entry = ttk.Entry(srframe, width=7, textvariable=s3)
        s3_entry.grid(column=2, row=2)

        s4 = StringVar()
        s4_entry = ttk.Entry(srframe, width=7, textvariable=s4)
        s4_entry.grid(column=4, row=2)

        # Define labels for variables
        ttk.Label(srframe, text="spot rate 1 : ", anchor='center').grid(column=1, row=1)
        ttk.Label(srframe, text="spot rate 2 : ", anchor='center').grid(column=3, row=1)
        ttk.Label(srframe, text="spot rate 3 : ", anchor='center').grid(column=1, row=2)
        ttk.Label(srframe, text="spot rate 4 : ", anchor='center').grid(column=3, row=2)

        # Define input info label
        input_info = StringVar()
        ttk.Label(srframe, textvariable=input_info, anchor='center').grid(column=1, row=4, sticky=(W, E), columnspan=4)

        def input_test(entry):
            try:
                value = float(entry.get())
            except ValueError:
                input_info.set('Inputs must be numbers, please input again!')
            return value

        def input_test_int(entry):
            try:
                value = int(entry.get())
            except ValueError:
                input_info.set('Inputs must be numbers, please input again!')
            return value

        def calculate(event):
            s1 = input_test(s1_entry)
            s2 = input_test(s2_entry)
            s3 = input_test(s3_entry)
            s4 = input_test(s4_entry)
            sw1 = Symbol('sw1')
            sw2 = Symbol('sw2')
            sw3 = Symbol('sw3')
            sw4 = Symbol('sw4')
            sw1 / (1 + s1) + 1 / (1 + s1) == 1
            xsw1 = solveset(sw1 / (1 + s1) + 1 / (1 + s1) - 1, sw1)
            xsw2 = solveset(sw2 / (1 + s1) + sw2 / ((1 + s2) ** 2) + 1 / ((1 + s2) ** 2) - 1, sw2)
            xsw3 = solveset(sw3 / (1 + s1) + sw3 / ((1 + s2) ** 2) + sw3 / ((1 + s3) ** 3) + 1 / ((1 + s3) ** 3) - 1,
                            sw3)
            xsw4 = solveset(
                sw4 / (1 + s1) + sw4 / ((1 + s2) ** 2) + sw4 / ((1 + s3) ** 3) + sw4 / ((1 + s4) ** 4) + 1 / (
                            (1 + s4) ** 4) - 1, sw4)

            sw1 = list(ConditionSet(sw1, sw1 > 0, xsw1))[0]
            sw2 = list(ConditionSet(sw2, sw2 > 0, xsw2))[0]
            sw3 = list(ConditionSet(sw3, sw3 > 0, xsw3))[0]
            sw4 = list(ConditionSet(sw4, sw4 > 0, xsw4))[0]

            self.show_result_window(s1=s1, s2=s2, s3=s3, s4=s4, sw1=sw1, sw2=sw2, sw3=sw3, sw4=sw4)

        # Define calculate button
        button_cal = ttk.Button(srframe, text="Calculate Swap Rate")
        button_cal.grid(column=2, row=3, columnspan=2)
        button_cal.bind('<Button-1>', calculate)

        # Define BinomialTree output window

        for child in srframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def show_result_window(self, **kwargs):
        self.resultwindow = Toplevel()  # Create a new result window
        self.resultwindow.title("Swap Rate")
        self.resultwindow.geometry('650x400+550+350')
        self.resultwindow.columnconfigure(0, weight=1)
        self.resultwindow.rowconfigure(0, weight=1)
        text = Text(self.resultwindow, width=650, height=30)
        text.pack()
        stars = '*' * 100
        text.insert(INSERT, f'Set Variables: \n'
                            f'Spot rate 1 = {kwargs["s1"]},    Spot rate 2 = {kwargs["s2"]}\n'
                            f'Spot rate 3 = {kwargs["s3"]},    Spot rate 4= {kwargs["s4"]}\n'
                            f'{stars}\n'
                            f'Swap rate 1 is: {kwargs["sw1"]}\n'
                            f'Swap rate 2 is: {kwargs["sw2"]}\n'
                            f'Swap rate 3 is: {kwargs["sw3"]}\n'
                            f'Swap rate 4 is: {kwargs["sw4"]}\n'
                    )

if __name__ == '__main__':
    swaprate = SrWindow()
    swaprate.srwindow.mainloop()
