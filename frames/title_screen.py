import tkinter as tk
from pathlib import Path

from frames.const import APP_FRAMES_GRID


class TitleScreen(tk.Frame):
    """
    Display available features and switch between them.
    """

    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.lbl_title = tk.Label(self, text='Clinic Management System')
        self.lbl_title.grid(row=0, column=0, sticky='we', pady=10)
        register = Path('images/resized/register.png')
        find = Path('images/resized/find.png')
        appointment = Path('images/resized/appointment.png')
        self.img_reg = tk.PhotoImage(file=register)
        self.img_find = tk.PhotoImage(file=find)
        self.img_appointment = tk.PhotoImage(file=appointment)
        self.frm_buttons = tk.Frame(self)
        self.frm_buttons.grid(row=1, column=0, sticky='nsew')
        self.btn_reg = tk.Button(
            self.frm_buttons, text='Register', image=self.img_reg,
            compound=tk.TOP, command=lambda: master.change_frame(1))
        self.btn_reg.grid(row=0, column=0)
        self.btn_find = tk.Button(
            self.frm_buttons, text='Find', image=self.img_find,
            compound=tk.TOP, command=lambda: master.change_frame(2))
        self.btn_find.grid(row=0, column=1)
        self.btn_appointment = tk.Button(
            self.frm_buttons, text='Appointment', image=self.img_appointment,
            compound=tk.TOP, command=lambda: master.change_frame(3)
        )
        self.btn_appointment.grid(row=0, column=2)
        self.grid(**APP_FRAMES_GRID)
