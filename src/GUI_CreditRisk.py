"""

"""
__author__ = 'Hongpeng Zhang'
__email__ = 'hongpeng.zhang@nmbu.no'

from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
import numpy_financial as npf
import CreditRisk as CR

class CrWindow():
    def __init__(self):
        self.crwindow = None
        self.createwindow()

    def createwindow(self):
        self.crwindow = Toplevel()  # Create a new toplevel window
        self.crwindow.title("Credit Risk Calculator")
        self.crwindow.geometry('470x150+500+300')
        crframe = ttk.Frame(self.crwindow, padding="3 3 12 12")
        crframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.crwindow.columnconfigure(0, weight=1)
        self.crwindow.rowconfigure(0, weight=1)

        # Define entries for variables
        ParValue = StringVar()
        ParValue_entry = ttk.Entry(crframe, width=7, textvariable=ParValue)
        ParValue_entry.grid(column=2, row=1, sticky=(W, E))

        couponrate = StringVar()
        couponrate_entry = ttk.Entry(crframe, width=7, textvariable=couponrate)
        couponrate_entry.grid(column=4, row=1, sticky=(W, E))

        maturity = StringVar()
        maturity_entry = ttk.Entry(crframe, width=7, textvariable=maturity)
        maturity_entry.grid(column=6, row=1, sticky=(W, E))

        POD1 = StringVar()
        POD1_entry = ttk.Entry(crframe, width=7, textvariable=POD1)
        POD1_entry.grid(column=2, row=2, sticky=(W, E))

        recoverrate = StringVar()
        recoverrate_entry = ttk.Entry(crframe, width=7, textvariable=recoverrate)
        recoverrate_entry.grid(column=4, row=2, sticky=(W, E))

        YTM = StringVar()
        YTM_entry = ttk.Entry(crframe, width=7, textvariable=YTM)
        YTM_entry.grid(column=6, row=2, sticky=(W, E))

        # Define labels for variables
        ttk.Label(crframe, text="ParValue : ", anchor='center').grid(column=1, row=1, sticky=(N, W, E, S))
        ttk.Label(crframe, text="coupon rate : ", anchor='center').grid(column=3, row=1, sticky=(N, W, E, S))
        ttk.Label(crframe, text="maturity : ", anchor='center').grid(column=5, row=1, sticky=(N, W, E, S))
        ttk.Label(crframe, text="POD1 : ", anchor='center').grid(column=1, row=2, sticky=(N, W, E, S))
        ttk.Label(crframe, text="recover rate : ", anchor='center').grid(column=3, row=2, sticky=(N, W, E, S))
        ttk.Label(crframe, text="YTM : ", anchor='center').grid(column=5, row=2, sticky=(N, W, E, S))

        # Define input info label
        input_info = StringVar()
        ttk.Label(crframe, textvariable=input_info, anchor='center').grid(column=2, row=4, sticky=(W, E), columnspan=4)

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
            POD1 = input_test(POD1_entry)
            recoverrate = input_test(recoverrate_entry)
            YTM = input_test(YTM_entry)
            df = pd.DataFrame(np.zeros((maturity, 8)), index=np.arange(1, maturity + 1),
                              columns=['Exposure', 'Recovery', 'LGD', 'POD', 'POS', 'Expected Loss', 'DF',
                                       'PV of Expected Loss'])
            for index in df.index:
                df.loc[index, :] = np.array([CR.Exposuren(index), CR.Recoveryn(index), CR.LGDn(index), CR.PODn(index),
                                             CR.POSn(index), CR.ExpLoss(index), CR.DF(index), CR.PVofExpLoss(index)])
            CVA = df['PV of Expected Loss'].sum()
            pv = npf.pv(YTM, maturity, -ParValue * couponrate, -ParValue)
            pvafrisk = pv - CVA
            cashflow = np.hstack((-pvafrisk, np.full(maturity - 1, ParValue * couponrate), ParValue * (1 + couponrate)))
            YTMafrist = npf.irr(cashflow)
            creditspread = YTMafrist - YTM

            self.show_result_window(ParValue=ParValue, couponrate=couponrate, maturity=maturity,
                                    POD1=POD1, recoverrate=recoverrate, YTM=YTM,
                                    CVA=CVA, pvafrisk=pvafrisk, creditspread=creditspread)

        # Define calculate button
        button_cal = ttk.Button(crframe, text="Calculate Credit Risk")
        button_cal.grid(column=3, row=3, columnspan=2)
        button_cal.bind('<Button-1>', calculate)

        # Define BinomialTree output window

        for child in crframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def show_result_window(self, **kwargs):
        self.resultwindow = Toplevel()  # Create a new result window
        self.resultwindow.title("Credit Risk")
        self.resultwindow.geometry('650x400+550+350')
        self.resultwindow.columnconfigure(0, weight=1)
        self.resultwindow.rowconfigure(0, weight=1)
        text = Text(self.resultwindow, width=650, height=30)
        text.pack()
        stars = '*' * 100
        text.insert(INSERT, f'Set Variables: \n'
                            f'ParValue = {kwargs["ParValue"]},    Couponrate = {kwargs["couponrate"]},    maturity = {kwargs["maturity"]},\n'
                            f'POD1 = {kwargs["POD1"]},    recover rate = {kwargs["recoverrate"]},    YTM = {kwargs["YTM"]}\n'
                            f'{stars}\n'
                            f'The CVA is: {kwargs["CVA"]}\n'
                            f'The PV after risk is: {kwargs["pvafrisk"]}\n'
                            f'The credit spread is: {kwargs["creditspread"]}'
                    )

if __name__ == '__main__':
    creditrisk = CrWindow()
    creditrisk.crwindow.mainloop()
