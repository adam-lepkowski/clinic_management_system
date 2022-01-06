import tkinter as tk

from db import DB
from frames import Registration, TitleScreen, Search, Schedule


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
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.db = db
        self.frames = {
            0: TitleScreen(self),
            1: Registration(self),
            2: Search(self),
            3: Schedule(self)
        }
        self.frm_current = None
        self.change_frame(0)

    def change_frame(self, index):
        """
        Switch between frames specified in frames attribute

        Parameters
        ---------------
        index : int
            frame index
        """

        frame = self.frames[index]
        self.frm_current = frame
        frame.tkraise()
