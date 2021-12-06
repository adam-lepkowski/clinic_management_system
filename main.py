import tkinter as tk
import tkinter.messagebox as msg
from sqlite3 import IntegrityError

from db import DB
from registration_frame import RegistrationFrame
from title_screen import TitleScreen


class ClinicManagementSystem(tk.Tk):
    """
    Root window for ClinicManagementSystem GUI
    """
    def __init__(self, db):
        super().__init__()
        self.title("Clinic Management System")
        # set geometry and centre the window
        width = self.winfo_screenwidth() // 2
        height = self.winfo_screenheight() // 2
        self.geometry(f'{width}x{height}+{width // 2}+{height // 2}')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.frames = {
            0: TitleScreen(self),
            1: RegistrationFrame(self)
        }
        self.db = db
        self.frm_title = TitleScreen(self)
        # self.frm_reg = RegistrationFrame(self)
        self.frm_title.grid(row=0, column=1, sticky='nsew')
        # self.frm_reg.btn_register.configure(command=self.register)

    def register(self):
        patient_details = self.frm_reg.get_patient()
        try:
            self.db.register_patient(**patient_details)
            message = 'Patient registered successfully'
            msg.showinfo('Patient registered', message=message)
        except IntegrityError as error:
            message = str(error)
            msg.showerror('Patient not registered', message=message)
