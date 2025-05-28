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

    # Load config
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register the main blueprint from routes.vehicle_routes
    from routes.vehicle_routes import main
    app.register_blueprint(main)

    # Optional: Define a simple root route here if needed
    @app.route("/")
    def home():
        return {"message": "Vehicle Maintenance Tracker API is running."}

    return app

# Use factory properly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
