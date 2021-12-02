import unittest
from sqlite3 import IntegrityError

from parameterized import parameterized

from db import DB
from tests.test_input import PATIENT_INPUT_1


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
        expected = [
            'id', 'first_name', 'middle_name', 'last_name', 'date_of_birth'
        ]
        result = self.db._get_columns_patient()
        self.assertEqual(expected, result)


class TestRegisterPatient(unittest.TestCase):

    def setUp(self):
        self.db = DB(':memory:')
        self.pat_1 = PATIENT_INPUT_1.copy()

    def test_register_patient_valid(self):
        self.db.register_patient(**self.pat_1)
        result = self.db.cur.execute("SELECT * FROM patient").fetchone()
        expected = tuple(self.pat_1.values())
        self.assertEqual(expected, result)

    @parameterized.expand([
        ("first_name", {'first_name': ''}),
        ('last_name', {'last_name': ''}),
        ('date_of_birth', {'date_of_birth': ''})
    ])
    def test_empty_string_raises_error(self, name, column):
        with self.assertRaises(IntegrityError):
            self.db.register_patient(**column)
