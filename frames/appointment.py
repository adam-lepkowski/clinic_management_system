import tkinter as tk
import tkinter.messagebox as msg
from datetime import datetime, timedelta
import itertools

from tkcalendar import DateEntry


class Appointment(tk.Toplevel):

    def __init__(self, master, datetime, doctor, specialists, db):
        super().__init__(master)
        self.master = master
        self.db = db
        self.app_datetime = datetime
        self.lbl_date = tk.Label(self, text=f'Date: {datetime}')
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
        self.lbl_scheduled = tk.Label(self, text='Scheduled appointments')
        self.lbl_scheduled.grid(row=2, column=0)
        self.frm_scheduled = tk.Frame(self)
        self.frm_scheduled.grid(row=3, column=0, columnspan=5, sticky='nsew')
        self.show_scheduled()

    def confirm_appointment(self):
        document = self.ent_pat.get()
        patient = self.db.find_patient(document_no=document)
        patient = patient[0] if patient else []
        doctor = self.var_spec.get()
        if patient and doctor:
            title = 'Appointment scheduled'
            message = f'Patient scheduled for an appointment'
            patient_id = patient[0]
            self.db.register_appointment(patient_id, self.app_datetime, doctor)
            self.show_scheduled()
            msg.showinfo(title=title, message=message)
        elif not patient:
            msg.showinfo('Patient not found', 'Patient not found')
        elif not doctor:
            msg.showinfo('No doctor selected', 'Pick a doctor')

    def show_scheduled(self):
        for child in self.frm_scheduled.winfo_children():
            child.destroy()
        appointments = self.db.find_appointment(app_datetime=self.app_datetime)
        for row, appointment in enumerate(appointments):
            appointment = '\t'.join([str(val) for val in appointment])
            lbl = tk.Label(self.frm_scheduled, text=appointment)
            lbl.grid(row=row, column=0)
            lbl.bind('<Button-1>', self.cancel_appointment)

    def cancel_appointment(self, event):
        text = event.widget['text'].split('\t')
        doctor = text[-1]
        title = 'Cancel appointment'
        message = f"Are you sure you want to cancel {self.app_datetime}\
                    appointment with doctor {doctor}"
        if msg.askyesno(title=title, message=message):
            self.db.cancel_appointment(self.app_datetime, doctor)
            self.show_scheduled()


class Schedule(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.lbl_title = tk.Label(self, text='Appointment Schedule')
        self.lbl_title.grid(
            row=0, column=0, sticky='nsew', pady=10, columnspan=7
        )
        self.btn_back = tk.Button(self)
        self.btn_back.grid(row=1, column=0, sticky='e')
        self.btn_fwd = tk.Button(self)
        self.btn_fwd.grid(row=1, column=2, sticky='w')
        self.ent_date = DateEntry(self, date_pattern='y-mm-dd')
        self.ent_date.grid(row=1, column=1, sticky='we')
        self.lbl_specialty = tk.Label(self, text='Specialty')
        self.lbl_specialty.grid(row=1, column=3, sticky='we')
        self.specialties = {}
        self.set_specialties()
        self.var_specialty = tk.StringVar(self)
        self.var_specialty.set('All')
        self.opt_specialty = tk.OptionMenu(
            self, self.var_specialty, *list(self.specialties.keys()),
            command=self.set_specialists
        )
        self.opt_specialty.grid(row=1, column=4, sticky='we')
        self.lbl_doctor = tk.Label(self, text='Doctor')
        self.lbl_doctor.grid(row=1, column=5, sticky='we')
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
        self.colour_schemes = [
            {'fg': 'black', 'bg': 'lightgrey'},
            {'fg': 'white', 'bg': 'grey'}
        ]
        self.get_schedule()
        self._configure_columns()
        self.bind('<Configure>', self.configure_scroll)
        self.cnv_appointment.bind('<Configure>', self.set_schedule_width)
        self.btn_return = tk.Button(
            self, text='Return', command=lambda: self.master.change_frame(0)
        )
        self.btn_return.grid(row=3, column=0, sticky='we')
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

    def get_doctors(self):
        doctors = self.master.db.find_employee(position='doctor')
        emp = self.master.db.get_columns('employee')
        doctors = [{col: val for col, val in zip(emp, doc)} for doc in doctors]
        return doctors

    def set_specialties(self):
        for doctor in self.get_doctors():
            specialty = doctor['specialty']
            name = doctor['first_name']
            all_list = self.specialties.get('All', [])
            all_list.append(name)
            self.specialties['All'] = all_list
            value = self.specialties.get(specialty, [])
            value.append(name)
            self.specialties[specialty] = value

    def configure_scroll(self, event=None):
        self.cnv_appointment.configure(
            scrollregion=self.cnv_appointment.bbox('all')
        )

    def set_specialists(self, event):
        specialty = self.var_specialty.get()
        self.var_doctor.set('')
        self.opt_doctor.destroy()
        doctors = self.specialties[specialty]
        self.opt_doctor = tk.OptionMenu(self, self.var_doctor, *doctors)
        self.opt_doctor.grid(row=1, column=6, sticky='we')

    def get_schedule(self):
        start_hour = 8
        end_hour = 16
        app_time = timedelta(minutes=30)
        date = self.ent_date.get()
        date = datetime.strptime(date, '%Y-%m-%d').replace(hour=start_hour)
        row = 0
        schemes = itertools.cycle(self.colour_schemes)
        while date.hour != end_hour:
            scheme = next(schemes)
            lbl_text = date.strftime('%H:%M')
            date += app_time
            lbl_hour = tk.Label(
                self.frm_hours, text=lbl_text, bg='grey'
            )
            lbl_hour.grid(row=row, column=0, sticky='we')
            lbl_hour.configure(**scheme)
            available_hour = tk.Label(
                self.frm_hours, bg='lightgrey', name=lbl_text
            )
            available_hour.configure(**scheme)
            available_hour.grid(row=row, column=1, sticky='we')
            available_hour.bind('<Double-Button-1>', self.schedule_appointment)
            row += 1

    def set_schedule_width(self, event):
        canvas_width = event.width
        self.cnv_appointment.itemconfig(self.cnv_frm, width=canvas_width)

    def schedule_appointment(self, event):
        date = self.ent_date.get()
        hour = str(event.widget).split('.')[-1]
        datetime = f'{date} {hour}'
        doc = self.var_doctor.get()
        spec = self.specialties[self.var_specialty.get()]
        db = self.master.db
        Appointment(self, datetime, doc, spec, db)
