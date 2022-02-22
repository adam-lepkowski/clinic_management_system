import tkinter as tk

from frames.const import APP_FRAMES_GRID


class Login(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.lbl_title = tk.Label(self, text='Set Up An Administrator Account')
        self.lbl_title.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.lbl_f_name = tk.Label(self, text='First Name')
        self.lbl_f_name.grid(row=1, column=0, sticky='e')
        self.ent_f_name = tk.Entry(self)
        self.ent_f_name.grid(row=1, column=1, sticky='w')
        self.lbl_m_name = tk.Label(self, text='Middle Name')
        self.lbl_m_name.grid(row=2, column=0, sticky='e')
        self.ent_m_name = tk.Entry(self)
        self.ent_m_name.grid(row=2, column=1, sticky='w')
        self.lbl_l_name = tk.Label(self, text='Last Name')
        self.lbl_l_name.grid(row=3, column=0, sticky='e')
        self.ent_l_name = tk.Entry(self)
        self.ent_l_name.grid(row=3, column=1, sticky='w')
        self.configure_columns()
        self.grid(APP_FRAMES_GRID)

    def configure_columns(self):
        """
        Set equal weight to frame columns
        """
        columns, rows = self.grid_size()
        for column in range(columns):
            self.columnconfigure(column, weight=1)
