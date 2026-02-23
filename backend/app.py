import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from utils.db import engine
from models.base import Base
import logging
# -------------------------------------
# Load Environment Variables
# -------------------------------------
load_dotenv()

# -------------------------------------
# Structured Logging Configuration
# -------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

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
        logger.info("Database tables verified/created.")
    except SQLAlchemyError as e:
        logger.exception("Database initialization failed")

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
    from controllers.invoice_controller import invoice_bp
    from controllers.admin_controller import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(appointment_bp, url_prefix="/api/appointments")
    app.register_blueprint(billing_bp, url_prefix="/api/billing")
    app.register_blueprint(doctor_bp, url_prefix="/api/doctors")
    app.register_blueprint(patient_bp, url_prefix="/api/patients")
    app.register_blueprint(report_bp, url_prefix="/api/reports")
    app.register_blueprint(department_bp, url_prefix="/api/departments")
    app.register_blueprint(slot_bp, url_prefix="/api/slots")
    app.register_blueprint(invoice_bp)
    app.register_blueprint(admin_bp)
    # -------------------------------------
    # Root Health Check
    # -------------------------------------
    @app.route("/", methods=["GET"])
    def root():
        return jsonify({
            "success": True,
            "data": {
                "status": "running",
                "service": "MediSync API",
                "environment": app.config["ENV"]
            }
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
                "success": True,
                "data": {
                    "status": "healthy",
                    "database": "connected"
                }
            }), 200

        except Exception as e:
            logger.exception("Health check failed")
            return jsonify({
                "success": False,
                "error": "Service unhealthy"
            }), 500

    # -------------------------------------
    # 404 Handler (Important)
    # -------------------------------------
    @app.errorhandler(404)
    def not_found(e):
        logger.warning(f"404 - Route not found: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Route Not Found"
        }), 404

    # -------------------------------------
    # Global Error Handler
    # -------------------------------------
    @app.errorhandler(ValueError)
    def handle_value_error(e):
        logger.warning(f"Client error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(e):
        logger.exception("Database error occurred")
        return jsonify({
            "success": False,
            "error": "Database error"
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)