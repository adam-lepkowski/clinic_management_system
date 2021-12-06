import tkinter as tk


class TitleScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.lbl_title = tk.Label(self, text='Clinic Management System')
        self.lbl_title.grid(row=0, column=0, sticky='we', pady=10)
        self.img_reg = tk.PhotoImage(file=r'images\resized\register.png')
        self.frm_buttons = tk.Frame(self)
        self.frm_buttons.grid(row=1, column=0, sticky='nsew')
        self.btn_reg = tk.Button(
            self.frm_buttons, text='Register', image=self.img_reg,
            compound=tk.TOP)
        self.btn_reg.grid(row=0, column=0)
        self.grid(row=0, column=1, sticky='nsew')
