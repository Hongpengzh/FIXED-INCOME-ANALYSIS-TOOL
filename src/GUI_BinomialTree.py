"""

"""
__author__ = 'Hongpeng Zhang'
__email__ = 'hongpeng.zhang@nmbu.no'

from tkinter import *
from tkinter import ttk
import BinomialTree as BT

class BtWindow():
    def __init__(self):
        # self.root = root
        self.btwindow = None
        self.createwindow()

    def createwindow(self):
        self.btwindow = Toplevel()  # Create a new toplevel window
        self.btwindow.title("BinomialTree Calculator")
        self.btwindow.geometry('470x150+500+300')
        btframe = ttk.Frame(self.btwindow, padding="3 3 12 12")
        btframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.btwindow.columnconfigure(0, weight=1)
        self.btwindow.rowconfigure(0, weight=1)

        # Define entries for variables
        Par_rate1 = StringVar()
        Par_rate1_entry = ttk.Entry(btframe, width=7, textvariable=Par_rate1)
        Par_rate1_entry.grid(column=2, row=1, sticky=(W, E))

        Par_rate2 = StringVar()
        Par_rate2_entry = ttk.Entry(btframe, width=7, textvariable=Par_rate2)
        Par_rate2_entry.grid(column=4, row=1, sticky=(W, E))

        Par_rate3 = StringVar()
        Par_rate3_entry = ttk.Entry(btframe, width=7, textvariable=Par_rate3)
        Par_rate3_entry.grid(column=6, row=1, sticky=(W, E))

        ParValue = StringVar()
        ParValue_entry = ttk.Entry(btframe, width=7, textvariable=ParValue)
        ParValue_entry.grid(column=2, row=2, sticky=(W, E))

        var = StringVar()
        var_entry = ttk.Entry(btframe, width=7, textvariable=var)
        var_entry.grid(column=4, row=2, sticky=(W, E))

        couponrate = StringVar()
        couponrate_entry = ttk.Entry(btframe, width=7, textvariable=couponrate)
        couponrate_entry.grid(column=6, row=2, sticky=(W, E))

        # Define labels for variables
        ttk.Label(btframe, text="Par rate 1: ", anchor='center').grid(column=1, row=1, sticky=(N, W, E, S))
        ttk.Label(btframe, text="Par rate 2: ", anchor='center').grid(column=3, row=1, sticky=(N, W, E, S))
        ttk.Label(btframe, text="Par rate 3: ", anchor='center').grid(column=5, row=1, sticky=(N, W, E, S))
        ttk.Label(btframe, text="ParValue : ", anchor='center').grid(column=1, row=2, sticky=(N, W, E, S))
        ttk.Label(btframe, text="Volatility : ", anchor='center').grid(column=3, row=2, sticky=(N, W, E, S))
        ttk.Label(btframe, text="coupon rate : ", anchor='center').grid(column=5, row=2, sticky=(N, W, E, S))

        # Define input info label
        input_info = StringVar()
        ttk.Label(btframe, textvariable=input_info, anchor='center').grid(column=2, row=4, sticky=(W, E), columnspan=4)

        def input_test(entry):
            try:
                value = float(entry.get())
            except ValueError:
                input_info.set('Inputs must be numbers, please input again!')
            return value

        def calculate(event):
            par1 = input_test(Par_rate1_entry)
            par2 = input_test(Par_rate2_entry)
            par3 = input_test(Par_rate3_entry)
            ParValue = input_test(ParValue_entry)
            var = input_test(var_entry)
            couponrate = input_test(couponrate_entry)
            s1, s2, s3 = BT.spotrates(par1, par2, par3)
            f1, f2, f3 = BT.forwardrates(s1, s2, s3)
            pv1 = ParValue * couponrate / (1 + s1)
            pv2 = ParValue * couponrate / (1 + s1) + ParValue * (1 + couponrate) / (1 + s2) ** 2
            pv3 = ParValue * couponrate / (1 + s1) + ParValue * couponrate / (1 + s2) ** 2 \
                  + ParValue * (1 + couponrate) / (1 + s3) ** 3
            i1L, i1H = BT.rate_i1(s1, s2, var, ParValue=1, couponrate=0)
            i2L, i2M, i2H = BT.rate_i2(s1, s2, s3, var, ParValue=1, couponrate=0)
            V2L = ParValue * (1 + couponrate) / (1 + i2L) + ParValue * couponrate
            V2M = ParValue * (1 + couponrate) / (1 + i2M) + ParValue * couponrate
            V2H = ParValue * (1 + couponrate) / (1 + i2H) + ParValue * couponrate
            V1L = 0.5 * (V2L / (1 + i1L) + V2M / (1 + i1L)) + ParValue * couponrate
            V1H = 0.5 * (V2H / (1 + i1H) + V2M / (1 + i1H)) + ParValue * couponrate
            V0 = 0.5 * (V1L / (1 + s1) + V1H / (1 + s1))
            self.show_result_window(s1=s1, s2=s2, s3=s3, f1=f1, f2=f2, f3=f3, pv1=pv1, pv2=pv2, pv3=pv3,
                                    i1L=i1L, i1H=i1H,
                                    i2L=i2L, i2M=i2M, i2H=i2H,
                                    V2L=V2L, V2M=V2M, V2H=V2H,
                                    V1L=V1L, V1H=V1H, V0=V0,
                                    par1=par1, par2=par2, par3=par3,
                                    ParValue=ParValue, var=var, couponrate=couponrate)

        # Define calculate button
        button_cal = ttk.Button(btframe, text="Calculate BinomialTree")
        button_cal.grid(column=3, row=3, columnspan=2)
        button_cal.bind('<Button-1>', calculate)

        # Define BinomialTree output window

        for child in btframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def show_result_window(self, **kwargs):
        self.resultwindow = Toplevel()  # Create a new result window
        self.resultwindow.title("BinomialTree Result")
        self.resultwindow.geometry('650x400+550+350')
        # resultframe = ttk.Frame(self.resultwindow, padding="3 3 12 12")
        # resultframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.resultwindow.columnconfigure(0, weight=1)
        self.resultwindow.rowconfigure(0, weight=1)
        text = Text(self.resultwindow, width=650, height=30)
        text.pack()
        stars = '*' * 100
        text.insert(INSERT, f'Set Variables: \n'
                            f'Par rate 1 = {kwargs["par1"]},    Par rate 2 = {kwargs["par2"]},    Par rate 3 = {kwargs["par3"]},\n'
                            f'Par value = {kwargs["ParValue"]},    Coupon rate = {kwargs["couponrate"]},    Volatility = {kwargs["var"]}\n'
                            f'{stars}\n'
                            f's1 = {kwargs["s1"]}         s2 = {kwargs["s2"]}            s3={kwargs["s3"]}\n'
                            f'f1 = {kwargs["f1"]}         f2 = {kwargs["f2"]}            f3={kwargs["f3"]}\n'
                            f'pv1 = {kwargs["pv1"]}         pv2 = {kwargs["pv2"]}            pv3={kwargs["pv3"]}\n'
                            f'{stars}\n'
                            f'i1L = {kwargs["i1L"]}         i1H = {kwargs["i1H"]}\n'
                            f'i2L = {kwargs["i2L"]}         i2M = {kwargs["i2M"]}            i2H={kwargs["i2H"]}\n'
                            f'{stars}\n'
                            f'V2L = {kwargs["V2L"]}         V2M = {kwargs["V2M"]}            V2H={kwargs["V2H"]}\n'
                            f'V1L = {kwargs["V1L"]}         V1H = {kwargs["V1H"]}\n'
                            f'V0 = {kwargs["V0"]}'
                    )

if __name__ == '__main__':
    binomialtree = BtWindow()
    binomialtree.btwindow.mainloop()

