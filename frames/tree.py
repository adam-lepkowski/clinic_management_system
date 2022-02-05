import tkinter as tk
from tkinter.ttk import Treeview


class Tree(Treeview):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columns = kwargs['columns']
        self.grid(row=0, column=0, sticky='nsew')
        self.scroll = tk.Scrollbar(self.master)
        self.scroll.grid(row=0, column=1, sticky='nsw')
        self.configure(yscrollcommand=self.scroll.set)
        self.scroll.configure(command=self.yview)
        self.config_columns()

    def config_columns(self):
        """
        Set tree columns headings and width.
        """

        for column in self.columns:
            width = self.master.winfo_width() // len(self.columns) // 3
            self.column(column, width=width)
            self.heading(column, text=column)
