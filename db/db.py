import sqlite3

from db.db_const import *


class DB:
    """
    Class used to represent a connection to sqlite3 database

    Initialize tables and triggers if they don't already exist in the db

    Parameters
    ---------------
    db : str
        path to sqlite3 database file
    """

    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute(CREATE_TABLE_PATIENT)
        self.cur.execute(CREATE_TRIGGER_DOB)
        self.cur.execute(CREATE_TRIGGER_GENDER)
        self.cur.execute(CREATE_TRIGGER_MARITAL)
        self.cur.execute(CREATE_TRIGGER_EMAIL)
        self.cur.execute(CREATE_TRIGGER_PHONE)
        self.cur.execute(CREATE_TABLE_APPOINTMENT)
        self.cur.execute(CREATE_TRIGGER_APP_DATE)
        self.cur.execute(CREATE_TABLE_EMPLOYEE)
        self.cur.execute(CREATE_VIEW_APPOINTMENT)
        self.cur.execute('PRAGMA foreign_keys=on')
        self.cur.connection.commit()

    def get_columns(self, table):
        """
        Get column headers from given table

        Returns
        ---------------
        list
            a list of column headers
        """
        sql_tables = """SELECT name FROM sqlite_master WHERE type in ('table', 'view')"""
        tables =  self.cur.execute(sql_tables).fetchall()
        tables = [table[0] for table in tables]
        if table in tables:
            sql = f"PRAGMA table_info('{table}')"
            columns = self.cur.execute(sql).fetchall()
            column_names = [column[1] for column in columns]
            return column_names
        return None

    def register_patient(self, **kwargs):
        """
        Insert patient into patient table

        Values should be provided in format column_field=value, if column_field
        does not exist in table patient it is omitted.

        Parameters
        ---------------
        **kwargs
            table_field: value
        """

        columns = self.get_columns('patient')
        patient = {column: value for column, value in kwargs.items()
                   if column in columns}
        columns = ''
        placeholders = ''
        values = []
        for column, value in patient.items():
            columns += f'{column}, '
            placeholders += '?, '
            values.append(value)
        columns = columns.strip(', ')
        placeholders = placeholders.strip(', ')
        sql = f"INSERT INTO patient ({columns}) VALUES ({placeholders})"
        self.cur.execute(sql, tuple(values))
        self.cur.connection.commit()

    def find(self, table, partial_match=False, **kwargs):
        """
        Find records in table

        Parameters
        ---------------
        table : string
            table name
        partial_match : bool
            default False, True to allow partial matches
        **kwargs
            table_field: value search criteria

        Returns
        ---------------
        list
            a list of tuples with matches
            OR
            an empty list
        """

        columns = self.get_columns(table)
        search_conditions = {column: value for column, value in kwargs.items()
                   if column in columns}
        results = []
        if search_conditions:
            values = []
            sql = f"SELECT * FROM {table} WHERE "
            for column, value in search_conditions.items():
                sql += f'{column} LIKE ? AND '
                if partial_match:
                    value = f'%{value}%'
                values.append(value)
            sql = sql.strip('AND ')
            results = self.cur.execute(sql, tuple(values)).fetchall()
        return results

    def update_patient(self, id_, **kwargs):
        """
        Update patient details in patient table

        Parameters
        ---------------
        id_ : int
            patient id
        **kwargs
            update values provided in table_field: value format
        """

        columns = self.get_columns('patient')
        updated_values = {column: value for column, value in kwargs.items()
                          if column in columns}
        if updated_values:
            values = []
            sql = """UPDATE patient SET """
            for column, value in updated_values.items():
                sql += f'{column}=?, '
                values.append(value)
            sql = sql.strip(', ')
            sql += ' WHERE id=?'
            values.append(id_)
            self.cur.execute(sql, tuple(values))
            self.cur.connection.commit()

    def register_appointment(self, patient_id, date, doctor):
        sql = """INSERT INTO appointment VALUES (?, ?, ?)"""
        self.cur.execute(sql, (patient_id, date, doctor))
        self.cur.connection.commit()

    def cancel_appointment(self, date, doctor_id):
        sql = """
            DELETE FROM appointment WHERE app_datetime=? and doctor_id=?
        """
        self.cur.execute(sql, (date, doctor_id))
        self.cur.connection.commit()

    def add_employee(self, **kwargs):
        columns = self.get_columns('employee')
        employee = {column: value for column, value in kwargs.items()
                  if column in columns}
        columns = ''
        placeholders = ''
        values = []
        for column, value in employee.items():
            columns += f'{column}, '
            placeholders += '?, '
            values.append(value)
        columns = columns.strip(', ')
        placeholders = placeholders.strip(', ')
        sql = f"INSERT INTO employee ({columns}) VALUES ({placeholders})"
        self.cur.execute(sql, tuple(values))
        self.cur.connection.commit()
