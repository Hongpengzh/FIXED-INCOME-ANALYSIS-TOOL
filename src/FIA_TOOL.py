"""

"""
__author__ = 'Hongpeng Zhang'
__email__ = 'hongpeng.zhang@nmbu.no'

from tkinter import *
from tkinter import ttk
from GUI_duration import DurationWindow
from GUI_BinomialTree import BtWindow
from GUI_CreditRisk import CrWindow
from GUI_HorizonYield import HyWindow
from GUI_SwapRate import SrWindow
from GUI_Options import OpWindow

class FixIncomeCal:
    def __init__(self, root):
        self.root = root
        self.create_main_window()

    def create_main_window(self):
        self.main_frame = Frame(self.root, width=455, height=200)
        self.main_frame.grid()
        # Define and place different calculator button.
        self.button_duration = Button(self.main_frame, text="Duration", command=self.show_duration_window)
        self.button_duration.place(x=50, y=30, width=100, height=40)
        self.button_binomialtree = Button(self.main_frame, text="BinomialTree", command=self.show_binomialtree_window)
        self.button_binomialtree.place(x=50, y=110, width=100, height=40)
        self.button_creditrisk = Button(self.main_frame, text="CreditRisk", command=self.show_creditrisk_window)
        self.button_creditrisk.place(x=175, y=30, width=100, height=40)
        self.button_horizonyield = Button(self.main_frame, text="HorizonYield", command=self.show_horizonyield_window)
        self.button_horizonyield.place(x=175, y=110, width=100, height=40)
        self.button_swaprate = Button(self.main_frame, text="SwapRate", command=self.show_swaprate_window)
        self.button_swaprate.place(x=300, y=30, width=100, height=40)
        self.button_options = Button(self.main_frame, text="Options&OAS", command=self.show_options_window)
        self.button_options.place(x=300, y=110, width=100, height=40)
        self.author = ttk.Label(self.main_frame, text="Author: Patrick Zhang", anchor='center',
                                font=('Century', 9, 'normal'), foreground='gray')
        self.author.place(x=120, y=180, width=130, height=20)
        self.email = ttk.Label(self.main_frame, text="Email: Hongpeng.zhang@nmbu.no", anchor='center',
                               font=('Century', 9, 'normal'), foreground='gray')
        self.email.place(x=255, y=180, width=200, height=20)

    def show_duration_window(self):
        DurationWindow()

    def show_binomialtree_window(self):
        BtWindow()

    def show_creditrisk_window(self):
        CrWindow()

    def show_horizonyield_window(self):
        HyWindow()

    def  show_swaprate_window(self):
        SrWindow()

    def  show_options_window(self):
        OpWindow()

if __name__ == '__main__':
    root = Tk()
    root.title("FIXED INCOME ANALYSIS TOOL 1.0.0")
    root.geometry('455x200+500+300')
    calculator = FixIncomeCal(root)
    root.mainloop()

