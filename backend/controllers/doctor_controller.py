from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from services.doctor_service import (
    create_doctor_service,
    get_all_doctors_service,
    get_doctors_by_department_service,
    get_doctor_by_id_service
)

doctor_bp = Blueprint("doctor", __name__)


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

        result = create_doctor_service(
            name,
            specialization,
            department_id
        )

        return jsonify({
            "message": "Doctor created successfully",
            "doctor": result
        }), 201

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

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


# ---------------------------------------
# Get Doctors by Department
# GET /api/doctors/department/<id>
# ---------------------------------------
@doctor_bp.route("/department/<int:department_id>", methods=["GET"])
@jwt_required()
def get_doctors_by_department(department_id):
    try:
        doctors = get_doctors_by_department_service(department_id)

        return jsonify({
            "department_id": department_id,
            "doctors": doctors
        }), 200

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