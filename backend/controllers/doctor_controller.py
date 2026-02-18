from flask import Blueprint, jsonify

doctor_bp = Blueprint("doctor", __name__)

@doctor_bp.route("/", methods=["GET"])
def doctor_home():
    return jsonify({
        "message": "Doctor module working"
    }), 200