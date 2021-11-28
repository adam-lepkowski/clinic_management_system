import sqlite3


CREATE_TABLE_PATIENT = """
    CREATE TABLE IF NOT EXISTS patient (
        id          INTEGER PRIMARY KEY,
        first_name  TEXT NOT NULL,
        middle_name TEXT
    )
"""

class DB:
    """
    Class used to represent a connection to sqlite3 database
    """

    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute(CREATE_TABLE_PATIENT)
        self.cur.connection.commit()

    def _get_columns_patient(self):
        sql = "PRAGMA table_info('patient')"
        columns = self.cur.execute(sql).fetchall()
        column_names = [column[1] for column in columns]
        return column_names

    def register_patient(self, **kwargs):
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
