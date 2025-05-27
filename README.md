# Vehicle Maintenance Tracker

A web-based application to help users **track vehicle service history, costs, and future maintenance reminders**. Built with **Flask**, **SQLAlchemy**, and **SQLite**, this project is ideal for individual vehicle owners or small fleet managers.

---

##  Features

-  Add, view, update, and delete **vehicle records**
-  Log **maintenance activities** (e.g., oil change, tire rotation)
-  Track **service dates** and **costs**
-  Set **reminders** for upcoming vehicle maintenance
-  User-based access and ownership of vehicles

---

##  Technologies Used

- **Python**
- **Flask** (Web framework)
- **Flask-SQLAlchemy** (ORM)
- **Flask-Migrate** (Database migrations)
- **SQLite** (Development database)
- **HTML / CSS / JS** (Frontend – optional future addition)

---

##  Database Models

```python
User
- id (int)
- name (string)
- email (string)

Vehicle
- id (int)
- make (string)
- model (string)
- year (int)
- user_id (foreign key to User)

ServiceRecord
- id (int)
- vehicle_id (foreign key to Vehicle)
- service_type (string)
- date (string)
- cost (float)
