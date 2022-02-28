import tkinter as tk
from tkinter.ttk import Notebook

from frames.const import APP_FRAMES_GRID


class Employee(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.lbl_f_name = tk.Label(self, text='First Name')
        self.lbl_f_name.grid(row=0, column=0, sticky='e')
        self.ent_f_name = tk.Entry(self)
        self.ent_f_name.grid(row=0, column=1, sticky='we')
        self.lbl_m_name = tk.Label(self, text='Middle Name')
        self.lbl_m_name.grid(row=0, column=2, sticky='e')
        self.ent_m_name = tk.Entry(self)
        self.ent_m_name.grid(row=0, column=3, sticky='we')
        self.lbl_l_name = tk.Label(self, text='Last Name')
        self.lbl_l_name.grid(row=0, column=4, sticky='e')
        self.ent_l_name = tk.Entry(self)
        self.ent_l_name.grid(row=0, column=5, sticky='we')
        self.lbl_pos = tk.Label(self, text='Position')
        self.lbl_pos.grid(row=0, column=6, sticky='e')
        self.ent_pos = tk.Entry(self)
        self.ent_pos.grid(row=0, column=7, sticky='we')
        self.lbl_spec = tk.Label(self, text='Specialty')
        self.lbl_spec.grid(row=0, column=8, sticky='e')
        self.ent_spec = tk.Entry(self)
        self.ent_spec.grid(row=0, column=9, sticky='we')


class AdminPanel(Notebook):

    def __init__(self, master):
        super().__init__(master)
        self.frm_add_emp = tk.Frame(self)
        self.frm_create_usr = tk.Frame(self)
        self.add(self.frm_add_emp, text='Add Employee')
        self.add(self.frm_create_usr, text='Create User Account')
        self.grid(APP_FRAMES_GRID)
