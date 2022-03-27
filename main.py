import tkinter as tk

from db import DB
from frames import (Registration, TitleScreen, Search, Schedule,
                    FirstLaunchScreen, Login, AdminPanel, UserPanel)
from frames.const import (TITLE_SCRN, REGISTRATION, SEARCH, SCHEDULE, ADMIN,
                          USER, ADMIN_TITLE_SCREEN, DOCTOR_TITLE_SCREEN,
                          REGISTRATION_TITLE_SCREEN)


class ClinicManagementSystem(tk.Tk):
    """
    Root window for ClinicManagementSystem GUI

    Set up main frame, initialize child frames and configure app layout

    Parameters
    ---------------
    db : connection to database

    Attributes
    ---------------
    frames : dict
        a dictionary of frames in format index : frame
    db : database
        object representing a database connection
    """

    def __init__(self, db):
        super().__init__()
        self.title("Clinic Management System")
        # set geometry and centre the window
        width = self.winfo_screenwidth() // 2
        height = self.winfo_screenheight() // 2
        self.geometry(f'{width}x{height}+{width // 2}+{height // 2}')
        self.db = db
        self.frames = {
            TITLE_SCRN: TitleScreen,
            REGISTRATION: Registration,
            SEARCH: Search,
            SCHEDULE: Schedule,
            ADMIN: AdminPanel,
            USER: UserPanel
        }
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.current_user = None
        self.set_login_screen()

    def change_frame(self, index):
        """
        Switch between frames specified in frames attribute

        Parameters
        ---------------
        index : int
            frame index
        """

        frame = self.frames[index]
        frame.tkraise()

    def set_title_screen(self):
        """
        Set up a title screen. Available screens dependent on current_user's
        position
        """

        self.frames[TITLE_SCRN] = self.frames[TITLE_SCRN](self)
        if self.current_user['position'] == 'admin':
            screen = ADMIN_TITLE_SCREEN
        elif self.current_user['position'] == 'doctor':
            screen = DOCTOR_TITLE_SCREEN
        else:
            screen = REGISTRATION_TITLE_SCREEN
        for screen_idx in screen:
            self.frames[screen_idx] = self.frames[screen_idx](self)
        self.change_frame(TITLE_SCRN)

    def set_login_screen(self):
        """
        Display. If there is no admin (first launch). Display FirstLaunchScreen
        """
        
        user = self.db.find('employee', position='admin')
        if user:
            Login(self, self.db)
        else:
            FirstLaunchScreen(self, self.db)
