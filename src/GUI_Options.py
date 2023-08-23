"""

"""
__author__ = 'Hongpeng Zhang'
__email__ = 'hongpeng.zhang@nmbu.no'

from tkinter import *
from tkinter import ttk
import numpy as np
from sympy import *
import Options as Op

class OpWindow():
    def __init__(self):
        self.opwindow = None
        self.createwindow()

    def createwindow(self):
        self.opwindow = Toplevel()  # Create a new toplevel window
        self.opwindow.title("Options Price Calculator")
        self.opwindow.geometry('470x180+500+300')
        opframe = ttk.Frame(self.opwindow, padding="3 3 12 12")
        opframe.grid(column=0, row=0)
        self.opwindow.columnconfigure(0, weight=1)
        self.opwindow.rowconfigure(0, weight=1)

        # Define entries for variables
        par1 = StringVar()
        par1_entry = ttk.Entry(opframe, width=7, textvariable=par1)
        par1_entry.grid(column=2, row=1, sticky=(W, E))

        par2 = StringVar()
        par2_entry = ttk.Entry(opframe, width=7, textvariable=par2)
        par2_entry.grid(column=4, row=1, sticky=(W, E))

        par3 = StringVar()
        par3_entry = ttk.Entry(opframe, width=7, textvariable=par3)
        par3_entry.grid(column=6, row=1, sticky=(W, E))

        ParValue = StringVar()
        ParValue_entry = ttk.Entry(opframe, width=7, textvariable=ParValue)
        ParValue_entry.grid(column=2, row=2, sticky=(W, E))

        var = StringVar()
        var_entry = ttk.Entry(opframe, width=7, textvariable=var)
        var_entry.grid(column=4, row=2, sticky=(W, E))

        couponrate = StringVar()
        couponrate_entry = ttk.Entry(opframe, width=7, textvariable=couponrate)
        couponrate_entry.grid(column=6, row=2, sticky=(W, E))

        call = StringVar()
        call_entry = ttk.Entry(opframe, width=7, textvariable=call)
        call_entry.grid(column=2, row=3, sticky=(W, E))

        put = StringVar()
        put_entry = ttk.Entry(opframe, width=7, textvariable=put)
        put_entry.grid(column=4, row=3, sticky=(W, E))

        OAS = StringVar()
        OAS_entry = ttk.Entry(opframe, width=7, textvariable=OAS)
        OAS_entry.grid(column=6, row=3, sticky=(W, E))

        # Define labels for variables
        ttk.Label(opframe, text="Par rate 1 : ", anchor='center').grid(column=1, row=1)
        ttk.Label(opframe, text="Par rate 2 : ", anchor='center').grid(column=3, row=1)
        ttk.Label(opframe, text="Par rate 3 : ", anchor='center').grid(column=5, row=1)
        ttk.Label(opframe, text="ParValue : ", anchor='center').grid(column=1, row=2)
        ttk.Label(opframe, text="var : ", anchor='center').grid(column=3, row=2)
        ttk.Label(opframe, text="Coupon rate : ", anchor='center').grid(column=5, row=2)
        ttk.Label(opframe, text="Call value: ", anchor='center').grid(column=1, row=3)
        ttk.Label(opframe, text="Put value: ", anchor='center').grid(column=3, row=3)
        ttk.Label(opframe, text="OAS : ", anchor='center').grid(column=5, row=3)

        # Define input info label
        input_info = StringVar()
        ttk.Label(opframe, textvariable=input_info, anchor='center').grid(column=2, row=5, sticky=(W, E), columnspan=4)

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
            par1 = input_test(par1_entry)
            par2 = input_test(par2_entry)
            par3 = input_test(par3_entry)
            ParValue = input_test(ParValue_entry)
            var = input_test(var_entry)
            couponrate = input_test(couponrate_entry)
            call = input_test(call_entry)
            put = input_test(put_entry)
            OAS = input_test(OAS_entry)
            s1, s2, s3 = Op.spotrates(par1, par2, par3)
            callV0 = Op.V0_call(s1, s2, s3, var, ParValue, couponrate, call)
            putV0 = Op.V0_put(s1, s2, s3, var, ParValue, couponrate, put)
            OAScallV0 = Op.tryOAS_call(OAS, s1, s2, s3, var, ParValue, couponrate, call)
            OASputV0 = Op.tryOAS_put(OAS, s1, s2, s3, var, ParValue, couponrate, put)

            self.show_result_window(par1=par1, par2=par2, par3=par3,
                                    ParValue=ParValue, var=var, couponrate=couponrate,
                                    call=call, put=put, OAS=OAS,
                                    callV0=callV0, putV0=putV0, OAScallV0=OAScallV0, OASputV0=OASputV0)

        # Define calculate button
        button_cal = ttk.Button(opframe, text="Calculate Options Price")
        button_cal.grid(column=3, row=4, columnspan=2)
        button_cal.bind('<Button-1>', calculate)

        for child in opframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def show_result_window(self, **kwargs):
        self.resultwindow = Toplevel()  # Create a new result window
        self.resultwindow.title("Options Price")
        self.resultwindow.geometry('650x400+550+350')
        self.resultwindow.columnconfigure(0, weight=1)
        self.resultwindow.rowconfigure(0, weight=1)
        text = Text(self.resultwindow, width=650, height=30)
        text.pack()
        stars = '*' * 100
        text.insert(INSERT, f'Set Variables: \n'
                            f'Par rate 1 = {kwargs["par1"]},    Par rate 2 = {kwargs["par2"]},    Par rate 3 = {kwargs["par3"]},\n'
                            f'Par value = {kwargs["ParValue"]},     Coupon rate = {kwargs["couponrate"]},    Volatility = {kwargs["var"]}\n'
                            f'Call price = {kwargs["call"]},    Put price = {kwargs["put"]}\n'
                            f'{stars}\n'
                            f'if the bond is callable at par:        V0= {kwargs["callV0"]}\n'
                            f'if the bond is putable at par:         V0= {kwargs["putV0"]}\n'
                            f'{stars}\n'
                            f'if the bond is callable at par and OAS={kwargs["OAS"]}:      V0= {kwargs["OAScallV0"]}\n'
                            f'if the bond is putable at par and OAS={kwargs["OAS"]}:       V0= {kwargs["OASputV0"]} '
                    )

if __name__ == '__main__':
    creditrisk = OpWindow()
    creditrisk.opwindow.mainloop()