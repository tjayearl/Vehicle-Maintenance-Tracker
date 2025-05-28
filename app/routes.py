from flask import Blueprint, request, jsonify
from .models import db, User, Vehicle, ServiceRecord

main = Blueprint("main", __name__)

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
        "owner": v.owner.name
    } for v in vehicles])

@main.route("/services", methods=["POST"])
def add_service():
    data = request.get_json()
    service = ServiceRecord(
        vehicle_id=data["vehicle_id"],
        service_type=data["service_type"],
        date=data.get("date"),
        cost=data["cost"]
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
        "cost": s.cost
    } for s in services])
