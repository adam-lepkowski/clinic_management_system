import tkinter as tk

from tkcalendar import DateEntry


class Appointment(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.lbl_title = tk.Label(self, text='Appointment Schedule')
        self.lbl_title.grid(row=0, column=0, sticky='nsew', pady=10)
        self.ent_date = DateEntry(self, date_pattern='y-mm-dd')
        self.ent_date.grid(row=1, column=0)
        self.lbl_specialty = tk.Label(self, text='Specialty')
        self.lbl_specialty.grid(row=1, column=1, sticky='we')
        self.specialties = {
            'All': ['Der_1', 'Der_2', 'Oph_1', 'Oph_2'],
            'Dermatology': ['Der_1', 'Der_2'],
            'Ophthalmology': ['Oph_1', 'Oph_2']
        }
        self.var_specialty = tk.StringVar(self)
        self.opt_specialty = tk.OptionMenu(
            self, self.var_specialty, *list(self.specialties.keys()),
            command=self.set_specialists
        )
        self.opt_specialty.grid(row=1, column=2, sticky='we')
        self.lbl_doctor = tk.Label(self, text='Doctor')
        self.lbl_doctor.grid(row=1, column=3, sticky='we')
        # todo użyć variable trace, zeby śledzić zmiany w stringvar
        self.var_doctor = tk.StringVar(self)
        self.opt_doctor = tk.OptionMenu(
            self, self.var_doctor, *self.specialties['All']
        )
        self.opt_doctor.grid(row=1, column=4, sticky='we')
        self.grid(row=0, column=1, sticky='nsew')

    def set_specialists(self, event):
        specialty = self.var_specialty.get()
        self.var_doctor.set('')
        self.opt_doctor.destroy()
        doctors = self.specialties[specialty]
        self.opt_doctor = tk.OptionMenu(self, self.var_doctor, *doctors)
        self.opt_doctor.grid(row=1, column=4, sticky='we')
