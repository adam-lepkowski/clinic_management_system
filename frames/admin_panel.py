import tkinter as tk
from tkinter.ttk import Notebook
import tkinter.messagebox as msg

from frames.const import APP_FRAMES_GRID
from frames import Tree


class Employee(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.lbl_f_name = tk.Label(self, text='First Name')
        self.lbl_f_name.grid(row=0, column=0, sticky='e')
        self.ent_f_name = tk.Entry(self)
        self.ent_f_name.grid(row=0, column=1, sticky='we')
        self.lbl_m_name = tk.Label(self, text='Middle Name')
        self.lbl_m_name.grid(row=0, column=2, sticky='e')
        self.ent_m_name = tk.Entry(self)
        self.ent_m_name.grid(row=0, column=3, sticky='we')
        self.lbl_l_name = tk.Label(self, text='Last Name')
        self.lbl_l_name.grid(row=0, column=4, sticky='e')
        self.ent_l_name = tk.Entry(self)
        self.ent_l_name.grid(row=0, column=5, sticky='we')
        self.lbl_pos = tk.Label(self, text='Position')
        self.lbl_pos.grid(row=0, column=6, sticky='e')
        self.ent_pos = tk.Entry(self)
        self.ent_pos.grid(row=0, column=7, sticky='we')
        self.lbl_spec = tk.Label(self, text='Specialty')
        self.lbl_spec.grid(row=0, column=8, sticky='e')
        self.ent_spec = tk.Entry(self)
        self.ent_spec.grid(row=0, column=9, sticky='we')
        self.btn_add_emp = tk.Button(
            self, text='Add Employee', command=self.add_employee
        )
        self.btn_add_emp.grid(row=1, column=0, sticky='w')
        self.btn_find_emp = tk.Button(
            self, text='Find Employee', command=self.find_employee)
        self.btn_find_emp.grid(row=1, column=1, sticky='w')
        self.frm_tree = tk.Frame(self)
        self.frm_tree.grid(row=2, column=0, columnspan=10, sticky='nsew')
        columns = self.master.db.get_columns('employee')
        self.tree = Tree(self.frm_tree, columns=columns, show='headings')
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.emp_ent = {
            'first_name': self.ent_f_name,
            'middle_name': self.ent_m_name,
            'last_name': self.ent_l_name,
            'position': self.ent_pos,
            'specialty': self.ent_spec,
        }
        self.acc_menu = tk.Menu(self, tearoff=0)
        self.acc_menu.add_command(label='Create Account')
        self.tree.bind('<Double-Button-1>', self.menu_popup)
        self.configure_columns()

    def configure_columns(self):
        """
        Set equal weight to frame columns
        """

        columns, rows = self.grid_size()
        for column in range(columns):
            self.columnconfigure(column, weight=1)
        self.frm_tree.columnconfigure(0, weight=1)

    def get_employee(self):
        emp = {col: (val.get() if val.get() != '' else None)
               for col, val in self.emp_ent.items()}
        return emp

    def add_employee(self):
        emp = self.get_employee()
        try:
            self.master.db.insert('employee', **emp)
            title = 'Registration successful'
            msg.showinfo(title=title, message='Employee added to db')
        except self.master.db.con.IntegrityError as e:
            title = 'Registration failed'
            msg.showerror(title=title, message=str(e))

    def find_employee(self):
        self.tree.delete(*self.tree.get_children())
        employee = self.get_employee()
        employee = {col: val for col, val in employee.items() if val is not None}
        employees = self.master.db.find(
            'employee', partial_match=True, **employee
        )
        for index, emp in enumerate(employees):
            self.tree.insert(parent='', index=index, values=emp)

    def menu_popup(self, event):
        id_ = event.widget.focus()
        item = event.widget.item(id_)
        vals = item['values']
        if vals:
            try:
                self.acc_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.acc_menu.grab_release()

class AdminPanel(Notebook):

    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.frm_emp = Employee(self)
        self.frm_create_usr = tk.Frame(self)
        self.add(self.frm_emp, text='Add Employee')
        self.add(self.frm_create_usr, text='Create User Account')
        self.grid(APP_FRAMES_GRID)
