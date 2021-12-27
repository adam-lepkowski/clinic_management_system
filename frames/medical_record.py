import tkinter as tk

from frames import PatientDetailsFrame


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
        cols = self.db._get_columns_patient()
        self.patient = {col: value for col, value in zip(cols, patient)}
        self.frm_patient = PatientDetailsFrame(self, self.patient)
