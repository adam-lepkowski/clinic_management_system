import tkinter as tk


class PatientFrame(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        self.geometry(f'{width}x{height}')
        self.db = self.master.db
