from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime

from services.appointment_service import (
    get_doctors_by_department,
    get_available_slots,
    book_appointment_service,
    cancel_appointment_service
)

appointment_bp = Blueprint("appointment", __name__)


# -------------------------------------------------
# Get Doctors by Department
# GET /api/appointments/doctors?department_id=1
# -------------------------------------------------
@appointment_bp.route("/doctors", methods=["GET"])
@jwt_required()
def fetch_doctors_by_department():
    try:
        department_id = request.args.get("department_id", type=int)

        if not department_id:
            return jsonify({"error": "department_id is required"}), 400

        doctors = get_doctors_by_department(department_id)

        return jsonify({
            "department_id": department_id,
            "doctors": doctors
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------
# Get Available Slots
# GET /api/appointments/slots?doctor_id=1&date=2026-02-20
# -------------------------------------------------
@appointment_bp.route("/slots", methods=["GET"])
@jwt_required()
def fetch_available_slots():
    try:
        doctor_id = request.args.get("doctor_id", type=int)
        date_str = request.args.get("date")

        if not doctor_id or not date_str:
            return jsonify({"error": "doctor_id and date are required"}), 400

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format (YYYY-MM-DD required)"}), 400

        slots = get_available_slots(doctor_id, date)

        return jsonify({
            "doctor_id": doctor_id,
            "date": date_str,
            "available_slots": slots
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------
# Book Appointment
# POST /api/appointments/book
# -------------------------------------------------
@appointment_bp.route("/book", methods=["POST"])
@jwt_required()
def book_appointment():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        # Identity & Role
        patient_id = get_jwt_identity()
        claims = get_jwt()
        role = claims.get("role")

        if role != "patient":
            return jsonify({"error": "Only patients can book appointments"}), 403

        doctor_id = data.get("doctor_id")
        slot_id = data.get("slot_id")
        appointment_date_str = data.get("appointment_date")

        if not doctor_id or not slot_id or not appointment_date_str:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            appointment_date = datetime.strptime(
                appointment_date_str, "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({"error": "Invalid date format (YYYY-MM-DD required)"}), 400

        result = book_appointment_service(
            patient_id=int(patient_id),
            doctor_id=int(doctor_id),
            slot_id=int(slot_id),
            appointment_date=appointment_date
        )

        return jsonify({
            "message": "Appointment booked successfully",
            "appointment": result
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------
# Cancel Appointment
# DELETE /api/appointments/<appointment_id>
# -------------------------------------------------
@appointment_bp.route("/<int:appointment_id>", methods=["DELETE"])
@jwt_required()
def cancel_appointment(appointment_id):
    try:
        patient_id = get_jwt_identity()
        claims = get_jwt()
        role = claims.get("role")

        if role != "patient":
            return jsonify({"error": "Only patients can cancel appointments"}), 403

        result = cancel_appointment_service(
            appointment_id=appointment_id,
            patient_id=int(patient_id)
        )

        return jsonify(result), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500