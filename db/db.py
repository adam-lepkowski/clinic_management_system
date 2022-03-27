import sqlite3

import bcrypt

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
        self.cur.execute(CREATE_TABLE_USER)
        self.cur.execute('PRAGMA foreign_keys=on')
        self.cur.connection.commit()

    def get_columns(self, table):
        """
        Get column headers from given table

        Parameters
        ---------------
        table : string
            table or view name

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

    def map_column_value(self, table, **kwargs):
        columns = self.get_columns(table)
        table_dict = {column: value for column, value in kwargs.items()
                      if column in columns}
        return table_dict

    def insert(self, table, **kwargs):
        """
        Insert values into table

        Parameters
        ---------------
        table : string
            table name
        **kwargs
            table_field: value
        """

        insert_dict = self.map_column_value(table, **kwargs)
        columns = ''
        placeholders = ''
        values = []
        for column, value in insert_dict.items():
            columns += f'{column}, '
            placeholders += '?, '
            values.append(value)
        columns = columns.strip(', ')
        placeholders = placeholders.strip(', ')
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cur.execute(sql, tuple(values))
        self.cur.connection.commit()

    def find(self, table, partial_match=False, **kwargs):
        """
        Find records in table

        Parameters
        ---------------
        table : string
            table name
        partial_match : bool, default=False
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

        find_dict = self.map_column_value(table, **kwargs)
        results = []
        if find_dict:
            values = []
            sql = f"SELECT * FROM {table} WHERE "
            for column, value in find_dict.items():
                sql += f'{column} LIKE ? AND '
                if partial_match:
                    value = f'%{value}%'
                values.append(value)
            sql = sql.rstrip('AND ')
            results = self.cur.execute(sql, tuple(values)).fetchall()
        return results

    def update(self, table, id_, **kwargs):
        """
        Update record in table

        Parameters
        ---------------
        table : string
            table name
        id_ : int
            id
        **kwargs
            update values provided in table_field: value format
        """

        update_dict = self.map_column_value(table, **kwargs)
        if update_dict:
            values = []
            sql = f"""UPDATE {table} SET """
            for column, value in update_dict.items():
                sql += f'{column}=?, '
                values.append(value)
            sql = sql.strip(', ')
            sql += ' WHERE id=?'
            values.append(id_)
            self.cur.execute(sql, tuple(values))
            self.cur.connection.commit()

    def delete(self, table, **kwargs):
        delete_dict = self.map_column_value(table, **kwargs)
        if delete_dict:
            sql = f'DELETE FROM {table} WHERE '
            values = []
            for column, value in delete_dict.items():
                sql += f'{column}=? AND '
                values.append(value)
        sql = sql.rstrip('AND ')
        self.cur.execute(sql, tuple(values))
        self.cur.connection.commit()

    def create_user_account(self, emp_id):
        result = self.find('employee', id=emp_id)
        columns = self.get_columns('employee')
        emp = {col: val for col, val in zip(columns, result[0])}
        username = f"{emp['first_name']}.{emp['last_name']}".lower()
        same_name_search = {
            'first_name': emp['first_name'],
            'last_name': emp['last_name']
        }
        results = self.find('employee', **same_name_search)
        if len(results) > 1:
            username += str(len(results))
        self.insert('user', id=emp['id'], username=username)

    def update_pwd(self, emp_id, pwd):
        hash_pw = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
        self.update('user', emp_id, hash_pw=hash_pw)
