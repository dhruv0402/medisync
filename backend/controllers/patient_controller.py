from flask import Blueprint, jsonify

patient_bp = Blueprint("patient", __name__)

@patient_bp.route("/", methods=["GET"])
def patient_home():
    return jsonify({
        "message": "Patient module working"
    }), 200