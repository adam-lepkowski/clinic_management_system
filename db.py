import sqlite3


CREATE_TABLE_PATIENT = """
    CREATE TABLE IF NOT EXISTS patient (
        id          INTEGER PRIMARY KEY,
        first_name  TEXT NOT NULL
    )
"""

class DB:

    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute(CREATE_TABLE_PATIENT)
        self.cur.connection.commit()