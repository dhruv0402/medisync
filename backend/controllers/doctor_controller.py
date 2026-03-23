from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from backend.services.doctor_service import (
    create_doctor_service,
    get_all_doctors_service,
    get_doctors_by_department_service,
    get_doctor_by_id_service,
)

doctor_bp = Blueprint("doctor", __name__, url_prefix="/api/doctors")


# ---------------------------------------
# Create Doctor (Admin Only)
# POST /api/doctors/
# ---------------------------------------
@doctor_bp.route("/", methods=["POST"])
@jwt_required()
def create_doctor():
    try:
        claims = get_jwt()

        if claims.get("role") != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()

        name = data.get("name")
        specialization = data.get("specialization")
        department_id = data.get("department_id")

        if not all([name, specialization, department_id]):
            return jsonify({"error": "Missing required fields"}), 400

        result = create_doctor_service(name, specialization, department_id)

        return jsonify(
            {"message": "Doctor created successfully", "doctor": result}
        ), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


# ---------------------------------------
# Get All Doctors
# GET /api/doctors/
# ---------------------------------------
@doctor_bp.route("/", methods=["GET"])
@jwt_required()
def get_doctors():
    try:
        doctors = get_all_doctors_service()

        return jsonify({"doctors": doctors}), 200

    except Exception as e:
        print("DOCTOR FETCH ERROR:", str(e))  # 👈 ADD THIS
        return jsonify({"error": str(e)}), 500


# ---------------------------------------
# Get Doctors by Department
# GET /api/doctors/department/<id>
# ---------------------------------------
@doctor_bp.route("/department/<int:department_id>", methods=["GET"])
@jwt_required()
def get_doctors_by_department(department_id):
    try:
        doctors = get_doctors_by_department_service(department_id)

        return jsonify({"department_id": department_id, "doctors": doctors}), 200

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


# ---------------------------------------
# Get Doctor by ID
# GET /api/doctors/<id>
# ---------------------------------------
@doctor_bp.route("/<int:doctor_id>", methods=["GET"])
@jwt_required()
def get_doctor(doctor_id):
    try:
        doctor = get_doctor_by_id_service(doctor_id)

        return jsonify(doctor), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


# ---------------------------------------
# Doctor: Get My Appointments
# GET /api/doctors/my/appointments
# ---------------------------------------
@doctor_bp.route("/my/appointments", methods=["GET"])
@jwt_required()
def get_my_appointments():
    try:
        claims = get_jwt()

        if claims.get("role") != "doctor":
            return jsonify({"error": "Unauthorized"}), 403

        user_id = int(get_jwt_identity())

        from backend.utils.db import get_db_session
        from backend.models.doctor import Doctor
        from backend.models.appointment import Appointment
        from sqlalchemy.orm import joinedload

        session = get_db_session()

        doctor = session.query(Doctor).filter(Doctor.user_id == user_id).first()

        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

        appointments = (
            session.query(Appointment)
            .options(joinedload(Appointment.slot))
            .filter(Appointment.doctor_id == doctor.id)
            .all()
        )

        result = [
            {
                "appointment_id": a.id,
                "status": a.status,
                "date": str(a.slot.date),
                "start_time": str(a.slot.start_time),
                "end_time": str(a.slot.end_time),
            }
            for a in appointments
        ]

        return jsonify({"count": len(result), "appointments": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------
# Doctor: Earnings
# GET /api/doctors/my/earnings
# ---------------------------------------
@doctor_bp.route("/my/earnings", methods=["GET"])
@jwt_required()
def get_my_earnings():
    try:
        claims = get_jwt()

        if claims.get("role") != "doctor":
            return jsonify({"error": "Unauthorized"}), 403

        user_id = int(get_jwt_identity())

        from backend.utils.db import get_db_session
        from backend.models.doctor import Doctor
        from backend.models.invoice import Invoice
        from sqlalchemy import func

        session = get_db_session()

        doctor = session.query(Doctor).filter(Doctor.user_id == user_id).first()

        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

        total = (
            session.query(func.sum(Invoice.total_amount))
            .filter(Invoice.doctor_id == doctor.id, Invoice.status == "paid")
            .scalar()
        )

        return jsonify(
            {"doctor_id": doctor.id, "total_earnings": float(total or 0)}
        ), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
