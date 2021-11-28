import tkinter as tk


class RegistrationFrame(tk.Frame):
    """
    Class used to represent patient registration frame and it's child widgets
    """

    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.lbl_pat_details = tk.Label(self, text='Patient Details')
        self.lbl_pat_details.grid(row=0, column=0, sticky='we', columnspan=2)
        self.lbl_f_name = tk.Label(self, text='First Name')
        self.lbl_f_name.grid(row=1, column=0, sticky='e')
        self.ent_f_name = tk.Entry(self)
        self.ent_f_name.grid(row=1, column=1, sticky='w')
        self.btn_register = tk.Button(self, text='Register')
        self.btn_register.grid(row=2, column=0)
