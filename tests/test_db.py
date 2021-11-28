import unittest
from sqlite3 import IntegrityError

from db import DB


class TestDBInit(unittest.TestCase):

    def test_init(self):
        db = DB(':memory:')
        sql = """SELECT name FROM sqlite_master WHERE type='table'"""
        expected = [('patient', )]
        result = db.cur.execute(sql).fetchall()
        self.assertEqual(expected, result)


class TestDBGetColumnNames(unittest.TestCase):

    def setUp(self):
        self.db = DB(':memory:')

    def test_get_columns_patient(self):
        expected = ['id', 'first_name', 'middle_name']
        result = self.db._get_columns_patient()
        self.assertEqual(expected, result)


class TestRegisterPatient(unittest.TestCase):

    def setUp(self):
        self.db = DB(':memory:')

    def test_register_patient_valid(self):
        self.db.register_patient(first_name='First', middle_name='Middle')
        result = self.db.cur.execute("SELECT * FROM patient").fetchone()
        expected = (1, 'First', 'Middle')
        self.assertEqual(expected, result)

    def test_f_name_empty_string_raises_error(self):
        with self.assertRaises(IntegrityError):
            self.db.register_patient(first_name='')
