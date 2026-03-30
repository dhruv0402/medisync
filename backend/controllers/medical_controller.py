from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from backend.services.medical_service import (
    create_medical_record,
    get_patient_records,
)

medical_bp = Blueprint("medical", __name__, url_prefix="/api/medical")


@medical_bp.route("/create", methods=["POST"])
@jwt_required()
def create_record():
    claims = get_jwt()

    if claims.get("role") != "doctor":
        return jsonify({"error": "Unauthorized"}), 403

    from backend.models.doctor import Doctor
    from backend.utils.db import get_db_session

    user_id = int(get_jwt_identity())
    session = get_db_session()

    doctor = session.query(Doctor).filter(Doctor.user_id == user_id).first()
    if not doctor:
        session.close()
        return jsonify({"error": "Doctor profile not found"}), 404

    doctor_id = doctor.id
    session.close()

    data = request.get_json()

    result = create_medical_record(
        appointment_id=data.get("appointment_id"),
        patient_id=data.get("patient_id"),
        doctor_id=doctor_id,
        diagnosis=data.get("diagnosis"),
        prescription=data.get("prescription"),
        notes=data.get("notes"),
    )

    return jsonify(result), 201


@medical_bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_records():
    claims = get_jwt()

    if claims.get("role") != "patient":
        return jsonify({"error": "Unauthorized"}), 403

    patient_id = int(get_jwt_identity())

    records = get_patient_records(patient_id)

    return jsonify({"records": records}), 200
