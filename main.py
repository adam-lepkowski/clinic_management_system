import tkinter as tk

from db import DB
from frames import RegistrationFrame, TitleScreen, SearchFrame


class ClinicManagementSystem(tk.Tk):
    """
    Root window for ClinicManagementSystem GUI
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
        self.frames = {
            0: TitleScreen(self),
            1: RegistrationFrame(self),
            2: SearchFrame(self)
        }
        self.db = db
        self.frm_current = None
        self.change_frame(0)

    def change_frame(self, index):
        frame = self.frames[index]
        self.frm_current = frame
        frame.tkraise()
