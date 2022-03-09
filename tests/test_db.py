import unittest
import datetime

from parameterized import parameterized
import bcrypt

from db import DB
from tests.test_input import (PATIENT_INPUT_1, PATIENT_INPUT_2,
                              EMPLOYEE_INPUT_1, EMPLOYEE_INPUT_2,
                              USER_INPUT_1)


def insert_test_values(db, table, values):
    placeholders = '?, ' * len(values)
    sql = f"INSERT INTO {table} VALUES ({placeholders.strip(', ')})"
    db.cur.execute(sql, tuple(values))
    db.cur.connection.commit()


def db_factory(patient=None, employee=None, app=None, user=None):
    db = DB(':memory:')
    if patient:
        insert_test_values(db, 'patient', PATIENT_INPUT_2)
    if employee:
        insert_test_values(db, 'employee', EMPLOYEE_INPUT_2)
    if app:
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        values = (1, date, 1)
        insert_test_values(db, 'appointment', values)
    if user:
        insert_test_values(db, 'user', USER_INPUT_1)
    return db


class TestDBInit(unittest.TestCase):

    def test_init(self):
        db = DB(':memory:')
        sql = """SELECT name FROM sqlite_master WHERE type='table'"""
        expected = [
            ('patient', ), ('appointment', ), ('employee', ), ('user', )
        ]
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
        result = self.db.get_columns('patient')
        self.assertEqual(expected, result)


class TestRegisterPatient(unittest.TestCase):

    def setUp(self):
        self.db = DB(':memory:')
        self.pat_1 = PATIENT_INPUT_1.copy()

    def test_register_patient_valid(self):
        self.db.insert('patient', **self.pat_1)
        result = self.db.cur.execute("SELECT * FROM patient").fetchone()
        expected = tuple(self.pat_1.values())
        self.assertEqual(expected, result)

    @parameterized.expand([
        ('middle_name', {'middle_name': None}),
        ('email', {'email': None})
    ])
    def test_register_patient_null_fields_valid(self, name, column):
        self.pat_1[name] = column[name]
        self.db.insert('patient', **self.pat_1)
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
        with self.assertRaises(self.db.con.IntegrityError):
            self.pat_1[name] = column[name]
            self.db.insert('patient', **self.pat_1)

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
        with self.assertRaises(self.db.con.IntegrityError):
            self.pat_1[name] = column[name]
            self.db.insert('patient', **self.pat_1)

    def test_date_of_birth_trigger_future_date_raises_error(self):
        delta = datetime.timedelta(days=1)
        today = datetime.date.today()
        future_date = today + delta
        self.pat_1['date_of_birth'] = future_date.strftime('%Y-%m-%d')
        with self.assertRaises(self.db.con.IntegrityError):
            self.db.insert('patient', **self.pat_1)

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
        with self.assertRaises(self.db.con.IntegrityError):
            self.db.insert('patient', **self.pat_1)

    @parameterized.expand([
        ('invalid_str', 'value'),
        ('int', 1),
        ('float', 1.1)
    ])
    def test_invalid_gender_raises_error(self, name, value):
        self.pat_1['gender'] = value
        with self.assertRaises(self.db.con.IntegrityError):
            self.db.insert('patient', **self.pat_1)

    @parameterized.expand([
        ('invalid_str', 'value'),
        ('int', 1),
        ('float', 1.2)
    ])
    def test_invalid_marital_raises_error(self, name, value):
        self.pat_1['marital_status'] = value
        with self.assertRaises(self.db.con.IntegrityError):
            self.db.insert('patient', **self.pat_1)

    @parameterized.expand([
        ('no_chars_before_@', '@email.com'),
        ('no_chars_after_@', 'test@'),
        ('no_chars_before_dot', 'test@.test'),
        ('no_chars_after_dot', 'test@test.')
    ])
    def test_invalid_email_raises_error(self, name, email):
        self.pat_1['email'] = email
        with self.assertRaises(self.db.con.IntegrityError):
            self.db.insert('patient', **self.pat_1)

    @parameterized.expand([
        ('not_numeric', 'abcdefghijklm'),
        ('alphanumeric', '1234abdc123'),
        ('too_short', '12'),
        ('special_characters', '+1111111-')
    ])
    def test_invalid_phone_raises_error(self, name, phone):
        self.pat_1['phone'] = phone
        with self.assertRaises(self.db.con.IntegrityError):
            self.db.insert('patient', **self.pat_1)


