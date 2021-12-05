import tkinter as tk

from tkcalendar import DateEntry


class RegistrationFrame(tk.Frame):
    """
    Class used to represent patient registration frame and it's child widgets
    """

    def __init__(self, master):
        super().__init__(master)
        self.lbl_pat_details = tk.Label(self, text='Patient Details')
        self.lbl_pat_details.grid(row=0, column=0, sticky='we', columnspan=6)
        self.lbl_f_name = tk.Label(self, text='First Name')
        self.lbl_f_name.grid(row=1, column=0, sticky='e')
        self.ent_f_name = tk.Entry(self)
        self.ent_f_name.grid(row=1, column=1, sticky='we')
        self.lbl_m_name = tk.Label(self, text='Middle Name')
        self.lbl_m_name.grid(row=1, column=2, sticky='e')
        self.ent_m_name = tk.Entry(self)
        self.ent_m_name.grid(row=1, column=3, sticky='we')
        self.lbl_l_name = tk.Label(self, text='Last Name')
        self.lbl_l_name.grid(row=1, column=4, sticky='e')
        self.ent_l_name = tk.Entry(self)
        self.ent_l_name.grid(row=1, column=5, sticky='we')
        self.lbl_dob = tk.Label(self, text='Date Of Birth')
        self.lbl_dob.grid(row=2, column=0, sticky='e')
        self.ent_dob = DateEntry(self, date_pattern='y-mm-dd')
        self.ent_dob.grid(row=2, column=1, sticky='we')
        self.lbl_gender = tk.Label(self, text='Gender')
        self.lbl_gender.grid(row=2, column=2, sticky='e')
        genders = ['', 'Male', 'Female']
        self.var_gender = tk.StringVar(self)
        self.opt_gender = tk.OptionMenu(self, self.var_gender, *genders)
        self.opt_gender.grid(row=2, column=3, sticky='we')
        self.lbl_marital = tk.Label(self, text='Marital Status')
        self.lbl_marital.grid(row=2, column=4, sticky='e')
        maritals = [
            '', 'Single', 'Married', 'Widowed', 'Divorced', 'Separated'
        ]
        self.var_marital = tk.StringVar(self)
        self.opt_marital = tk.OptionMenu(self, self.var_marital, *maritals)
        self.opt_marital.grid(row=2, column=5, sticky='we')
        self.lbl_nation = tk.Label(self, text='Nationality')
        self.lbl_nation.grid(row=3, column=0, sticky='e')
        self.ent_nation = tk.Entry(self)
        self.ent_nation.grid(row=3, column=1, sticky='we')
        self.lbl_email = tk.Label(self, text='Email')
        self.lbl_email.grid(row=3, column=2, sticky='e')
        self.ent_email = tk.Entry(self)
        self.ent_email.grid(row=3, column=3, sticky='we')
        self.btn_register = tk.Button(self, text='Register')
        self.btn_register.grid(row=4, column=0)
        self._configure_columns()
        self.patient_ent = {
            'first_name': self.ent_f_name,
            'middle_name': self.ent_m_name,
            'last_name': self.ent_l_name,
            'date_of_birth': self.ent_dob,
            'gender': self.var_gender,
            'marital_status': self.var_marital,
            'nationality': self.ent_nation,
            'email': self.ent_email
        }

    def _configure_columns(self):
        columns, rows = self.grid_size()
        for column in range(columns):
            self.columnconfigure(column, weight=1)

    def get_patient(self):
        patient_details = {}
        for col_name, widget in self.patient_ent.items():
            patient_details[col_name] = widget.get()
        return patient_details
