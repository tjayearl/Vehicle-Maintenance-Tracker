from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from .routes import main
    app.register_blueprint(main)

    @app.route("/")
    def home():
        return {
            "message": "Vehicle Maintenance Tracker API is running.",
            "features": [
                "Add/view/update/delete vehicle records",
                "Log maintenance activities (e.g., oil change, tire rotation)",
                "Track costs and dates of service",
                "Set reminders for future maintenance"
            ],
            "models": {
                "User": ["id", "name", "email"],
                "Vehicle": ["id", "make", "model", "year", "user_id"],
                "ServiceRecord": ["id", "vehicle_id", "service_type", "date", "cost", "reminder_date"]
            }
        }

    return app