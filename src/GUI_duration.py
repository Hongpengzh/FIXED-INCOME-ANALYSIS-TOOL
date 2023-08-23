from tkinter import *
from tkinter import ttk
import Duration as dur

class DurationWindow():
    def __init__(self):
        # self.root = root
        self.durationwindow = None
        self.createwindow()

    def createwindow(self):
        self.durationwindow = Toplevel()  # Create a new toplevel window
        self.durationwindow.title("Duration Calculator")
        self.durationwindow.geometry('470x180+500+300')
        durationframe = ttk.Frame(self.durationwindow, padding="3 3 12 12")
        durationframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.durationwindow.columnconfigure(0, weight=1)
        self.durationwindow.rowconfigure(0, weight=1)

        # Define entries for variables
        Parvalue = StringVar()
        Parvalue_entry = ttk.Entry(durationframe, width=7, textvariable=Parvalue)
        Parvalue_entry.grid(column=2, row=1, sticky=(W, E))

        Couponrate = StringVar()
        Couponrate_entry = ttk.Entry(durationframe, width=7, textvariable=Couponrate)
        Couponrate_entry.grid(column=4, row=1, sticky=(W, E))

        YTM = StringVar()
        YTM_entry = ttk.Entry(durationframe, width=7, textvariable=YTM)
        YTM_entry.grid(column=6, row=1, sticky=(W, E))

        Maturity = StringVar()
        Maturity_entry = ttk.Entry(durationframe, width=7, textvariable=Maturity)
        Maturity_entry.grid(column=2, row=2, sticky=(W, E))

        t = StringVar()
        t_entry = ttk.Entry(durationframe, width=7, textvariable=t)
        t_entry.grid(column=4, row=2, sticky=(W, E))

        T = StringVar()
        T_entry = ttk.Entry(durationframe, width=7, textvariable=T)
        T_entry.grid(column=6, row=2, sticky=(W, E))

        # Define labels for variables
        ttk.Label(durationframe, text="Par value: ", anchor='center').grid(column=1, row=1, sticky=(N, W, E, S))
        ttk.Label(durationframe, text="Coupon rate: ", anchor='center').grid(column=3, row=1, sticky=(N, W, E, S))
        ttk.Label(durationframe, text="YTM: ", anchor='center').grid(column=5, row=1, sticky=(N, W, E, S))
        ttk.Label(durationframe, text="Maturity : ", anchor='center').grid(column=1, row=2, sticky=(N, W, E, S))
        ttk.Label(durationframe, text="t : ", anchor='center').grid(column=3, row=2, sticky=(N, W, E, S))
        ttk.Label(durationframe, text="T : ", anchor='center').grid(column=5, row=2, sticky=(N, W, E, S))

        # Define input info label
        input_info = StringVar()
        ttk.Label(durationframe, textvariable=input_info, anchor='center').grid(column=2, row=4, sticky=(W, E), columnspan=4)

        def input_test(entry):
            try:
                value = float(entry.get())
            except ValueError:
                input_info.set('Inputs must be numbers, please input again!')
            return value

        def calculate(event):
            Parvalue = input_test(Parvalue_entry)
            Couponrate = input_test(Couponrate_entry)
            YTM = input_test(YTM_entry)
            Maturity = input_test(Maturity_entry)
            t = input_test(t_entry)
            T = input_test(T_entry)
            duration_mac = round(dur.MacaulayDuration(Parvalue, Couponrate, YTM, Maturity, t, T), 5)
            duration_mod = round(dur.ModDuration(duration_mac, YTM, ann=1), 5)
            Mac.set(duration_mac)
            Mod.set(duration_mod)

        # Define calculate button
        button_cal = ttk.Button(durationframe, text="Calculate Duration")
        button_cal.grid(column=3, row=3, columnspan=2)
        button_cal.bind('<Button-1>', calculate)

        # Define MacaulayDuration and ModDuration output label
        ttk.Label(durationframe, text="Macaulay: ").grid(column=1, row=5, sticky=(N, W, E, S))
        ttk.Label(durationframe, text="Mod: ", anchor='e').grid(column=3, row=5, sticky=(N, W, E, S))
        Mac = StringVar()
        ttk.Label(durationframe, textvariable=Mac, anchor='center').grid(column=2, row=5, sticky=(W, E))
        Mod = StringVar()
        ttk.Label(durationframe, textvariable=Mod, anchor='center').grid(column=4, row=5, sticky=(W, E))

        for child in durationframe.winfo_children():
            child.grid_configure(padx=5, pady=5)


if __name__ == '__main__':
    durationframe = DurationWindow()
    durationframe.durationwindow.mainloop()


