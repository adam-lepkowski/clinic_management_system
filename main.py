import tkinter as tk
import tkinter.messagebox as msg

from db import DB
from registration_frame import RegistrationFrame


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
        self.db = db
        self.geometry(f'{width}x{height}+{width // 2}+{height // 2}')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.frm_reg = RegistrationFrame(self)
        self.frm_reg.grid(row=0, column=1, sticky='nsew')
        self.frm_reg.btn_register.configure(command=self.register)

    def get_patient(self):
        patient_details = {}
        for col_name, widget in self.frm_reg.patient_ent.items():
            patient_details[col_name] = widget.get()
        return patient_details

    def register(self):
        first_name = self.frm_reg.ent_f_name.get()
        self.frm_reg.ent_f_name.delete(0, tk.END)
        if first_name != '':
            self.db.register_patient()
            message = 'Patient registered successfully'
            msg.showinfo('Patient registered', message=message)
        else:
            message = "Invalid input"
            msg.showerror('Patient not registered', message=message)
