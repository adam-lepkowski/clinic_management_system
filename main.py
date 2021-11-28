import tkinter as tk


class ClinicManagementSystem(tk.Tk):
    """
    Root window for ClinicManagementSystem GUI
    """
    def __init__(self):
        super().__init__()
        self.title("Clinic Management System")
        # set geometry and centre the window
        width = self.winfo_screenwidth() // 2
        height = self.winfo_screenheight() // 2
        self.geometry(f'{width}x{height}+{width // 2}+{height // 2}')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.frm_registration = tk.Frame(self)
        self.frm_registration.grid(row=0, column=1, sticky='nsew')
        self.frm_registration.columnconfigure(0, weight=1)
