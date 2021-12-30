import tkinter as tk

from tkcalendar import DateEntry


class Appointment(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.lbl_title = tk.Label(self, text='Appointment Schedule')
        self.lbl_title.grid(row=0, column=0, sticky='nsew', pady=10)
        self.ent_date = DateEntry(self, date_pattern='y-mm-dd')
        self.ent_date.grid(row=1, column=0)
        self.grid(row=0, column=1, sticky='nsew')
