import tkinter as tk
import tkinter.messagebox as msg
from datetime import datetime, timedelta
import itertools

from tkcalendar import DateEntry

from frames import Tree
from frames.const import TITLE_SCRN, APP_FRAMES_GRID


class ScheduleAppointment(tk.Toplevel):
    """
    Represent frame to schedule appoitnments in given datetime.

    Parameters
    ---------------
    master : container
        tk container object
    datetime : str
        datetime in %Y-%m-%d %H:%M format
    doctor : str
        doctor str in format "id: full_name"
    specialists : list
        list of doctors
    db
        database connection

    Attributes
    ---------------
    tree : Tree
        Treeview child object
    """

    def __init__(self, master, datetime, doctor, specialists, db):
        super().__init__(master)
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
        self.lbl_pat = tk.Label(self, text='Patient ID')
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
        columns = self.db.get_columns('app_v')
        self.tree = Tree(
            self.frm_scheduled, columns=columns, show='headings'
        )
        self.tree.bind('<Double-Button-1>', self.cancel_appointment)
        self.show_scheduled()
        self.configure_columns()

    def configure_columns(self):
        """
        Set equal weight to frame columns
        """

        columns, rows = self.grid_size()
        for column in range(columns):
            self.columnconfigure(column, weight=1)
        self.frm_scheduled.columnconfigure(0, weight=1)

    def confirm_appointment(self):
        """
        Add appointment to appointments table.
        """
        document = self.ent_pat.get()
        patient = self.db.find('patient', document_no=document)
        patient = patient[0] if patient else []
        doctor = self.var_spec.get()
        if patient and doctor:
            title = 'Appointment scheduled'
            message = 'Patient scheduled for an appointment'
            pat_id = patient[0]
            doc_id = doctor.split(':')[0]
            try:
                appointment = {
                    'patient_id': pat_id,
                    'app_datetime': self.app_datetime,
                    'doctor_id': doc_id
                }
                self.db.insert('appointment', **appointment)
                self.show_scheduled()
                msg.showinfo(title=title, message=message)
            except self.db.con.IntegrityError:
                message = 'Cannot schedule two appointments at the same time'
                msg.showerror(title='Too many appointments', message=message)
        elif not patient:
            msg.showinfo('Patient not found', 'Patient not found')
        elif not doctor:
            msg.showinfo('No doctor selected', 'Pick a doctor')

    def show_scheduled(self):
        """
        Populate Tree with appoitnments scheduled for dt from app_datetime.
        """

        self.tree.delete(*self.tree.get_children())
        appointments = self.db.find('app_v', app_datetime=self.app_datetime)
        if appointments:
            for i, appointment in enumerate(appointments):
                self.tree.insert(parent='', index=i, values=appointment)

    def cancel_appointment(self, event):
        """
        Cancel appointment selected in Tree and refresh appointment list.
        """

        id_ = event.widget.focus()
        item = event.widget.item(id_)
        appointment = item['values']
        # if header is clicked appointment will be empty
        if appointment:
            doc_name = appointment[3]
            doc_id = appointment[2]
            title = 'Cancel appointment'
            message = f"Are you sure you want to cancel {self.app_datetime}\
                        appointment with doctor {doc_name}"
            if msg.askyesno(title=title, message=message):
                del_params = {
                    'app_datetime': self.app_datetime,
                    'doctor_id': doc_id
                }
                self.db.delete('appointment', **del_params)
                self.show_scheduled()


