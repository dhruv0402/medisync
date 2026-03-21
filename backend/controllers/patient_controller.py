from flask import Blueprint, jsonify

patient_bp = Blueprint("patient", __name__, url_prefix="/api/patient")


@patient_bp.route("/", methods=["GET"])
def patient_home():
    return jsonify({"message": "Patient module working"}), 200
