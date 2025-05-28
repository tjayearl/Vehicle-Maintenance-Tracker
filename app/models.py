from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    vehicles = db.relationship('Vehicle', backref='owner', cascade="all, delete")

    def __repr__(self):
        return f"<User {self.name}>"

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_records = db.relationship('ServiceRecord', backref='vehicle', cascade="all, delete")

    def __repr__(self):
        return f"<Vehicle {self.make} {self.model} ({self.year})>"

class ServiceRecord(db.Model):
    __tablename__ = 'service_records'

    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    cost = db.Column(db.Float, nullable=False)

    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)

    def __repr__(self):
        return f"<ServiceRecord {self.service_type} on {self.date}>"
