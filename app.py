from main import ClinicManagementSystem
from db import DB


if __name__ == '__main__':
    db = DB('test_database.db')
    clinic = ClinicManagementSystem(db)
    clinic.mainloop()
