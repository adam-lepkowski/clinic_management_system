import tkinter as tk

from tkcalendar import DateEntry


class Appointment(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.lbl_title = tk.Label(self, text='Appointment Schedule')
        self.lbl_title.grid(
            row=0, column=0, sticky='nsew', pady=10, columnspan=5
        )
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
        self.cnv_appointment = tk.Canvas(self, bg='white')
        self.cnv_appointment.grid(row=2, column=0, columnspan=5, sticky='nsew')
        self.frm_hours = tk.Frame(self.cnv_appointment)
        self.cnv_frm = self.cnv_appointment.create_window(
            (0, 0), anchor=tk.NW, window=self.frm_hours)
        self.get_schedule()
        self._configure_columns()
        self.cnv_appointment.bind('<Configure>', self.set_schedule_width)
        self.grid(row=0, column=1, sticky='nsew')

    def _configure_columns(self):
        """
        Set equal weight to frame columns
        """
        columns, rows = self.grid_size()
        for column in range(columns):
            self.columnconfigure(column, weight=1)

        columns, rows = self.frm_hours.grid_size()
        for column in range(columns):
            self.frm_hours.columnconfigure(column, weight=1)

    def set_specialists(self, event):
        specialty = self.var_specialty.get()
        self.var_doctor.set('')
        self.opt_doctor.destroy()
        doctors = self.specialties[specialty]
        self.opt_doctor = tk.OptionMenu(self, self.var_doctor, *doctors)
        self.opt_doctor.grid(row=1, column=4, sticky='we')

    def get_schedule(self):
        lbl_hour = tk.Label(self.frm_hours, text='8:00 AM', bg='lightgrey')
        lbl_hour.grid(row=0, column=0, pady=10, padx=10, sticky='we')
        available_hour = tk.Label(self.frm_hours, bg='lightgrey')
        available_hour.grid(row=0, column=1, pady=10, padx=10, sticky='we')
        available_hour.bind('<Double-Button-1>', self.schedule_appointment)

    def set_schedule_width(self, event):
        canvas_width = event.width
        self.cnv_appointment.itemconfig(self.cnv_frm, width=canvas_width)

    def schedule_appointment(self, event):
        frm = tk.Toplevel(self)
        date = self.ent_date.get()
        tk.Label(frm, text=f'Date: {date}').grid(row=0, column=0)
