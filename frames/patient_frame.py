import tkinter as tk
from frames import RegistrationFrame


class PatientDetailsFrame(RegistrationFrame):

    def __init__(self, master):
        super().__init__(master)
        self.btn_register['text'] = 'Edit'
        self.set_state('disabled')

    @property
    def register(self):
        return self.edit

    def edit(self):
        print('Edit placeholder')

    def set_state(self, state):
        for widget in self.winfo_children():
            if isinstance(widget, tk.OptionMenu):
                widget.config(state=state)
        for widget in self.patient_ent.values():
            if not isinstance(widget, tk.StringVar):
                widget.config(state=state)

class PatientFrame(tk.Toplevel):

    def __init__(self, master, patient):
        super().__init__(master)
        self.master = master
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        self.geometry(f'{width}x{height}')
        self.db = self.master.db
        cols = self.db._get_columns_patient()
        self.patient = {col: value for col, value in zip(cols, patient)}
        self.frm_patient = PatientDetailsFrame(self)
