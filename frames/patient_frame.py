import tkinter as tk

from tkcalendar import DateEntry


class PatientFrame(tk.Frame):
    """
    Represent patient table columns with widgets.

    Attributes
    ---------------
    patient_ent : dict
        represent column_name: Entry/StringVar to extract entered values

    Methods
    ---------------
    configure_columns
    get_patient
    """

    def __init__(self, master):
        super().__init__(master)
        self.lbl_pat_details = tk.Label(self, text='Patient Details')
        self.lbl_pat_details.grid(
            row=0, column=0, sticky='we', columnspan=6, pady=10)
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
        self.lbl_phone = tk.Label(self, text='Phone')
        self.lbl_phone.grid(row=3, column=4, sticky='e')
        self.ent_phone = tk.Entry(self)
        self.ent_phone.grid(row=3, column=5, sticky='we')
        self.lbl_document = tk.Label(self, text='Document')
        self.lbl_document.grid(row=4, column=0, sticky='e')
        self.ent_document = tk.Entry(self)
        self.ent_document.grid(row=4, column=1, sticky='we')
        self.configure_columns()
        self.patient_ent = {
            'first_name': self.ent_f_name,
            'middle_name': self.ent_m_name,
            'last_name': self.ent_l_name,
            'date_of_birth': self.ent_dob,
            'gender': self.var_gender,
            'marital_status': self.var_marital,
            'nationality': self.ent_nation,
            'email': self.ent_email,
            'phone': self.ent_phone,
            'document_no': self.ent_document
        }

    def configure_columns(self):
        """
        Set equal weight to frame columns
        """
        columns, rows = self.grid_size()
        for column in range(columns):
            self.columnconfigure(column, weight=1)

    def get_patient(self):
        """
        Gets values entered by user. If value is '' replace with None.

        Returns
        ---------------
        dictionary
            patient column name: value
        """

        patient_details = {col: (val.get() if val.get() != '' else None)
                           for col, val in self.patient_ent.items()}
        return patient_details
