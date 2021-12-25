import unittest
from sqlite3 import IntegrityError
import datetime

from parameterized import parameterized

from db import DB
from tests.test_input import PATIENT_INPUT_1, PATIENT_INPUT_2


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
            'id', 'first_name', 'middle_name', 'last_name', 'date_of_birth',
            'gender', 'marital_status', 'nationality', 'email', 'phone',
            'document_no'
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
        ('middle_name', {'middle_name': None}),
        ('email', {'email': None})
    ])
    def test_register_patient_null_fields_valid(self, name, column):
        self.pat_1[name] = column[name]
        self.db.register_patient(**self.pat_1)
        result = self.db.cur.execute("SELECT * FROM patient").fetchone()
        expected = tuple(self.pat_1.values())
        self.assertEqual(expected, result)

    @parameterized.expand([
        ("first_name", {'first_name': None}),
        ('last_name', {'last_name': None}),
        ('date_of_birth', {'date_of_birth': None}),
        ('gender', {'gender': None}),
        ('marital_status', {'marital_status': None}),
        ('nationality', {'nationality': None}),
        ('phone', {'phone': None}),
        ('document_no', {'document_no': None})
    ])
    def test_register_patient_null_raises_error(self, name, column):
        with self.assertRaises(IntegrityError):
            self.pat_1[name] = column[name]
            self.db.register_patient(**self.pat_1)

    @parameterized.expand([
        ("first_name", {'first_name': ''}),
        ('last_name', {'last_name': ''}),
        ('date_of_birth', {'date_of_birth': ''}),
        ('gender', {'gender': ''}),
        ('marital_status', {'marital_status': ''}),
        ('nationality', {'nationality': ''}),
        ('email', {'email': ''}),
        ('phone', {'phone': ''}),
        ('document_no', {'document_no': ''})
    ])
    def test_empty_string_raises_error(self, name, column):
        with self.assertRaises(IntegrityError):
            self.pat_1[name] = column[name]
            self.db.register_patient(**self.pat_1)

    def test_date_of_birth_trigger_future_date_raises_error(self):
        delta = datetime.timedelta(days=1)
        today = datetime.date.today()
        future_date = today + delta
        self.pat_1['date_of_birth'] = future_date.strftime('%Y-%m-%d')
        with self.assertRaises(IntegrityError):
            self.db.register_patient(**self.pat_1)

    @parameterized.expand([
        ('invalid_format', '10-10-1990'),
        ('string_not_date', 'test'),
        ('integer', 1),
        ('float', 1.2),
        ('string_int', '1'),
        ('string_float', '1.2')
    ])
    def test_date_invalid_type_raises_error(self, name, value):
        self.pat_1['date_of_birth'] = value
        with self.assertRaises(IntegrityError):
            self.db.register_patient(**self.pat_1)

    @parameterized.expand([
        ('invalid_str', 'value'),
        ('int', 1),
        ('float', 1.1)
    ])
    def test_invalid_gender_raises_error(self, name, value):
        self.pat_1['gender'] = value
        with self.assertRaises(IntegrityError):
            self.db.register_patient(**self.pat_1)

    @parameterized.expand([
        ('invalid_str', 'value'),
        ('int', 1),
        ('float', 1.2)
    ])
    def test_invalid_marital_raises_error(self, name, value):
        self.pat_1['marital_status'] = value
        with self.assertRaises(IntegrityError):
            self.db.register_patient(**self.pat_1)

    @parameterized.expand([
        ('no_chars_before_@', '@email.com'),
        ('no_chars_after_@', 'test@'),
        ('no_chars_before_dot', 'test@.test'),
        ('no_chars_after_dot', 'test@test.')
    ])
    def test_invalid_email_raises_error(self, name, email):
        self.pat_1['email'] = email
        with self.assertRaises(IntegrityError):
            self.db.register_patient(**self.pat_1)

    @parameterized.expand([
        ('not_numeric', 'abcdefghijklm'),
        ('alphanumeric', '1234abdc123'),
        ('too_short', '12'),
        ('special_characters', '+1111111-')
    ])
    def test_invalid_phone_raises_error(self, name, phone):
        self.pat_1['phone'] = phone
        with self.assertRaises(IntegrityError):
            self.db.register_patient(**self.pat_1)


