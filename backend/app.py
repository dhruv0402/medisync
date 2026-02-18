import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Initialize extensions (declared globally)
jwt = JWTManager()
engine = None
SessionLocal = None


def create_app():
    app = Flask(__name__)

    # ----------------------------
    # Basic Configuration
    # ----------------------------
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "super-secret-key")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")

    # ----------------------------
    # Database Configuration
    # ----------------------------
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME")

    DATABASE_URL = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    global engine, SessionLocal
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # ----------------------------
    # Initialize Extensions
    # ----------------------------
    CORS(app)
    jwt.init_app(app)

    # ----------------------------
    # Register Blueprints
    # ----------------------------
    from controllers.auth_controller import auth_bp
    from controllers.appointment_controller import appointment_bp
    from controllers.billing_controller import billing_bp
    from controllers.doctor_controller import doctor_bp
    from controllers.patient_controller import patient_bp
    from controllers.report_controller import report_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(appointment_bp, url_prefix="/api/appointments")
    app.register_blueprint(billing_bp, url_prefix="/api/billing")
    app.register_blueprint(doctor_bp, url_prefix="/api/doctors")
    app.register_blueprint(patient_bp, url_prefix="/api/patients")
    app.register_blueprint(report_bp, url_prefix="/api/reports")

    # ----------------------------
    # Health Check Route
    # ----------------------------
    @app.route("/")
    def health_check():
        return jsonify({
            "status": "running",
            "service": "MediSync API"
        }), 200

    # ----------------------------
    # Global Error Handler
    # ----------------------------
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500

    return app


# ----------------------------
# Run Server
# ----------------------------
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)