class TestFindPatient(unittest.TestCase):

    def setUp(self):
        self.pat = PATIENT_INPUT_2.copy()
        self.pat_1 = PATIENT_INPUT_1.copy()
        self.db = db_factory(patient=True)

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
        result = self.db.find('patient', **search_condition)
        expected = [tuple(self.pat)]
        self.assertEqual(result, expected)


    def test_find_patient_multiple_conditions(self):
        result = self.db.find('patient', **self.pat_1)
        expected = [tuple(self.pat)]
        self.assertEqual(result, expected)

    @parameterized.expand([
        ('invalid_column', {'invalid': 'First'}),
        ('non_existent_patient', {'first_name': 'NonExistent'})
    ])
    def test_find_patient_invalid_values(self, name, search_conditions):
        result = self.db.find('patient', **search_conditions)
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
        result = self.db.find(
            'patient', partial_match = True, **search_condition
        )
        expected = [tuple(self.pat)]
        self.assertEqual(result, expected)


class TestUpdatePatient(unittest.TestCase):

    def setUp(self):
        self.pat_1 = PATIENT_INPUT_1.copy()
        self.db = db_factory(patient=True)

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
        self.db.update('patient', id_=1, **update_vals)
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
        with self.assertRaises(self.db.con.IntegrityError):
            self.db.update('patient', id_=1, **update_vals)
        expected = tuple(self.pat_1.values())
        sql = 'SELECT * FROM patient WHERE id=1'
        result = self.db.cur.execute(sql).fetchone()
        self.assertEqual(expected, result)


