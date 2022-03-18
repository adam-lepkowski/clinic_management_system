import tkinter as tk
from frames.const import APP_FRAMES_GRID


class UserPanel(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.lbl_curr_pwd = tk.Label(self, text='Current Password')
        self.lbl_curr_pwd.grid(row=0, column=0, sticky='e')
        self.ent_curr_pwd = tk.Entry(self)
        self.ent_curr_pwd.grid(row=0, column=1, sticky='w')
        self.lbl_new_pwd = tk.Label(self, text='New Password')
        self.lbl_new_pwd.grid(row=1, column=0, sticky='e')
        self.ent_new_pwd = tk.Entry(self)
        self.ent_new_pwd.grid(row=1, column=1, sticky='w')
        self.lbl_con_pwd = tk.Label(self, text='Confirm Password')
        self.lbl_con_pwd.grid(row=2, column=0, sticky='e')
        self.ent_con_pwd = tk.Entry(self)
        self.ent_con_pwd.grid(row=2, column=1, sticky='w')
        self.btn_update = tk.Button(self, text='Update Password')
        self.btn_update.grid(row=3, column=1, sticky='w')
        self.grid(**APP_FRAMES_GRID)
