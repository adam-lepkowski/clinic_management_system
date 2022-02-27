import tkinter as tk
import tkinter.messagebox as msg

import bcrypt

from frames.const import APP_FRAMES_GRID


class FirstLaunchScreen(tk.Frame):

    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.lbl_title = tk.Label(self, text='Set Up An Administrator Account')
        self.lbl_title.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.lbl_f_name = tk.Label(self, text='First Name')
        self.lbl_f_name.grid(row=1, column=0, sticky='e')
        self.ent_f_name = tk.Entry(self)
        self.ent_f_name.grid(row=1, column=1, sticky='w')
        self.lbl_m_name = tk.Label(self, text='Middle Name')
        self.lbl_m_name.grid(row=2, column=0, sticky='e')
        self.ent_m_name = tk.Entry(self)
        self.ent_m_name.grid(row=2, column=1, sticky='w')
        self.lbl_l_name = tk.Label(self, text='Last Name')
        self.lbl_l_name.grid(row=3, column=0, sticky='e')
        self.ent_l_name = tk.Entry(self)
        self.ent_l_name.grid(row=3, column=1, sticky='w')
        self.lbl_pwd = tk.Label(self, text='Password')
        self.lbl_pwd.grid(row=4, column=0, sticky='e')
        self.ent_pwd = tk.Entry(self, show='*')
        self.ent_pwd.grid(row=4, column=1, sticky='w')
        self.lbl_pwd_confirm = tk.Label(self, text='Confirm Password')
        self.lbl_pwd_confirm.grid(row=5, column=0, sticky='e')
        self.ent_pwd_confirm = tk.Entry(self, show='*')
        self.ent_pwd_confirm.grid(row=5, column=1, sticky='w')
        self.btn_register = tk.Button(
            self, text='Register', command=self.register
        )
        self.btn_register.grid(row=6, column=1, sticky='w')
        self.configure_columns()
        self.grid(APP_FRAMES_GRID)

    def configure_columns(self):
        """
        Set equal weight to frame columns
        """
        columns, rows = self.grid_size()
        for column in range(columns):
            self.columnconfigure(column, weight=1)

    def register(self):
        fname = self.ent_f_name.get()
        mname = self.ent_m_name.get() if self.ent_m_name.get() != '' else None
        lname = self.ent_l_name.get()
        pwd = self.ent_pwd.get()
        conf_pwd = self.ent_pwd_confirm.get()

        if pwd == conf_pwd:
            try:
                employee = {
                    'first_name': fname,
                    'middle_name': mname,
                    'last_name': lname,
                    'position': 'admin',
                    'specialty': None
                }
                self.db.insert('employee', **employee)
                self.db.create_user_account(1)
                self.db.update_pwd(1, pwd)
                username = f'{fname}.{lname}'
                message = f'Account created successfully. Username: {username}'
                title = 'Account created'
                self.master.set_login_screen()
            except self.db.con.IntegrityError as e:
                title = 'Account not created'
                message = 'Invalid user details'
        else:
            title = "Invalid password"
            message = "Passwords don't match"
        msg.showinfo(title=title, message=message)


class Login(tk.Frame):

    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.lbl_title = tk.Label(self, text='Sign in')
        self.lbl_title.grid(row=0, column=0, columnspan=2, sticky='we')
        self.lbl_usrname = tk.Label(self, text='Username')
        self.lbl_usrname.grid(row=1, column=0, sticky='e')
        self.ent_usrname = tk.Entry(self)
        self.ent_usrname.grid(row=1, column=1, sticky='w')
        self.lbl_pwd = tk.Label(self, text='Password')
        self.lbl_pwd.grid(row=2, column=0, sticky='e')
        self.ent_pwd = tk.Entry(self)
        self.ent_pwd.grid(row=2, column=1, sticky='w')
        self.btn_login = tk.Button(self, text='Sign in', command=self.login)
        self.btn_login.grid(row=3, column=0, columnspan=2)
        self.configure_columns()
        self.grid(APP_FRAMES_GRID)

    def configure_columns(self):
        """
        Set equal weight to frame columns
        """
        columns, rows = self.grid_size()
        for column in range(columns):
            self.columnconfigure(column, weight=1)

    def login(self):
        username = self.ent_usrname.get()
        pwd = self.ent_pwd.get().encode('utf-8')
        match = self.db.find('user', username=username)
        if match:
            id_, user, hash_pw = match[0]
            if bcrypt.checkpw(pwd, hash_pw):
                self.master.set_title_screen()
                self.destroy()
        else:
            msg.showerror(title='Login failed', message='Invalid credentials')