class TestRegisterAppointment(unittest.TestCase):

    def setUp(self):
        self.pat = PATIENT_INPUT_2.copy()
        self.doc =  EMPLOYEE_INPUT_2.copy()
        self.db = db_factory(patient=True, employee=True)

    def test_register_appointment(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        test_input = {'patient_id': 1, 'app_datetime': date, 'doctor_id': 1}
        expected = tuple(test_input.values())
        self.db.insert('appointment', **test_input)
        result = self.db.cur.execute('SELECT * FROM appointment').fetchone()
        self.assertEqual(expected, result)

    def test_register_appointment_invalid_patient_id(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        test_input = {'patient_id': 3, 'app_datetime': date, 'doctor_id': 1}
        with self.assertRaises(self.db.con.IntegrityError):
            self.db.insert('appointment', **test_input)

    def test_invalid_date_raises_error(self):
        test_input = {'patient_id': 1, 'app_datetime': 'date', 'doctor_id': 1}
        with self.assertRaises(self.db.con.IntegrityError):
            self.db.insert('appointment', **test_input)

    def test_same_dates_same_doc_raises_error(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        test_input = {'patient_id': 1, 'app_datetime': date, 'doctor_id': 1}
        expected = tuple(test_input.values())
        self.db.insert('appointment', **test_input)
        result = self.db.cur.execute('SELECT * FROM appointment').fetchone()
        self.assertEqual(expected, result)
        with self.assertRaises(self.db.con.IntegrityError):
            self.db.insert('appointment', **test_input)

    def test_same_date_diff_doc(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.doc[0] = 2
        doc_placeholders = '?, ' * len(self.doc)
        doc_sql = f"""INSERT INTO employee VALUES
                      ({doc_placeholders.strip(', ')})"""
        self.db.cur.execute(doc_sql, tuple(self.doc))
        test_input_1 = {'patient_id': 1, 'app_datetime': date, 'doctor_id': 1}
        test_input_2 = {'patient_id': 1, 'app_datetime': date, 'doctor_id': 2}
        expected_1 = tuple(test_input_1.values())
        expected_2 = tuple(test_input_2.values())
        self.db.insert('appointment', **test_input_1)
        self.db.insert('appointment', **test_input_2)
        result = self.db.cur.execute('SELECT * FROM appointment').fetchall()
        expected = [expected_1, expected_2]
        self.assertEqual(expected, result)


class TestFindAppointment(unittest.TestCase):

    def setUp(self):
        self.pat = PATIENT_INPUT_2.copy()
        self.doc =  EMPLOYEE_INPUT_2.copy()
        self.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.db = db_factory(patient=True, employee=True, app=True)

    @parameterized.expand([
        ('patient_id', {'patient_id': 1}),
        ('doctor', {'doctor_id': 1})
    ])
    def test_find_appointment(self, name, search_condition):
        expected = [(1, self.date, 1)]
        result = self.db.find('appointment', **search_condition)
        self.assertEqual(expected, result)

    def test_find_appointment_by_datetime(self):
        expected = [(1, self.date, 1)]
        result = self.db.find('appointment', app_datetime=self.date)
        self.assertEqual(expected, result)


class TestAddEmployee(unittest.TestCase):

    def setUp(self):
        self.db = DB(':memory:')
        self.emp = EMPLOYEE_INPUT_1.copy()

    def test_add_employee(self):
        self.db.insert('employee', **self.emp)
        expected = tuple(self.emp.values())
        result = self.db.cur.execute('SELECT * FROM employee').fetchone()
        self.assertEqual(expected, result)

    @parameterized.expand([
        ("first_name", {'first_name': ''}),
        ('last_name', {'last_name': ''}),
        ('middle_name', {'middle_name': ''}),
        ('position', {'position': ''}),
        ('specialty', {'specialty': ''})
    ])
    def test_add_employee_empty_string_raises_error(self, name, column):
        self.emp[name] = column[name]
        with self.assertRaises(self.db.con.IntegrityError):
            self.db.insert('employee', **self.emp)


class TestFindEmployee(unittest.TestCase):

    def setUp(self):
        self.db = db_factory(employee=True)
        self.emp = EMPLOYEE_INPUT_1.copy()

    def test_find_employee(self):
        expected = [tuple(self.emp.values())]
        result = self.db.find('employee', id=self.emp['id'])
        self.assertEqual(expected, result)

    @parameterized.expand([
        ('id', {'id': 'Test'}),
        ('first_name', {'first_name': 'Test'}),
        ('middle_name', {'middle_name': 'Test'}),
        ('last_name', {'last_name': 'Test'}),
        ('position', {'position': 'Test'}),
        ('specialty', {'specialty': 'Test'})
    ])
    def test_find_employee_no_matches(self, name, column):
        expected = []
        result = self.db.find('employee', **column)
        self.assertEqual(expected, result)


class TestFindFullAppointment(unittest.TestCase):

    def setUp(self):
        self.db = db_factory(employee=True, app=True, patient=True)

    def test_find_full_appointment(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        expected = [
            (1, 'First Middle Last', 1, 'EmpFirst EmpMiddle EmpLast', date)
            ]
        result = self.db.find('app_v', app_datetime=date)
        self.assertEqual(expected, result)


class TestCreateUserAccount(unittest.TestCase):

    def setUp(self):
        self.db = db_factory(employee=True)
        self.emp =  EMPLOYEE_INPUT_1.copy()

    def test_add_account(self):
        self.db.create_user_account(self.emp['id'])
        sql = "SELECT * FROM user"
        result = self.db.cur.execute(sql).fetchone()
        expected = (1, 'empfirst.emplast', None)
        self.assertEqual(expected, result)

class TestUpdatePassword(unittest.TestCase):

    def setUp(self):
        self.db = db_factory(employee=True, user=True)

    def test_update_password(self):
        pwd = 'testpwd1'
        self.db.update_pwd(1, pwd)
        sql = 'SELECT hash_pw FROM user WHERE id=1'
        result = self.db.cur.execute(sql).fetchone()
        self.assertTrue(bcrypt.checkpw(pwd.encode('utf-8'), result[0]))


class TestDelete(unittest.TestCase):

    def setUp(self):
        self.db = db_factory(patient=True, employee=True, app=True, user=True)
        self.app_sql = 'SELECT * FROM appointment'
        self.pat_sql = 'SELECT * FROM patient'
        self.emp_sql = 'SELECT * FROM employee'
        self.usr_sql = 'SELECT * FROM user'

    def test_delete_patient(self):
        appointments = self.db.cur.execute(self.app_sql).fetchall()
        patients = self.db.cur.execute(self.pat_sql).fetchall()
        self.assertEqual(len(patients), 1)
        self.assertEqual(len(appointments), 1)
        self.db.delete('patient', id=1)
        appointments = self.db.cur.execute(self.app_sql).fetchall()
        patients = self.db.cur.execute(self.pat_sql).fetchall()
        self.assertEqual(len(patients), 0)
        self.assertEqual(len(appointments), 0)

    def test_delete_appointment(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.db.delete('appointment', app_datetime=date, doctor_id=1)
        expected = None
        result = self.db.cur.execute('SELECT * FROM appointment').fetchone()
        self.assertEqual(expected, result)

    @parameterized.expand([
        ("date", {'app_datetime': 'invalid_date', 'doctor_id': 1}),
        ('doctor_id', {'app_datetime': '', 'doctor_id': 2})
    ])
    def test_delete_appointment_invalid_input(self, name, vals):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        if name != 'date':
            vals['app_datetime'] = date
        self.db.delete('appointment', **vals)
        expected = (1, date, 1)
        result = self.db.cur.execute('SELECT * FROM appointment').fetchone()
        self.assertEqual(expected, result)

    def test_delete_employee(self):
        appointments = self.db.cur.execute(self.app_sql).fetchall()
        emp = self.db.cur.execute(self.emp_sql).fetchall()
        self.assertEqual(len(emp), 1)
        self.assertEqual(len(appointments), 1)
        self.db.delete('employee', id=1)
        appointments = self.db.cur.execute(self.app_sql).fetchall()
        emp = self.db.cur.execute(self.emp_sql).fetchall()
        self.assertEqual(len(emp), 0)
        self.assertEqual(len(appointments), 0)
