import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg

from tkcalendar import DateEntry

from frames import PatientFrame, Tree


class PatientDetails(PatientFrame):
    """
    Represent and edit single patient details.

    Parameters
    ---------------
    master
        tk parent container widget
    patient: dict
        dictionary containing patient details
    """

    def __init__(self, master, patient, db):
        super().__init__(master)
        self.patient = patient
        self.db = db
        self.frm_buttons = tk.Frame(self)
        col, row = self.grid_size()
        self.frm_buttons.grid(row=row + 1, column=0, sticky='nsew')
        self.btn_submit = tk.Button(
            self.frm_buttons, text='Submit', command=self.submit
        )
        self.btn_submit.grid(row=0, column=0)
        self.btn_edit = tk.Button(
            self.frm_buttons, text='Edit', command=self.edit
        )
        self.btn_edit.grid(row=0, column=1)
        self.btn_cancel = tk.Button(
            self.frm_buttons, text='Cancel', command=self.set_default)
        self.btn_cancel.grid(row=0, column=2)
        self.set_default()
        self.grid(row=0, column=0, sticky='nsew')

    def edit(self):
        """
        Enable patient details edition.
        """

        self.set_state('normal')
        self.btn_submit.config(state='normal')
        self.btn_edit.config(state='disabled')
        self.btn_cancel.config(state='normal')

    def submit(self):
        """
        Submit changes to patient table.
        """

        edited_patient = self.get_patient()
        updated_values = {col: val for col, val in edited_patient.items()
                          if str(self.patient.get(col, None)) != str(val)}
        try:
            self.db.update(
                'patient', id_=self.patient['id'], **updated_values
            )
            self.patient.update(updated_values)
            self.set_default()
            message = 'Patient updated successfully'
            msg.showinfo(title='Updated', message=message)
        except self.db.con.IntegrityError as error:
            message = str(error)
            msg.showerror(title='Update failed', message=message)

    def set_default(self):
        """
        Set default state to child widgets and populate entries with values.
        """

        self.set_values(self.patient)
        self.set_state('disabled')
        self.btn_submit.config(state='disabled')
        self.btn_edit.config(state='normal')
        self.btn_cancel.config(state='disabled')

    def set_state(self, state):
        """
        Set chosen state to Entry and OptionMenu widgets.

        Parameters
        ---------------
        state: str
            state to be set to widgets. Available states: 'normal', 'disabled'
        """

        for widget in self.winfo_children():
            if isinstance(widget, tk.OptionMenu):
                widget.config(state=state)
        for widget in self.patient_ent.values():
            if not isinstance(widget, tk.StringVar):
                widget.config(state=state)

    def set_values(self, patient):
        """
        Set Entry and StringVar values to chosen patient details.

        Clear entries and populate them with new values.

        Parameters
        ---------------
        patient: dict
            dictionary containing patient table column: value to be set
        """

        for col, value in self.patient.items():
            widget = self.patient_ent.get(col, None)
            if isinstance(widget, DateEntry):
                widget.set_date(value)
            elif isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                    widget.insert(0, value)
            elif isinstance(widget, tk.StringVar):
                widget.set(value)


class AppointmentHistory(tk.Frame):
    """
    Represent a frame to hold patients appointment history in a TreeView.

    Parameters
    ---------------
    master
        tk container object
    db
        database connection
    patient: dict
        dictionary containing patient details
    """

    def __init__(self, master, patient, db):
        super().__init__(master)
        self.patient = patient
        self.db = db
        columns = self.db.get_columns('app_v')
        self.tree = Tree(self, columns=columns, show='headings')
        self.get_appointments()
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky='nsew')

    def get_appointments(self):
        """
        Populate Tree with patient appoitnments.
        """

        patient_id = self.patient['id']
        appointments = self.db.find('app_v', patient_id=patient_id)
        if appointments:
            for i, appointment in enumerate(appointments):
                self.tree.insert(parent='', index=i, values=appointment)


class MedicalRecord(tk.Toplevel):
    """
    Display patient medical record.

    Parameters
    ---------------
    master
        tk parent container widget
    patient: dict
        dictionary containing patient details
    """

    def __init__(self, master, patient):
        super().__init__(master)
        self.master = master
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        self.geometry(f'{width}x{height}')
        self.db = self.master.db
        cols = self.db.get_columns('patient')
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=1, sticky='nsew')
        self.patient = {col: value for col, value in zip(cols, patient)}
        self.frm_patient = PatientDetails(self.notebook, self.patient, self.db)
        self.frm_history = AppointmentHistory(
            self.notebook, self.patient, self.db
        )
        self.notebook.add(self.frm_patient, text='Patient Details')
        self.notebook.add(self.frm_history, text='Appointment History')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
