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
        email           TEXT,
        phone           TEXT NOT NULL
                        CHECK (phone != '' AND LENGTH(phone) > 3),
        document_no     TEXT NOT NULL CHECK (document_no != '')
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