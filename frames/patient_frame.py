import tkinter as tk

from tkcalendar import DateEntry

from frames import RegistrationFrame


class PatientDetailsFrame(RegistrationFrame):

    def __init__(self, master, patient):
        super().__init__(master)
        self.btn_register['text'] = 'Edit'
        self.patient = patient
        self.set_values(self.patient)
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

    def set_values(self, patient):
        for col, value in self.patient.items():
            widget = self.patient_ent.get(col, None)
            if isinstance(widget, DateEntry):
                widget.set_date(value)
            elif isinstance(widget, tk.Entry):
                    widget.insert(0, value)
            elif isinstance(widget, tk.StringVar):
                widget.set(value)
