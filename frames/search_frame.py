import tkinter as tk
import tkinter.messagebox as msg
from tkinter.ttk import Treeview


class SearchFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.lbl_title = tk.Label(self, text='Find Patients')
        self.lbl_title.grid(
            row=0, column=0, sticky='we', columnspan=6, pady=10)
        self.lbl_f_name = tk.Label(self, text='First Name')
        self.lbl_f_name.grid(row=1, column=0, sticky='e')
        self.ent_f_name = tk.Entry(self)
        self.ent_f_name.grid(row=1, column=1, sticky='we')
        self.lbl_l_name = tk.Label(self, text='Last Name')
        self.lbl_l_name.grid(row=1, column=2, sticky='e')
        self.ent_l_name = tk.Entry(self)
        self.ent_l_name.grid(row=1, column=3, sticky='we')
        self.lbl_document = tk.Label(self, text='Document')
        self.lbl_document.grid(row=1, column=4, sticky='e')
        self.ent_document = tk.Entry(self)
        self.ent_document.grid(row=1, column=5, sticky='we')
        self.frm_buttons = tk.Frame(self)
        self.frm_buttons.grid(row=2, column=0, sticky='we', columnspan=6)
        self.btn_find = tk.Button(self.frm_buttons, text='Find',
            command=self.find_patient)
        self.btn_find.grid(row=0, column=0)
        self.btn_return = tk.Button(
            self.frm_buttons, text='Return',
            command=lambda: master.change_frame(0)
        )
        self.btn_return.grid(row=0, column=1)
        self.frm_results = tk.Frame(self)
        self.frm_results.grid(row=3, column=0, sticky='nsew', columnspan=6)
        self.columns = self.master.db._get_columns_patient()
        self.tree = Treeview(
            self.frm_results, columns=self.columns, show='headings')
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree_scroll = tk.Scrollbar(self.frm_results)
        self.tree_scroll.grid(row=0, column=1, sticky='nsw')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.configure(command=self.tree.yview)
        self.tree.bind('<Double-Button-1>', self.view_patient)
        self._config_tree_columns()
        self.grid(row=0, column=1, sticky='nsew')
        self._configure_columns()
        self.search_ent = {
            'first_name': self.ent_f_name,
            'last_name': self.ent_l_name,
            'document_no': self.ent_document
        }

    def _configure_columns(self):
        columns, rows = self.grid_size()
        for column in range(columns):
            self.columnconfigure(column, weight=1)
        self.frm_results.columnconfigure(0, weight=1)

    def _config_tree_columns(self):
        for column in self.columns:
            width = self.master.winfo_width() // len(self.columns) // 3
            self.tree.column(column, width=width)
            self.tree.heading(column, text=column)

    def get_search_cond(self):
        search_conditions = {}
        for column, widget in self.search_ent.items():
            if widget.get() == '':
                continue
            search_conditions[column] = widget.get()
        return search_conditions

    def find_patient(self):
        self.tree.delete(*self.tree.get_children())
        search_conditions = self.get_search_cond()
        results = self.master.db.find_patient(**search_conditions)
        if results:
            for index, result in enumerate(results):
                self.tree.insert(parent='', index=index, values=result)
        else:
            message = 'No patients matching the search criteria'
            msg.showinfo(title='Search Results', message=message)

    def view_patient(self, event):
        id_ = event.widget.focus()
        item = event.widget.item(id_)
        values = item['values']
        if values:
            msg.showinfo(title='Placeholder', message=values)
