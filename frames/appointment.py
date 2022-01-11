import tkinter as tk
import tkinter.messagebox as msg
from datetime import datetime, timedelta

from tkcalendar import DateEntry


class Appointment(tk.Toplevel):

    def __init__(self, master, date, doctor, specialists, db):
        super().__init__(master)
        self.master = master
        self.db = db
        self.date = date
        self.lbl_date = tk.Label(self, text=f'Date: {date}')
        self.lbl_date.grid(row=0, column=0)
        self.var_spec = tk.StringVar(self)
        self.opt_specialty = tk.OptionMenu(
            self, self.var_spec, *specialists
        )
        self.opt_specialty.grid(row=0, column=1)
        if doctor != '':
            self.var_spec.set(doctor)
        self.lbl_pat = tk.Label(self, text='Patient')
        self.lbl_pat.grid(row=0, column=2)
        self.ent_pat = tk.Entry(self)
        self.ent_pat.grid(row=0, column=3)
        self.btn_schedule = tk.Button(
            self, text='Schedule', command=self.confirm_appointment
        )
        self.btn_schedule.grid(row=0, column=4)

    def confirm_appointment(self):
        document = self.ent_pat.get()
        patient = self.db.find_patient(document_no=document)[0]
        doctor = self.var_spec.get()
        if patient and doctor:
            title = 'Appointment scheduled'
            message = f'Patient scheduled for an appointment'
            patient_id = patient[0]
            self.db.register_appointment(patient_id, self.date, doctor)
            msg.showinfo(title=title, message=message)
        else:
            msg.showinfo('Patient not found', 'Patient not found')


class Schedule(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.lbl_title = tk.Label(self, text='Appointment Schedule')
        self.lbl_title.grid(
            row=0, column=0, sticky='nsew', pady=10, columnspan=5
        )
        self.btn_back = tk.Button(self)
        self.btn_back.grid(row=1, column=0, sticky='e')
        self.btn_fwd = tk.Button(self)
        self.btn_fwd.grid(row=1, column=2, sticky='w')
        self.ent_date = DateEntry(self, date_pattern='y-mm-dd')
        self.ent_date.grid(row=1, column=1, sticky='we')
        self.lbl_specialty = tk.Label(self, text='Specialty')
        self.lbl_specialty.grid(row=1, column=3, sticky='we')
        self.specialties = {
            'All': ['Der_1', 'Der_2', 'Oph_1', 'Oph_2'],
            'Dermatology': ['Der_1', 'Der_2'],
            'Ophthalmology': ['Oph_1', 'Oph_2']
        }
        self.var_specialty = tk.StringVar(self)
        self.var_specialty.set('All')
        self.opt_specialty = tk.OptionMenu(
            self, self.var_specialty, *list(self.specialties.keys()),
            command=self.set_specialists
        )
        self.opt_specialty.grid(row=1, column=4, sticky='we')
        self.lbl_doctor = tk.Label(self, text='Doctor')
        self.lbl_doctor.grid(row=1, column=5, sticky='we')
        # todo użyć variable trace, zeby śledzić zmiany w stringvar
        self.var_doctor = tk.StringVar(self)
        self.opt_doctor = tk.OptionMenu(
            self, self.var_doctor, *self.specialties['All']
        )
        self.opt_doctor.grid(row=1, column=6, sticky='we')
        self.cnv_appointment = tk.Canvas(self, bg='white')
        self.cnv_appointment.grid(row=2, column=0, columnspan=7, sticky='nsew')
        self.frm_hours = tk.Frame(self.cnv_appointment)
        self.cnv_frm = self.cnv_appointment.create_window(
            (0, 0), anchor=tk.NW, window=self.frm_hours)
        self.scr_cnv = tk.Scrollbar(self, command=self.cnv_appointment.yview)
        self.scr_cnv.grid(row=2, column=7, sticky='wns')
        self.cnv_appointment.configure(yscrollcommand=self.scr_cnv.set)
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
        start_hour = 8
        end_hour = 16
        app_time = timedelta(minutes=30)
        date = self.ent_date.get()
        date = datetime.strptime(date, '%Y-%m-%d').replace(hour=start_hour)
        row = 0
        while date.hour != end_hour:
            lbl_text = date.strftime('%H:%M')
            date += app_time
            lbl_hour = tk.Label(self.frm_hours, text=lbl_text, bg='lightgrey')
            lbl_hour.grid(row=row, column=0, pady=10, padx=10, sticky='we')
            available_hour = tk.Label(self.frm_hours, bg='lightgrey')
            available_hour.grid(row=row, column=1, pady=10, padx=10, sticky='we')
            available_hour.bind('<Double-Button-1>', self.schedule_appointment)
            row += 1

    def set_schedule_width(self, event):
        canvas_width = event.width
        self.cnv_appointment.itemconfig(self.cnv_frm, width=canvas_width)

    def schedule_appointment(self, event):
        date = self.ent_date.get()
        doc = self.var_doctor.get()
        spec = self.specialties[self.var_specialty.get()]
        db = self.master.db
        Appointment(self, date, doc, spec, db)
