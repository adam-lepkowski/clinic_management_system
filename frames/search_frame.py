import tkinter as tk


class SearchFrame(tk.Frame):

    def __init__(self):
        super().__init__()
        self.lbl_title = tk.Label(self, text='Find Patients')
        self.lbl_title.grid(row=0, column=0, sticky='nsew')