class Schedule(tk.Frame):
    """
    Represent appointment schedule and doctor availability for given date.

    Parameters
    ---------------
    master : container
        tk container object

    Attributes
    ---------------
    colour_schemes : list
        list of dicts with label color schemes for appoitnments
    specialties : dictionary
        specialty: list of doctors of a given specialty
    """

    def __init__(self, master):
        super().__init__(master)
        self.lbl_title = tk.Label(self, text='Appointment Schedule')
        self.lbl_title.grid(
            row=0, column=0, sticky='nsew', pady=10, columnspan=7
        )
        self.btn_back = tk.Button(
            self, text='<', command=lambda: self.set_date('back')
        )
        self.btn_back.grid(row=1, column=0, sticky='e')
        self.btn_fwd = tk.Button(
            self, text='>', command=lambda: self.set_date('fwd')
        )
        self.btn_fwd.grid(row=1, column=2, sticky='w')
        self.ent_date = DateEntry(self, date_pattern='y-mm-dd')
        self.ent_date.grid(row=1, column=1, sticky='we')
        if self.master.db.find('employee', position='doctor'):
            self.specialties = {}
            self.set_specialties()
            self.lbl_specialty = tk.Label(self, text='Specialty')
            self.lbl_specialty.grid(row=1, column=3, sticky='we')
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
            self.cnv_appointment.grid(
                row=2, column=0, columnspan=7, sticky='nsew'
            )
            self.frm_hours = tk.Frame(self.cnv_appointment)
            self.cnv_frm = self.cnv_appointment.create_window(
                (0, 0), anchor=tk.NW, window=self.frm_hours)
            self.scr_cnv = tk.Scrollbar(
                self, command=self.cnv_appointment.yview
            )
            self.scr_cnv.grid(row=2, column=7, sticky='wns')
            self.cnv_appointment.configure(yscrollcommand=self.scr_cnv.set)
            self.colour_schemes = [
                {'fg': 'black', 'bg': 'lightgrey'},
                {'fg': 'white', 'bg': 'grey'}
            ]
            self.get_schedule()
            self.configure_columns()
            self.bind('<Configure>', self.configure_scroll)
            self.cnv_appointment.bind('<Configure>', self.set_schedule_width)
        self.btn_return = tk.Button(
            self, text='Return',
            command=lambda: self.master.change_frame(TITLE_SCRN)
        )
        self.btn_return.grid(row=3, column=0, sticky='we')
        self.set_current_doctor()
        self.grid(**APP_FRAMES_GRID)

    def configure_columns(self):
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
        """
        Get doctors from employee table.

        Returns
        ---------------
        doctors : dict
            dictionary containing doctor details column_name: value
        """

        doctors = self.master.db.find('employee', position='doctor')
        emp = self.master.db.get_columns('employee')
        doctors = [{col: val for col, val in zip(emp, doc)} for doc in doctors]
        return doctors

    def set_specialties(self):
        """
        Populate self.specialties with spec: list of doctors of given specialty
        """

        for doc in self.get_doctors():
            specialty = doc['specialty']
            if doc['middle_name']:
                full = f"{doc['first_name']} {doc['middle_name']} {doc['last_name']}"
            else:
                full = f"{doc['first_name']} {doc['last_name']}"
            name = f"{doc['id']}: {full}"
            all_list = self.specialties.get('All', [])
            all_list.append(name)
            self.specialties['All'] = all_list
            value = self.specialties.get(specialty, [])
            value.append(name)
            self.specialties[specialty] = value

    def configure_scroll(self, event=None):
        """
        Configure canvas scrollregion.
        """

        self.cnv_appointment.configure(
            scrollregion=self.cnv_appointment.bbox('all')
        )

    def set_specialists(self, event):
        """
        Place OptionMenu with doctors of selected specialty.
        """

        specialty = self.var_specialty.get()
        self.var_doctor.set('')
        self.opt_doctor.destroy()
        doctors = self.specialties[specialty]
        self.opt_doctor = tk.OptionMenu(self, self.var_doctor, *doctors)
        self.opt_doctor.grid(row=1, column=6, sticky='we')

    def get_schedule(self):
        """
        Populate cnv_appointment with labels representing appointment datetimes
        """

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
        """
        Set cnv_frm width equal to cnv_appointment width.
        """

        canvas_width = event.width
        self.cnv_appointment.itemconfig(self.cnv_frm, width=canvas_width)

    def set_date(self, direction):
        """
        Change viewed schedule datetime by 1 forward or backward.
        """

        delta = timedelta(days=1)
        date = self.ent_date.get()
        if direction == 'fwd':
            date = datetime.strptime(date, '%Y-%m-%d') + delta
        else:
            date = datetime.strptime(date, '%Y-%m-%d') - delta
        self.ent_date.set_date(date)

    def schedule_appointment(self, event):
        """
        Instatiate ScheduleAppointment class to set up an appointment.
        """

        date = self.ent_date.get()
        hour = str(event.widget).split('.')[-1]
        datetime = f'{date} {hour}'
        doc = self.var_doctor.get()
        spec = self.specialties[self.var_specialty.get()]
        db = self.master.db
        ScheduleAppointment(self, datetime, doc, spec, db)

    def set_current_doctor(self):
        """
        Lock current user's schedule if position == doctor.
        """

        if self.master.current_user['position'] == 'doctor':
            specialty = self.master.current_user['specialty']
            doc_id = str(self.master.current_user['id'])
            for doctor in self.specialties[specialty]:
                if doctor.startswith(doc_id):
                    self.var_doctor.set(doctor)
                    self.var_specialty.set(specialty)
                    self.opt_doctor.configure(state='disabled')
                    self.opt_specialty.configure(state='disabled')
                    break

    def get_appointment(self, doc_id, app_datetime):
        """
        Get scheduled appointment

        Parameters
        ---------------
        doc_id : int or str
            doctor's id
        app_datetime : datetime or str
            datetime in format YYYY-MM-DD HH:MM

        Returns
        ---------------
        dictionary
        OR
        empty list
        """

        columns = self.master.db.get_columns('appointment')
        appointment = self.master.db.find(
            'appointment', doctor_id=doc_id, app_datetime=app_datetime
        )
        if appointment:
            appointment = {
                col: val for col, val in zip(columns, appointment[0])
            }
        return appointment
