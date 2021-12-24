import tkinter as tk

from tkcalendar import DateEntry

from frames import PatientFrame


class PatientDetailsFrame(PatientFrame):

    def __init__(self, master, patient):
        super().__init__(master)
        self.frm_buttons = tk.Frame(self)
        col, row = self.grid_size()
        self.frm_buttons.grid(row=row + 1, column=0, sticky='nsew')
        self.btn_submit = tk.Button(
            self.frm_buttons, text='Submit', state='disabled',
            command=self.submit
        )
        self.btn_submit.grid(row=0, column=0)
        self.btn_edit = tk.Button(
            self.frm_buttons, text='Edit', command=self.edit
        )
        self.btn_edit.grid(row=0, column=1)
        self.patient = patient
        self.set_values(self.patient)
        self.set_state('disabled')
        self.grid(row=0, column=0, sticky='nsew')

    def edit(self):
        print('Edit placeholder')

    def submit(self):
        print('Submit placeholder')

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
