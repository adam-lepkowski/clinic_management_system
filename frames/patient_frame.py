import tkinter as tk
from frames import RegistrationFrame


class PatientDetailsFrame(RegistrationFrame):

    def __init__(self, master):
        super().__init__(master)
        self.btn_register['text'] = 'Edit'

    @property
    def register(self):
        return self.edit

    def edit(self):
        print('Edit placeholder')


class PatientFrame(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        self.geometry(f'{width}x{height}')
        self.db = self.master.db
        self.frm_patient = PatientDetailsFrame(self)
