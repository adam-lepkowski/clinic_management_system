import tkinter as tk

from db import DB
from frames import (Registration, TitleScreen, Search, Schedule,
                    FirstLaunchScreen, Login)
from frames.const import TITLE_SCRN, REGISTRATION, SEARCH, SCHEDULE


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
            TITLE_SCRN: TitleScreen(self),
            REGISTRATION: Registration(self),
            SEARCH: Search(self),
            SCHEDULE: Schedule(self)
        }
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.change_frame(0)
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

    def set_login_screen(self):
        user = self.db.find('employee', position='admin')
        if user:
            Login(self, self.db)
        else:
            FirstLaunchScreen(self, self.db)
