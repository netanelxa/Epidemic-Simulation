from tkinter import Tk, IntVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import PhotoImage
from tkinter import RIGHT, END, LEFT
from tkinter import Checkbutton
from tkinter import DISABLED, NORMAL

import tkinter.ttk as ttk


class MainWindow:
    def __init__(self, list):
        self.paramters = []
        self.list = list

        window = Tk()
        window.title("Computational Biology Ex1 Ido Netanel")
        window.geometry('600x450')

        image1 = PhotoImage(file="pngfuel.com.png")
        panel1 = Label(window, image=image1)
        panel1.place(x=215, y=145, relwidth=1, relheight=1)

        # panel1.pack(side='top', fill='both', expand='yes')
        panel1.image = image1

        combo = ttk.Combobox(window, width=9)
        combo['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        combo.place(x=300, y=100)
        LC1 = Label(window, text="Select Experiment or create one", font=("Times", 20, "italic"))
        LC1.place(x=125, y=55)
        LC = Label(window, text="Experiment number")
        LC.place(x=120, y=100)
        L1 = Label(window, text="Number of creatures")
        L1.pack(side=LEFT)
        L1.place(x=120, y=150)
        E1 = Entry(window)
        E1.pack(side=RIGHT)
        E1.place(x=300, y=150)
        L2 = Label(window, text="Probability to infect")
        L2.pack(side=LEFT)
        L2.place(x=120, y=185)
        E2 = Entry(window)
        E2.pack(side=RIGHT)
        E2.place(x=300, y=185)
        L3 = Label(window, text="Isolation level (k)")
        L3.pack(side=LEFT)
        L3.place(x=120, y=220)
        E3 = Entry(window)
        E3.pack(side=RIGHT)
        E3.place(x=300, y=220)

        def checked():
            if self.value_check.get():
                L4.config(state=NORMAL)
                L5.config(state=NORMAL)
                L6.config(state=NORMAL)
                E4.config(state=NORMAL)
                E5.config(state=NORMAL)
            else:
                L4.config(state=DISABLED)
                L5.config(state=DISABLED)
                L6.config(state=DISABLED)
                E4.delete(0, END)
                E5.delete(0, END)
                E4.config(state=DISABLED)
                E5.config(state=DISABLED)

        self.value_check = IntVar()
        CB = Checkbutton(window, text="Isolation levels change over time?", variable=self.value_check,
                         command=checked).place(
            x=100, y=260)
        self.value_check.set(0)
        L4 = Label(window, text="New K: ")
        L4.pack(side=LEFT)
        L4.config(state=DISABLED)
        L4.place(x=120, y=300)
        E4 = Entry(window)
        E4.pack(side=RIGHT)
        E4.place(x=170, y=300, width=50)
        E4.config(state=DISABLED)
        L5 = Label(window, text="After:")
        L5.pack(side=LEFT)
        L5.config(state=DISABLED)
        L5.place(x=240, y=300)
        E5 = Entry(window)
        E5.pack(side=RIGHT)
        E5.config(state=DISABLED)
        E5.place(x=280, y=300, width=50)
        L6 = Label(window, text="Steps")
        L6.pack(side=LEFT)
        L6.config(state=DISABLED)
        L6.place(x=330, y=300)

        def close_window():
            window.destroy()

        def clicked():
            if self.value_check.get() == 1:
                if E4.get() and E5.get():
                    try:
                        if int(E4.get()) > 8 or int(E4.get()) < 0 and E4.get():
                            E4.delete(0, END)
                        if int(E5.get()) < 1:
                            E5.delete(0, END)
                        else:
                            self.paramters.insert(3,int(E4.get()))
                            self.paramters.insert(4,int(E5.get()))
                    except:
                        self.paramters = []
                        L2 = Label(window, text="Please choose correct values")
                        L2.place(x=120, y=340)
                else:
                    self.paramters = []
                    L2 = Label(window, text="Please choose correct values")
                    L2.place(x=120, y=340)
            try:
                if int(E1.get()) > 3000 or int(E1.get()) < 0:
                    E1.delete(0, END)
                    L1 = Label(window, text="between 0-200")
                    L1.place(x=480, y=150)
                if int(E2.get()) > 100 or int(E2.get()) < 0:
                    E2.delete(0, END)
                    L2 = Label(window, text="between 0-100")
                    L2.place(x=480, y=185)
                if int(E3.get()) > 8 or int(E3.get()) < -1:
                    E3.delete(0, END)
                    L3 = Label(window, text="between 0-8")
                    L3.place(x=480, y=220)
                else:
                    if (self.value_check.get() == 0) or (self.value_check.get() == 1 and E4.get() and E5.get()):
                        self.paramters.append(int(E1.get()))
                        self.paramters.append(int(E2.get()))
                        self.paramters.append(int(E3.get()))
                        close_window()
                        return self.paramters
            except:
                self.paramters = []
                L2 = Label(window, text="Please choose correct values")
                L2.place(x=120, y=340)

        btn = Button(window, text='Run', command=clicked)
        btn.place(x=275, y=370)

        def parse():
            try:
                E1.delete(0, END)
                E2.delete(0, END)
                E3.delete(0, END)
                set = int(combo.get()) - 1
                E1.insert(0, self.list[set][0])
                E2.insert(0, self.list[set][1])
                E3.insert(0, self.list[set][2])
            except:
                self.paramters = []
                L2 = Label(window, text="Please choose correct values")
                L2.place(x=120, y=340)
                L3 = Label(window, text="between 0 -8")
                L3.place(x=480, y=220)
                L1 = Label(window, text="between 0-100")
                L1.place(x=480, y=185)
                L = Label(window, text="between 0-200")
                L.place(x=480, y=150)

        button1 = Button(window, height=1, width=5, text="Select", command=parse)
        button1.place(x=400, y=95)

        window.mainloop()