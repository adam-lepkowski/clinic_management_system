import tkinter as tk
from tkinter.ttk import Notebook

from frames.const import APP_FRAMES_GRID

class AdminPanel(Notebook):

    def __init__(self, master):
        super().__init__(master)
        self.frm_add_emp = tk.Frame(self)
        self.frm_create_usr = tk.Frame(self)
        self.add(self.frm_add_emp, text='Add Employee')
        self.add(self.frm_create_usr, text='Create User Account')
        self.grid(APP_FRAMES_GRID)
