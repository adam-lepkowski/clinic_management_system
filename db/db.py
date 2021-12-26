import sqlite3

from db.db_const import (CREATE_TABLE_PATIENT, CREATE_TRIGGER_DOB,
                         CREATE_TRIGGER_GENDER, CREATE_TRIGGER_MARITAL,
                         CREATE_TRIGGER_EMAIL, CREATE_TRIGGER_PHONE)


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
        self.cur.connection.commit()

    def _get_columns_patient(self):
        """
        Get column headers from table patient

        Returns
        ---------------
        list
            a list of column headers
        """

        sql = "PRAGMA table_info('patient')"
        columns = self.cur.execute(sql).fetchall()
        column_names = [column[1] for column in columns]
        return column_names

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

        columns = self._get_columns_patient()
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

    def find_patient(self, **kwargs):
        """
        Find patients in patient table

        Search criteria be provided in format column_field=value, if
        column_field does not exist in table patient it is omitted.
        Search is case insensitive and allows partial matches.

        Parameters
        ---------------
        **kwargs
            table_field: value

        Returns
        ---------------
        list
            a list of tuples with matches
            OR
            an empty list
        """

        columns = self._get_columns_patient()
        search_conditions = {column: value for column, value in kwargs.items()
                   if column in columns}
        results = []
        if search_conditions:
            values = []
            sql = "SELECT * FROM patient WHERE "
            for column, value in search_conditions.items():
                sql += f'{column} LIKE ? AND '
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

        columns = self._get_columns_patient()
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
