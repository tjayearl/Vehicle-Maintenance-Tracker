from flask import Blueprint, request, jsonify
from .models import db, User, Vehicle, ServiceRecord
from datetime import datetime

main = Blueprint("main", __name__)

# USERS
@main.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created!", "user": {"id": user.id, "name": user.name}}), 201

@main.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

# VEHICLES
@main.route("/vehicles", methods=["POST"])
def add_vehicle():
    data = request.get_json()
    vehicle = Vehicle(make=data["make"], model=data["model"], year=data["year"], user_id=data["user_id"])
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle added!"}), 201

@main.route("/vehicles", methods=["GET"])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{
        "id": v.id,
        "make": v.make,
        "model": v.model,
        "year": v.year,
        "user_id": v.user_id,
        "owner": v.owner.name
    } for v in vehicles])

@main.route("/vehicles/<int:vehicle_id>", methods=["PUT"])
def update_vehicle(vehicle_id):
    data = request.get_json()
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    vehicle.make = data.get("make", vehicle.make)
    vehicle.model = data.get("model", vehicle.model)
    vehicle.year = data.get("year", vehicle.year)
    db.session.commit()
    return jsonify({"message": "Vehicle updated!"})

@main.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle deleted!"})

# SERVICE RECORDS
@main.route("/services", methods=["POST"])
def add_service():
    data = request.get_json()
    service = ServiceRecord(
        vehicle_id=data["vehicle_id"],
        service_type=data["service_type"],
        date=datetime.strptime(data["date"], '%Y-%m-%d') if "date" in data else datetime.utcnow(),
        cost=data["cost"],
        reminder_date=datetime.strptime(data["reminder_date"], '%Y-%m-%d') if "reminder_date" in data else None
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({"message": "Service record added!"}), 201

@main.route("/services", methods=["GET"])
def get_services():
    services = ServiceRecord.query.all()
    return jsonify([{
        "id": s.id,
        "vehicle_id": s.vehicle_id,
        "type": s.service_type,
        "date": s.date.strftime('%Y-%m-%d'),
        "cost": s.cost,
        "reminder_date": s.reminder_date.strftime('%Y-%m-%d') if s.reminder_date else None
    } for s in services])

@main.route("/services/<int:service_id>", methods=["PUT"])
def update_service(service_id):
    service = ServiceRecord.query.get_or_404(service_id)
    data = request.get_json()
    service.service_type = data.get("service_type", service.service_type)
    service.date = datetime.strptime(data["date"], '%Y-%m-%d') if "date" in data else service.date
    service.cost = data.get("cost", service.cost)
    service.reminder_date = datetime.strptime(data["reminder_date"], '%Y-%m-%d') if "reminder_date" in data else service.reminder_date
    db.session.commit()
    return jsonify({"message": "Service record updated!"})

@main.route("/services/<int:service_id>", methods=["DELETE"])
def delete_service(service_id):
    service = ServiceRecord.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service record deleted!"})