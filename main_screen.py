import tkinter as tk


class MainScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.lbl_title = tk.Label(self, text='Clinic Management System')
        self.lbl_title.grid(row=0, column=0, sticky='we')
        self.frm_buttons = tk.Frame(self)
        self.frm_buttons.grid(row=1, column=0, sticky='nsew')
        self.btn_reg = tk.Button(self.frm_buttons, text='Register')
        self.btn_reg.grid(row=0, column=0)
