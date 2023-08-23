"""

"""
__author__ = 'Hongpeng Zhang'
__email__ = 'hongpeng.zhang@nmbu.no'

from tkinter import *
from tkinter import ttk
import HorizonYield as HY
import numpy_financial as npf

class HyWindow():
    def __init__(self):
        # self.root = root
        self.hywindow = None
        self.createwindow()

    def createwindow(self):
        self.hywindow = Toplevel()  # Create a new toplevel window
        self.hywindow.title("Horizon Yeild Calculator")
        self.hywindow.geometry('470x150+500+300')
        hyframe = ttk.Frame(self.hywindow, padding="3 3 12 12")
        hyframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.hywindow.columnconfigure(0, weight=1)
        self.hywindow.rowconfigure(0, weight=1)

        # Define entries for variables
        ParValue = StringVar()
        ParValue_entry = ttk.Entry(hyframe, width=7, textvariable=ParValue)
        ParValue_entry.grid(column=2, row=1, sticky=(W, E))

        couponrate = StringVar()
        couponrate_entry = ttk.Entry(hyframe, width=7, textvariable=couponrate)
        couponrate_entry.grid(column=4, row=1, sticky=(W, E))

        maturity = StringVar()
        maturity_entry = ttk.Entry(hyframe, width=7, textvariable=maturity)
        maturity_entry.grid(column=6, row=1, sticky=(W, E))

        n = StringVar()
        n_entry = ttk.Entry(hyframe, width=7, textvariable=n)
        n_entry.grid(column=2, row=2, sticky=(W, E))

        YTMnew = StringVar()
        YTMnew_entry = ttk.Entry(hyframe, width=7, textvariable=YTMnew)
        YTMnew_entry.grid(column=4, row=2, sticky=(W, E))

        YTMold = StringVar()
        YTMold_entry = ttk.Entry(hyframe, width=7, textvariable=YTMold)
        YTMold_entry.grid(column=6, row=2, sticky=(W, E))

        # Define labels for variables
        ttk.Label(hyframe, text="ParValue: ", anchor='center').grid(column=1, row=1, sticky=(N, W, E, S))
        ttk.Label(hyframe, text="Coupon rate: ", anchor='center').grid(column=3, row=1, sticky=(N, W, E, S))
        ttk.Label(hyframe, text="maturity: ", anchor='center').grid(column=5, row=1, sticky=(N, W, E, S))
        ttk.Label(hyframe, text="n : ", anchor='center').grid(column=1, row=2, sticky=(N, W, E, S))
        ttk.Label(hyframe, text="YTMnew : ", anchor='center').grid(column=3, row=2, sticky=(N, W, E, S))
        ttk.Label(hyframe, text="YTMold : ", anchor='center').grid(column=5, row=2, sticky=(N, W, E, S))

        # Define input info label
        input_info = StringVar()
        ttk.Label(hyframe, textvariable=input_info, anchor='center').grid(column=2, row=4, sticky=(W, E), columnspan=4)

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
            ParValue = input_test(ParValue_entry)
            couponrate = input_test(couponrate_entry)
            maturity = input_test_int(maturity_entry)
            n = input_test_int(n_entry)
            YTMnew = input_test(YTMnew_entry)
            YTMold = input_test(YTMold_entry)
            coupon, Pvold, Pvatn, horizonyeild = HY.horizonyeild(ParValue, couponrate, maturity, YTMold, YTMnew, n)
            self.show_result_window(ParValue=ParValue, couponrate=couponrate, maturity=maturity,
                                    n=n, YTMold=YTMold, YTMnew=YTMnew,
                                    coupon=coupon, Pvold=Pvold, Pvatn=Pvatn, horizonyeild=horizonyeild)

        # Define calculate button
        button_cal = ttk.Button(hyframe, text="Calculate HorizonYield")
        button_cal.grid(column=3, row=3, columnspan=2)
        button_cal.bind('<Button-1>', calculate)

        # Define BinomialTree output window

        for child in hyframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def show_result_window(self, **kwargs):
        self.resultwindow = Toplevel()  # Create a new result window
        self.resultwindow.title("HorizonYield Result")
        self.resultwindow.geometry('650x400+550+350')
        self.resultwindow.columnconfigure(0, weight=1)
        self.resultwindow.rowconfigure(0, weight=1)
        text = Text(self.resultwindow, width=650, height=30)
        text.pack()
        stars = '*' * 100
        text.insert(INSERT, f'Set Variables: \n'
                            f'ParValue = {kwargs["ParValue"]},    Coupon rate = {kwargs["couponrate"]},    maturity = {kwargs["maturity"]},\n'
                            f'n = {kwargs["n"]},    YTMold = {kwargs["YTMold"]},    YTMnew = {kwargs["YTMnew"]}\n'
                            f'{stars}\n'
                            f'The pv when we bought the bond is : {kwargs["Pvold"]}\n'
                            f'The coupon reinvestment when we sell the bond at year {kwargs["n"]} is: {kwargs["coupon"]}\n'
                            f'The pv when we sell the bond at year {kwargs["n"]} is : {kwargs["Pvatn"]}\n'
                            f'The horizonyeild at year {kwargs["n"]} is : {kwargs["horizonyeild"]}\n'
                    )

if __name__ == '__main__':
    horizonyeild = HyWindow()
    horizonyeild.hywindow.mainloop()