class TestFindPatient(unittest.TestCase):

    def setUp(self):
        self.pat = PATIENT_INPUT_2.copy()
        self.pat_1 = PATIENT_INPUT_1.copy()
        placeholders = '?, ' * len(self.pat)
        self.db = DB(':memory:')
        sql = f"INSERT INTO patient VALUES ({placeholders.strip(', ')})"
        self.db.cur.execute(sql, tuple(self.pat))
        self.db.cur.connection.commit()

    @parameterized.expand([
        ("first_name", {'first_name': 'First'}),
        ('last_name', {'last_name': 'Last'}),
        ('middle_name', {'middle_name': 'Middle'}),
        ('date_of_birth', {'date_of_birth': '1900-10-10'}),
        ('gender', {'gender': 'Male'}),
        ('marital_status', {'marital_status': 'Single'}),
        ('nationality', {'nationality': 'TestNation'}),
        ('email', {'email': 'test@email.com'}),
        ('phone', {'phone': '123456789'}),
        ('document_no', {'document_no': 'ABCD12345'})
    ])
    def test_find_patient(self, name, search_condition):
        result = self.db.find_patient(**search_condition)
        expected = [tuple(self.pat)]
        self.assertEqual(result, expected)


    def test_find_patient_multiple_conditions(self):
        result = self.db.find_patient(**self.pat_1)
        expected = [tuple(self.pat)]
        self.assertEqual(result, expected)

    @parameterized.expand([
        ('invalid_column', {'invalid': 'First'}),
        ('non_existent_patient', {'first_name': 'NonExistent'})
    ])
    def test_find_patient_invalid_values(self, name, search_conditions):
        result = self.db.find_patient(**search_conditions)
        expected = []
        self.assertEqual(expected, result)

    @parameterized.expand([
        ("first_name", {'first_name': 'st'}),
        ('last_name', {'last_name': 'la'}),
        ('middle_name', {'middle_name': 'm'}),
        ('date_of_birth', {'date_of_birth': '1900'}),
        ('gender', {'gender': 'ma'}),
        ('marital_status', {'marital_status': 'in'}),
        ('nationality', {'nationality': 'nat'}),
        ('email', {'email': '.com'}),
        ('phone', {'phone': '1'}),
        ('document_no', {'document_no': 'abc'})
    ])
    def test_find_partial_match(self, name, search_condition):
        result = self.db.find_patient(**search_condition)
        expected = [tuple(self.pat)]
        self.assertEqual(result, expected)


class TestUpdatePatient(unittest.TestCase):

    def setUp(self):
        self.pat = PATIENT_INPUT_2.copy()
        self.pat_1 = PATIENT_INPUT_1.copy()
        placeholders = '?, ' * len(self.pat)
        self.db = DB(':memory:')
        sql = f"INSERT INTO patient VALUES ({placeholders.strip(', ')})"
        self.db.cur.execute(sql, tuple(self.pat))
        self.db.cur.connection.commit()

    @parameterized.expand([
        ("first_name", {'first_name': 'NewFirst'}),
        ('last_name', {'last_name': 'NewLast'}),
        ('middle_name', {'middle_name': 'NewMiddle'}),
        ('date_of_birth', {'date_of_birth': '1900-12-10'}),
        ('gender', {'gender': 'Female'}),
        ('marital_status', {'marital_status': 'Widowed'}),
        ('nationality', {'nationality': 'NewTestNation'}),
        ('email', {'email': 'new_test@email.com'}),
        ('phone', {'phone': '012345678'}),
        ('document_no', {'document_no': 'EFGH12345'})
    ])
    def test_update_patient(self, name, update_vals):
        self.db.update_patient(id_=1, **update_vals)
        self.pat_1[name] = update_vals[name]
        sql = 'SELECT * FROM patient WHERE id=1'
        result = self.db.cur.execute(sql).fetchone()
        expected = tuple(self.pat_1.values())
        self.assertEqual(expected, result)

    @parameterized.expand([
        ("first_name", {'first_name': ''}),
        ('last_name', {'last_name': ''}),
        ('date_of_birth', {'date_of_birth': ''}),
        ('gender', {'gender': ''}),
        ('marital_status', {'marital_status': ''}),
        ('nationality', {'nationality': ''}),
        ('email', {'email': ''}),
        ('phone', {'phone': ''}),
        ('document_no', {'document_no': ''})
    ])
    def test_update_patient_empty_strings(self, name, update_vals):
        with self.assertRaises(IntegrityError):
            self.db.update_patient(id_=1, **update_vals)
        expected = tuple(self.pat_1.values())
        sql = 'SELECT * FROM patient WHERE id=1'
        result = self.db.cur.execute(sql).fetchone()
        self.assertEqual(expected, result)
