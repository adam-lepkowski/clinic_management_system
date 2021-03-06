import tkinter as tk
import tkinter.messagebox as msg
from tkinter import filedialog as fd

import csv

from frames.const import APP_FRAMES_GRID, TITLE_SCRN
from frames import Tree


class AdminPanel(tk.Frame):
    """
    Represent admin panel to completely manage ClinicManagementSystem database.

    Parameters
    ---------------
    master
        tk parent container widget
    """

    def __init__(self, master):
        super().__init__(master)
        self.db = self.master.db
        # employee frame
        self.frm_emp = tk.Frame(self)
        self.frm_emp.grid(row=0, column=0, sticky='nsew')
        self.lbl_f_name = tk.Label(self.frm_emp, text='First Name')
        self.lbl_f_name.grid(row=0, column=0, sticky='e')
        self.ent_f_name = tk.Entry(self.frm_emp)
        self.ent_f_name.grid(row=0, column=1, sticky='we')
        self.lbl_m_name = tk.Label(self.frm_emp, text='Middle Name')
        self.lbl_m_name.grid(row=0, column=2, sticky='e')
        self.ent_m_name = tk.Entry(self.frm_emp)
        self.ent_m_name.grid(row=0, column=3, sticky='we')
        self.lbl_l_name = tk.Label(self.frm_emp, text='Last Name')
        self.lbl_l_name.grid(row=0, column=4, sticky='e')
        self.ent_l_name = tk.Entry(self.frm_emp)
        self.ent_l_name.grid(row=0, column=5, sticky='we')
        self.lbl_pos = tk.Label(self.frm_emp, text='Position')
        self.lbl_pos.grid(row=0, column=6, sticky='e')
        self.ent_pos = tk.Entry(self.frm_emp)
        self.ent_pos.grid(row=0, column=7, sticky='we')
        self.lbl_spec = tk.Label(self.frm_emp, text='Specialty')
        self.lbl_spec.grid(row=0, column=8, sticky='e')
        self.ent_spec = tk.Entry(self.frm_emp)
        self.ent_spec.grid(row=0, column=9, sticky='we')
        # common buttons
        self.frm_btn = tk.Frame(self)
        self.frm_btn.grid(row=1, column=0, sticky='nsew')
        self.btn_add_emp = tk.Button(
            self.frm_btn, text='Add Employee', command=self.add_employee
        )
        self.btn_add_emp.grid(row=0, column=0, sticky='we')
        self.btn_find_emp = tk.Button(
            self.frm_btn, text='Find Employee', command=self.find_employee)
        self.btn_find_emp.grid(row=0, column=1, sticky='we')
        self.btn_find_usr = tk.Button(
            self.frm_btn, text='Find User', command=self.find_user
        )
        self.btn_find_usr.grid(row=0, column=2)
        self.btn_add_multiple = tk.Button(
            self.frm_btn, text='Add multiple', command=self.add_multiple_popup
        )
        self.btn_add_multiple.grid(row=0, column=3, sticky='we')
        self.btn_return = tk.Button(
            self.frm_btn, text='Return',
            command=lambda: self.master.change_frame(TITLE_SCRN)
        )
        self.btn_return.grid(row=0, column=4, sticky='we')
        self.var_frame = tk.IntVar(self)
        self.btn_usr = tk.Radiobutton(
            self.frm_btn, text='Employee', variable=self.var_frame, value=0,
            command=self.change_panel
        )
        self.btn_usr.grid(row=0, column=5)
        self.btn_emp = tk.Radiobutton(
            self.frm_btn, text='User', variable=self.var_frame, value=1,
            command=self.change_panel
        )
        self.btn_emp.grid(row=0, column=6)
        # employee tree
        self.frm_emp_tree = tk.Frame(self)
        self.frm_emp_tree.grid(row=2, column=0, sticky='nsew')
        columns = self.db.get_columns('employee')
        self.emp_tree = Tree(
            self.frm_emp_tree, columns=columns, show='headings', name='emp_tree'
        )
        self.emp_tree.grid(row=0, column=0, sticky='nsew')
        self.emp_ent = {
            'first_name': self.ent_f_name,
            'middle_name': self.ent_m_name,
            'last_name': self.ent_l_name,
            'position': self.ent_pos,
            'specialty': self.ent_spec,
        }
        self.emp_menu = tk.Menu(self, tearoff=0)
        self.emp_menu.add_command(
            label='Create Account', command=lambda: self.pwd_popup('create')
        )
        self.emp_tree.bind('<Double-Button-1>', self.menu_popup)
        # user frame and tree
        self.frm_usr = tk.Frame(self)
        self.frm_usr.grid(row=0, column=0, sticky='nsew')
        self.lbl_usr_id = tk.Label(self.frm_usr, text='User ID')
        self.lbl_usr_id.grid(row=0, column=0, sticky='e')
        self.ent_usr_id = tk.Entry(self.frm_usr)
        self.ent_usr_id.grid(row=0, column=1, sticky='we')
        self.lbl_username = tk.Label(self.frm_usr, text='Username')
        self.lbl_username.grid(row=0, column=2, sticky='e')
        self.ent_username = tk.Entry(self.frm_usr)
        self.ent_username.grid(row=0, column=3, sticky='we')
        self.frm_usr_tree = tk.Frame(self)
        self.frm_usr_tree.grid(row=2, column=0, sticky='nsew')
        usr_columns = ['id', 'username']
        self.usr_tree = Tree(
            self.frm_usr_tree, columns=usr_columns, show='headings',
            name='usr_tree'
        )
        self.usr_tree.grid(row=0, column=0, sticky='nsew')
        self.usr_tree.bind('<Double-Button-1>', self.menu_popup)
        self.usr_menu = tk.Menu(self, tearoff=0)
        self.usr_menu.add_command(
            label='Delete User', command=self.delete_user
        )
        self.usr_menu.add_command(
            label='Update Password', command=lambda:self.pwd_popup('update')
        )
        self.configure_columns()
        self.change_panel()
        self.grid(APP_FRAMES_GRID)

    def configure_columns(self):
        """
        Set equal weight to frame columns
        """
        frames = [self, self.frm_emp, self.frm_usr]
        for frame in frames:
            columns, rows = frame.grid_size()
            for column in range(columns):
                frame.columnconfigure(column, weight=1)
        self.frm_emp_tree.columnconfigure(0, weight=1)
        self.frm_usr_tree.columnconfigure(0, weight=1)

    def change_panel(self):
        """
        Raise appropriate frames and and enable/disable widgets
        """

        option = self.var_frame.get()
        if option == 0:
            self.frm_emp.tkraise()
            self.frm_emp_tree.tkraise()
            self.btn_find_usr['state'] = 'disabled'
            self.btn_find_emp['state'] = 'normal'
            self.btn_add_emp['state'] = 'normal'
        else:
            self.frm_usr.tkraise()
            self.frm_usr_tree.tkraise()
            self.btn_find_usr['state'] = 'normal'
            self.btn_find_emp['state'] = 'disabled'
            self.btn_add_emp['state'] = 'disabled'

    def get_employee(self):
        """
        Get values from employee related entries
        """

        emp = {col: (val.get() if val.get() != '' else None)
               for col, val in self.emp_ent.items()}
        return emp

    def add_employee(self):
        """
        Add an employee to db
        """

        emp = self.get_employee()
        try:
            self.db.insert('employee', **emp)
            title = 'Registration successful'
            msg.showinfo(title=title, message='Employee added to db')
        except self.db.con.IntegrityError as e:
            title = 'Registration failed'
            msg.showerror(title=title, message=str(e))

    def find_employee(self):
        """
        Display employees meeting the search criteria in emp_tree
        """

        self.emp_tree.delete(*self.emp_tree.get_children())
        employee = self.get_employee()
        employee = {col: val for col, val in employee.items() if val is not None}
        employees = self.db.find(
            'employee', partial_match=True, **employee
        )
        for index, emp in enumerate(employees):
            self.emp_tree.insert(parent='', index=index, values=emp)

    def menu_popup(self, event):
        """
        Show popup menus when doubleclicked on a record in emp_tree or usr_tree
        """

        id_ = event.widget.focus()
        item = event.widget.item(id_)
        vals = item['values']
        menu = self.emp_menu if 'emp' in str(event.widget) else self.usr_menu
        if vals:
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

    def create_account(self):
        """
        Create an user account and set up an temporary password
        """

        id_ = self.emp_tree.focus()
        item = self.emp_tree.item(id_)
        emp_id = item['values'][0]
        pwd = self.frm_pwd.nametowidget('pwd').get()
        conf_pwd = self.frm_pwd.nametowidget('c_pwd').get()
        if (pwd == conf_pwd) and (pwd != ''):
            try:
                self.db.create_user_account(emp_id)
                username = self.db.find('user', id=emp_id)[0][1]
                self.db.update_pwd(emp_id, pwd)
                msg.showinfo(
                    title='Account created', message=f'Username: {username}'
                )
                self.frm_pwd.destroy()
            except self.db.con.IntegrityError as e:
                title = "Error occured"
                msg.showerror(title=title, message=e)
        else:
            msg.showerror('Invalid Password', 'Invalid password')

    def pwd_popup(self, action):
        """
        Set up or reset users password

        Parameters
        ---------------
        action : str
            str containg an action to be taken. should be "update" or "create"
        """

        self.frm_pwd = tk.Toplevel(self)
        lbl_title = tk.Label(self.frm_pwd, text='Set up a temporary password')
        lbl_title.grid(row=0, column=0, columnspan=2, sticky='we')
        lbl_pwd = tk.Label(self.frm_pwd, text='Password')
        lbl_pwd.grid(row=1, column=0, sticky='e')
        ent_pwd = tk.Entry(self.frm_pwd, show='*', name='pwd')
        ent_pwd.grid(row=1, column=1, sticky='w')
        lbl_pwd_confirm = tk.Label(self.frm_pwd, text='Confirm Password')
        lbl_pwd_confirm.grid(row=2, column=0, sticky='e')
        ent_pwd_confirm = tk.Entry(self.frm_pwd, show='*', name='c_pwd')
        ent_pwd_confirm.grid(row=2, column=1, sticky='w')
        if action == 'create':
            btn_register = tk.Button(
                self.frm_pwd, text='Create Account',
                command=self.create_account
            )
            btn_register.grid(row=3, column=1, sticky='we')
        if action == 'update':
            btn_update_pwd = tk.Button(
                self.frm_pwd, text='Update password', command=self.update_pwd
            )
            btn_update_pwd.grid(row=3, column=1, sticky='we')

    def update_pwd(self):
        """
        Update/reset a user's password
        """
        id_ = self.usr_tree.focus()
        item = self.usr_tree.item(id_)
        usr_id = item['values'][0]
        username = item['values'][1]
        pwd = self.frm_pwd.nametowidget('pwd').get()
        conf_pwd = self.frm_pwd.nametowidget('c_pwd').get()
        if (pwd == conf_pwd) and (pwd != ''):
            try:
                self.db.update_pwd(usr_id, pwd)
                message = f'Password for user: {username} updated'
                msg.showinfo(title='Password updated', message=message)
                self.frm_pwd.destroy()
            except self.db.con.IntegrityError as e:
                title = "Error occured"
                msg.showerror(title=title, message=e)
        else:
            msg.showerror('Invalid Password', 'Invalid password')

    def find_user(self):
        """
        Display users meeting the search criteria in usr_tree
        """

        self.usr_tree.delete(*self.usr_tree.get_children())
        id_ = self.ent_usr_id.get() if self.ent_usr_id.get() != '' else None
        username = self.ent_username.get() if self.ent_username.get() != '' else None
        if id_ and username:
            results = self.db.find(
                'user', id=id_, partial_match=True,username=username
            )
        elif id_:
            results = self.db.find('user', id=id_)
        else:
            results = self.db.find(
                'user', partial_match=True, username=username
            )
        for index, result in enumerate(results):
            self.usr_tree.insert(parent='', index=index, value=result[:-1])

    def delete_user(self):
        """
        Delete a single user from db
        """

        id_ = self.usr_tree.focus()
        item = self.usr_tree.item(id_)
        usr_id = item['values'][0]
        username = item['values'][1]
        title = f'Delete user {username}'
        message = f'Are you sure you want to delete user account: {username}?'
        if msg.askyesno(title=title, message=message):
            self.db.delete('user', id=usr_id)
            title = 'Account deleted'
            message = f'{username} account deleted'
            msg.showinfo(title=title, message=message)
            self.find_user()

    def add_multiple_popup(self):
        """
        Insert multiple rows to a chosen table from a csv file
        """

        frm = tk.Toplevel(self)
        swidth = frm.winfo_screenwidth() // 2
        sheight = frm.winfo_screenheight() // 2
        frm.geometry(f"+{swidth // 2}+{sheight // 2}")
        sql = "SELECT name FROM sqlite_master WHERE type='table'"
        tables = self.db.cur.execute(sql).fetchall()
        tables = [table[0] for table in tables]
        var = tk.StringVar(frm, value=tables[0])
        for index, table in enumerate(tables):
            tk.Radiobutton(
                frm, text=table, var=var, value=table
            ).grid(row=0, column=index)
        tk.Button(
            frm, text='Submit', command=lambda:self.select_file(var.get())
        ).grid(row=0, column=len(tables) + 1)

    def select_file(self, table):
        """
        Select a csv file containing table rows

        Parameters
        ---------------
        table : str
            name of the table to insert the values into
        """

        filetypes = (
            ('csv', '*.csv'),
            ('all files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Select a csv file containing db rows',
            filetypes=filetypes
        )
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            IntegrityError = self.db.con.IntegrityError
            OperationalError = self.db.con.OperationalError
            for row in reader:
                for key, value in row.items():
                    if value == '':
                        row[key] = None
                try:
                    self.db.insert(table, **row)
                except (IntegrityError, OperationalError) as e:
                    title = 'An error has occured'
                    message = f"Row:{row} raised an error {e}"
                    msg.showerror(title=title, message=message)
                    break
            else:
                title = 'Records added'
                message = 'Records added successfully'
                msg.showinfo(title=title, message=message)
