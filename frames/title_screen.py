import tkinter as tk
from pathlib import Path

from frames.const import (APP_FRAMES_GRID, REGISTRATION, SEARCH, SCHEDULE,
                          ADMIN, USER, ADMIN_TITLE_SCREEN, DOCTOR_TITLE_SCREEN,
                          REGISTRATION_TITLE_SCREEN)


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
        admin = Path('images/resized/admin.png')
        user = Path('images/resized/user.png')
        self.img_reg = tk.PhotoImage(file=register)
        self.img_find = tk.PhotoImage(file=find)
        self.img_appointment = tk.PhotoImage(file=appointment)
        self.img_admin = tk.PhotoImage(file=admin)
        self.img_user = tk.PhotoImage(file=user)
        self.frm_buttons = tk.Frame(self)
        self.frm_buttons.grid(row=1, column=0, sticky='nsew')
        self.btn_register = tk.Button(
            self.frm_buttons, text='Register', image=self.img_reg,
            compound=tk.TOP, command=lambda: master.change_frame(REGISTRATION))
        self.btn_find = tk.Button(
            self.frm_buttons, text='Find', image=self.img_find,
            compound=tk.TOP, command=lambda: master.change_frame(SEARCH))
        self.btn_appointment = tk.Button(
            self.frm_buttons, text='Appointment', image=self.img_appointment,
            compound=tk.TOP, command=lambda: master.change_frame(SCHEDULE)
        )
        self.btn_appointment.grid(row=0, column=2)
        self.btn_admin = tk.Button(
            self.frm_buttons, text='Admin', image=self.img_admin,
            compound=tk.TOP, command=lambda: master.change_frame(ADMIN)
        )
        self.btn_user = tk.Button(
            self.frm_buttons, text='User', image=self.img_user,
            compound=tk.TOP, command=lambda: master.change_frame(USER)
        )
        if self.master.current_user['position'] == 'admin':
            screen = ADMIN_TITLE_SCREEN
        elif self.master.current_user['position'] == 'doctor':
            screen = DOCTOR_TITLE_SCREEN
        else:
            screen = REGISTRATION_TITLE_SCREEN
        for column, button in enumerate(screen.values()):
            getattr(self, f'btn_{button}').grid(row=0, column=column)
        self.grid(**APP_FRAMES_GRID)
