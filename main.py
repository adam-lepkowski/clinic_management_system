import tkinter as tk


class ClinicManagementSystem(tk.Tk):
    """
    Root window for ClinicManagementSystem GUI
    """
    def __init__(self):
        super().__init__()
        self.title("Clinic Management System")
        # set geometry and centre the window
        width = self.winfo_screenwidth() // 2
        height = self.winfo_screenheight() // 2
        self.geometry(f'{width}x{height}+{width // 2}+{height // 2}')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.frm_registration = tk.Frame(self)
        self.frm_registration.grid(row=0, column=1, sticky='nsew')
        self.frm_registration.columnconfigure(0, weight=1)
        self.lbl_pat_details = tk.Label(
            self.frm_registration, text='Patient Details')
        self.lbl_pat_details.grid(row=0, column=0, sticky='we')
        self.lbl_f_name = tk.Label(self.frm_registration, text='First Name')
        self.lbl_f_name.grid(row=1, column=0, sticky='e')
        self.ent_f_name = tk.Entry(self.frm_registration)
        self.ent_f_name.grid(row=1, column=1, sticky='w')
        self.btn_register = tk.Button(self.frm_registration, text='Register')
        self.btn_register.grid(row=2, column=0)
