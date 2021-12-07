import tkinter as tk


class SearchFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.lbl_title = tk.Label(self, text='Find Patients')
        self.lbl_title.grid(row=0, column=0, sticky='nsew')
        self.lbl_f_name = tk.Label(self, text='First Name')
        self.lbl_f_name.grid(row=1, column=0, sticky='e')
        self.ent_f_name = tk.Entry(self)
        self.ent_f_name.grid(row=1, column=1, sticky='we')
        self.frm_buttons = tk.Frame(self)
        self.frm_buttons.grid(row=2, column=0, sticky='we')
        self.btn_find = tk.Button(self.frm_buttons, text='Find')
        self.btn_find.grid(row=0, column=0)
        self.grid(row=0, column=1, sticky='nsew')
