import unittest

from db import DB


class TestDBInit(unittest.TestCase):

    def test_init(self):
        db = DB(':memory:')
        sql = """SELECT name FROM sqlite_master WHERE type='table'"""
        expected = [('patient', )]
        result = db.cur.execute(sql).fetchall()
        self.assertEqual(expected, result)


class TestRegisterPatient(unittest.TestCase):

    def setUp(self):
        self.db = DB(':memory:')

    def test_register_patient_valid(self):
        self.db.register_patient('Test')
        result = self.db.cur.execute("SELECT * FROM patient").fetchone()
        expected = (1, 'Test')
        self.assertEqual(expected, result)
