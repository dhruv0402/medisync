import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from utils.db import engine
from models.base import Base
# -------------------------------------
# Load Environment Variables
# -------------------------------------
load_dotenv()

jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # -------------------------------------
    # Basic Configuration
    # -------------------------------------
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "super-secret-key")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    app.config["ENV"] = os.getenv("FLASK_ENV", "development")
    # -------------------------------------
    # Database Initialization (Dev Only)
    # -------------------------------------
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables verified/created.")
    except SQLAlchemyError as e:
        print("❌ Database initialization failed:", str(e))

    # -------------------------------------
    # Initialize Extensions
    # -------------------------------------
    CORS(app)
    jwt.init_app(app)

    # -------------------------------------
    # Register Blueprints
    # -------------------------------------
    from controllers.auth_controller import auth_bp
    from controllers.appointment_controller import appointment_bp
    from controllers.billing_controller import billing_bp
    from controllers.doctor_controller import doctor_bp
    from controllers.patient_controller import patient_bp
    from controllers.report_controller import report_bp
    from controllers.department_controller import department_bp
    from controllers.availability_slot_controller import slot_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(appointment_bp, url_prefix="/api/appointments")
    app.register_blueprint(billing_bp, url_prefix="/api/billing")
    app.register_blueprint(doctor_bp, url_prefix="/api/doctors")
    app.register_blueprint(patient_bp, url_prefix="/api/patients")
    app.register_blueprint(report_bp, url_prefix="/api/reports")
    app.register_blueprint(department_bp, url_prefix="/api/departments")
    app.register_blueprint(slot_bp, url_prefix="/api/slots")
    # -------------------------------------
    # Root Health Check
    # -------------------------------------
    @app.route("/", methods=["GET"])
    def root():
        return jsonify({
            "status": "running",
            "service": "MediSync API",
            "environment": app.config["ENV"]
        }), 200

    # -------------------------------------
    # Dedicated Health Endpoint
    # -------------------------------------
    
    @app.route("/health", methods=["GET"])
    def health():
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            return jsonify({
                "status": "healthy",
                "database": "connected"
            }), 200

        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }), 500

    # -------------------------------------
    # 404 Handler (Important)
    # -------------------------------------
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "error": "Route Not Found",
            "message": str(e)
        }), 404

    # -------------------------------------
    # Global Error Handler
    # -------------------------------------
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)