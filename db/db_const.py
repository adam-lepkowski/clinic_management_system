CREATE_TABLE_PATIENT = """
    CREATE TABLE IF NOT EXISTS patient (
        id              INTEGER PRIMARY KEY,
        first_name      TEXT NOT NULL CHECK (first_name != ''),
        middle_name     TEXT,
        last_name       TEXT NOT NULL CHECK (last_name != ''),
        date_of_birth   TEXT NOT NULL CHECK (date_of_birth != ''),
        gender          TEXT NOT NULL CHECK (gender != ''),
        marital_status  TEXT NOT NULL CHECK (marital_status != ''),
        nationality     TEXT NOT NULL CHECK (nationality != ''),
        email           TEXT CHECK (email != ''),
        phone           TEXT NOT NULL
                        CHECK (phone != '' AND LENGTH(phone) > 3),
        document_no     TEXT UNIQUE NOT NULL CHECK (document_no != '')
    )
"""

CREATE_TRIGGER_DOB = """
    CREATE TRIGGER IF NOT EXISTS validate_dob BEFORE INSERT
    ON patient
    BEGIN
        SELECT CASE
            WHEN STRFTIME('%Y-%m-%d', NEW.date_of_birth) IS NULL
                OR DATE(NEW.date_of_birth) > DATE('now') IS NULL
            THEN RAISE(ABORT, 'Invalid date, should be YYYY-MM-DD')
            WHEN DATE(NEW.date_of_birth) < DATE('1900-01-01')
            THEN RAISE(ABORT, 'Date can not be older than 1900-01-01')
            WHEN DATE(NEW.date_of_birth) > DATE('now')
            THEN RAISE(ABORT, 'Birth date can not be a date from the future')
        END;
    END;
"""

CREATE_TRIGGER_GENDER = """
    CREATE TRIGGER IF NOT EXISTS validate_gender BEFORE INSERT
    ON patient
    BEGIN
        SELECT CASE
            WHEN NEW.gender COLLATE NOCASE NOT IN ('male', 'female')
            THEN RAISE(ABORT, 'Invalid gender')
        END;
    END;
"""

CREATE_TRIGGER_MARITAL = """
    CREATE TRIGGER IF NOT EXISTS validate_marital BEFORE INSERT
    ON patient
    BEGIN
        SELECT CASE
            WHEN NEW.marital_status COLLATE NOCASE NOT IN (
                'single', 'widowed', 'married', 'divorced', 'separated')
            THEN RAISE(ABORT, 'Invalid marital status')
        END;
    END;
"""

CREATE_TRIGGER_EMAIL = """
    CREATE TRIGGER IF NOT EXISTS validate_email BEFORE INSERT
    ON patient
    BEGIN
        SELECT CASE
            WHEN NEW.email NOT LIKE '%_@__%.__%' THEN
            RAISE(ABORT, 'Invalid email address')
        END;
    END;
"""

CREATE_TRIGGER_PHONE = """
    CREATE TRIGGER IF NOT EXISTS validate_phone BEFORE INSERT
    ON patient
    BEGIN
        SELECT CASE
            WHEN NEW.phone GLOB '*[^0-9]*' THEN
            RAISE(ABORT, 'Only numbers allowed in phone field')
        END;
    END;
"""

CREATE_TABLE_APPOINTMENT = """
    CREATE TABLE IF NOT EXISTS appointment (
        patient_id      INTEGER NOT NULL REFERENCES patient(id) ON DELETE CASCADE,
        app_datetime    TEXT NOT NULL CHECK (app_datetime != ''),
        doctor_id       INTEGER NOT NULL REFERENCES employee(id) ON DELETE CASCADE,
        complaint       TEXT,
        examination     TEXT,
        diagnosis       TEXT,
        prescription    TEXT,
        recommendations TEXT,
        PRIMARY KEY     (app_datetime, doctor_id)
    )
"""

CREATE_TRIGGER_APP_DATE = """
    CREATE TRIGGER IF NOT EXISTS validate_app_date BEFORE INSERT
    ON appointment
    BEGIN
        SELECT CASE
            WHEN STRFTIME('%Y-%m-%d %H:%M', NEW.app_datetime) IS NULL
                OR DATE(NEW.app_datetime) > DATE('now') IS NULL
                OR STRFTIME('%H:%M', NEW.app_datetime) == '00:00'
            THEN RAISE(ABORT, 'Invalid date, should be YYYY-MM-DD HH:MM')
            WHEN DATE(NEW.app_datetime) < DATE('now')
            THEN RAISE(ABORT, 'Cannot schedule appoitments in the past')
        END;
    END;
"""

CREATE_TABLE_EMPLOYEE = """
    CREATE TABLE IF NOT EXISTS employee (
        id          INTEGER PRIMARY KEY,
        first_name  TEXT NOT NULL CHECK (first_name != ''),
        middle_name TEXT CHECK (middle_name != ''),
        last_name   TEXT NOT NULL CHECK (last_name != ''),
        position    TEXT NOT NULL CHECK (position != ''),
        specialty   TEXT CHECK (specialty != '')
    )
"""

CREATE_VIEW_APPOINTMENT = """
    CREATE VIEW IF NOT EXISTS app_v AS
    SELECT
        patient.id as patient_id,
        CASE
            WHEN patient.middle_name IS NOT NULL THEN
                patient.first_name || ' ' || patient.middle_name || ' ' || patient.last_name
            ELSE
                patient.first_name || ' ' || patient.last_name
        END AS p_full_name,
        employee.id as emp_id,
        CASE
            WHEN employee.middle_name IS NOT NULL THEN
                employee.first_name || ' ' || employee.middle_name || ' ' || employee.last_name
            ELSE
                employee.first_name || ' ' || employee.last_name
        END AS d_full_name,
        appointment.app_datetime
    FROM appointment
    INNER JOIN patient ON appointment.patient_id == patient.id
    INNER JOIN employee ON appointment.doctor_id == employee.id
"""

CREATE_TABLE_USER = """
    CREATE TABLE IF NOT EXISTS user (
        id              PRIMARY KEY REFERENCES employee (id) ON DELETE CASCADE,
        username        TEXT NOT NULL UNIQUE,
        hash_pw         TEXT CHECK (hash_pw != '')
    )
"""
