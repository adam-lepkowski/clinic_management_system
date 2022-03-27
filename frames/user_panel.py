import tkinter as tk
import tkinter.messagebox as msg

import bcrypt

from frames.const import APP_FRAMES_GRID, TITLE_SCRN


class UserPanel(tk.Frame):
    """
    Display user panel with possible actions
    """

    def __init__(self, master):
        super().__init__(master)
        self.lbl_curr_pwd = tk.Label(self, text='Current Password')
        self.lbl_curr_pwd.grid(row=0, column=0, sticky='e')
        self.ent_curr_pwd = tk.Entry(self, show='*')
        self.ent_curr_pwd.grid(row=0, column=1, sticky='w')
        self.lbl_new_pwd = tk.Label(self, text='New Password')
        self.lbl_new_pwd.grid(row=1, column=0, sticky='e')
        self.ent_new_pwd = tk.Entry(self, show='*')
        self.ent_new_pwd.grid(row=1, column=1, sticky='w')
        self.lbl_con_pwd = tk.Label(self, text='Confirm Password')
        self.lbl_con_pwd.grid(row=2, column=0, sticky='e')
        self.ent_con_pwd = tk.Entry(self, show='*')
        self.ent_con_pwd.grid(row=2, column=1, sticky='w')
        self.btn_update = tk.Button(
            self, text='Update Password', command=self.update_pwd
        )
        self.btn_update.grid(row=3, column=1, sticky='we')
        self.btn_return = tk.Button(
            self, text='Return',
            command=lambda:self.master.change_frame(TITLE_SCRN)
        )
        self.btn_return.grid(row=3, column=0, sticky='we')
        self.grid(**APP_FRAMES_GRID)

    def update_pwd(self):
        """
        Update current user's password
        """
        emp_id = self.master.current_user['id']
        current_pwd = self.ent_curr_pwd.get().encode('utf-8')
        current_hash = self.master.db.find('user', id=emp_id)[0][2]
        new_pwd = self.ent_new_pwd.get()
        new_pwd_con = self.ent_con_pwd.get()
        invalid_pwd = "Invalid password"
        if (new_pwd == new_pwd_con) and (new_pwd != ''):
            if bcrypt.checkpw(current_pwd, current_hash):
                self.master.db.update_pwd(emp_id, new_pwd)
                title = 'Password updated'
                msg.showinfo(title=title, message=title)
            else:
                message = 'Invalid current password'
                msg.showerror(title=invalid_pwd, message=message)
        else:
            message = "Passwords don't match or none provided"
            msg.showerror(title=invalid_pwd, message=message)
