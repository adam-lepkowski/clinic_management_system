import tkinter as tk
import tkinter.messagebox as msg
from sqlite3 import IntegrityError

from tkcalendar import DateEntry

from frames import PatientFrame


class Registration(PatientFrame):
    """
    Class used to represent patient registration frame and it's child widgets
    """

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.frm_buttons = tk.Frame(self)
        self.frm_buttons.grid(row=5, column=0, sticky='we')
        self.btn_register = tk.Button(
            self.frm_buttons, text='Register', command=self.register)
        self.btn_register.grid(row=0, column=0)
        self.btn_return = tk.Button(
            self.frm_buttons, text='Return',
            command=lambda: master.change_frame(0)
        )
        self.btn_return.grid(row=0, column=1)
        self.grid(row=0, column=1, sticky='nsew')

    def register(self):
        """
        Register patient in patient table. Callback to db.register_patient

        Appropriate messagebox pops up if provided with valid/invalid values.
        """
        patient_details = self.get_patient()
        try:
            self.master.db.register_patient(**patient_details)
            message = 'Patient registered successfully'
            msg.showinfo('Patient registered', message=message)
        except IntegrityError as error:
            message = str(error)
            msg.showerror('Patient not registered', message=message)
