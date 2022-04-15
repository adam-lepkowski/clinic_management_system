# Clinic Management System
Manage patients, employees, doctors and their schedule. Write prescriptions and store data in a sqlite3 database file.

## First Launch
Before you start to schedule appointments you have to set up an administrator account. The first launch will prompt you to sign in as an admin user. After you successfully type in account details, you will be given a username (write it down) and a login screen will appear.

Now you have to get in to the admin panel and add employees – without that, you won’t be able to display full appointment frame.
You can use the admin panel „Add multiple” option to add employees and patients from a csv file. Columns must match specified table’s column names. I’ve provided csv files (mock_data directory) with mock data to make it possible to check out the functionality without the hassle.

After you add employees (and patients) you have to restart the app and voila, you are good to go.

## Available frames

### Registration
Register a single patient

### Find
Find patients – partial matches are allowed. Double clicking on a patient will initialize patient’s Medical Record

### Medical Record
View and update patient’s details. Check appointment history and each appointment details by double clicking on a record.

### Appointment
This frame has two settings. 

First – available to all users besides doctors (employee.role == doctor) allows you to schedule appointments to any doctor that is currently in your db. By default doctors are available in doctor option menu but you can group them by their specialty.
Default woring hours are 8 to 16 with a single appointment being 30 minutes long.
Double clicking on the label (on the right from the one displaying appointment hour) in schedule canvas will initialize a frame to set up an appointment with a chosen doctor  (you can still modify the choice in the new frame) and datetime. To set up an appointment you have to provide a valid patient document_no.

Second – available to doctors, allows the current user to see only his/hers own schedule. If the current user has an appoinement scheduled in a chosen date patients full name will be displayed on a corresponding label. Double clicking the label will initialize the appointment details frame. Doctor can complete the form containing complaint, examination, prescription and so on and submit them to the appointment’s details which can be later viewed in patient’s medical record.

### Admin panel
Available only to employees/users with role == admin. Add multiple rows to all available tables by „Add multiple”
Add/find a single employee. Create an user account with a temporary password by double clicking on a found employee record.
By clicking on the radiobutton you can switch the view to find users instead of employees and manage their accounts (delete account or update password).

### User panel
Update your password.

## Roles
There are 3 roles:
Admin – all frames and functionalities (besides filling up appointment details form) available.
Doctor – available frames – Find, Medical Record, Appointment (only to manage own schedule) and User panel
Others – Registration,  Find,  Medical Record,  Appointment (to schedule appointments)
The last one is made for nurses and employees responsible for setting up appointments and giving patients required information.

## Used graphics
The icons I used in the project are under Reshot Free License [Reshot license](https://www.reshot.com/license/)
Downloaded from [Reshot](https://www.reshot.com/)

