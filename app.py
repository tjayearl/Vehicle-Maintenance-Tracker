from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Setup SQLite DB path
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'vehicles.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year
        }

class ServiceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)  # Use string for simplicity
    cost = db.Column(db.Float, nullable=True)

    vehicle = db.relationship('Vehicle', backref=db.backref('services', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "service_type": self.service_type,
            "date": self.date,
            "cost": self.cost
        }

# Routes

@app.route('/')
def index():
    return jsonify({
        "message": "Vehicle Maintenance Tracker API is running",
        "features": [
            "List all vehicles",
            "Add a vehicle",
            "Book a service for a vehicle",
            "View all services",
            "Delete a service"
        ]
    })

# 1) List all vehicles
@app.route('/vehicles', methods=['GET'])
def list_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([v.to_dict() for v in vehicles])

# 2) Add a vehicle
@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    if not request.json:
        abort(400, description="Request must be JSON")
    data = request.json
    required = ['make', 'model', 'year']
    if not all(field in data for field in required):
        abort(400, description=f"Missing required fields: {required}")

    vehicle = Vehicle(make=data['make'], model=data['model'], year=data['year'])
    db.session.add(vehicle)
    db.session.commit()
    print(f"Added vehicle: {vehicle.to_dict()}")
    return jsonify(vehicle.to_dict()), 201

# 3) Book a service
@app.route('/services', methods=['POST'])
def book_service():
    if not request.json:
        abort(400, description="Request must be JSON")
    data = request.json
    required = ['vehicle_id', 'service_type', 'date']
    if not all(field in data for field in required):
        abort(400, description=f"Missing required fields: {required}")

    # Check vehicle exists
    vehicle = Vehicle.query.get(data['vehicle_id'])
    if not vehicle:
        abort(404, description="Vehicle not found")

    service = ServiceRecord(
        vehicle_id=data['vehicle_id'],
        service_type=data['service_type'],
        date=data['date'],
        cost=data.get('cost')
    )
    db.session.add(service)
    db.session.commit()
    print(f"Booked service: {service.to_dict()}")
    return jsonify(service.to_dict()), 201

# 4) View all services
@app.route('/services', methods=['GET'])
def view_services():
    services = ServiceRecord.query.all()
    return jsonify([s.to_dict() for s in services])

# 5) Delete a service
@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = ServiceRecord.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    print(f"Deleted service ID: {service_id}")
    return jsonify({"message": f"Service {service_id} deleted"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
