from flask import Blueprint, jsonify

report_bp = Blueprint("report", __name__)

@report_bp.route("/", methods=["GET"])
def report_home():
    return jsonify({
        "message": "Report module working"
    }), 200