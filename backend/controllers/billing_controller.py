from flask import Blueprint, jsonify

billing_bp = Blueprint("billing", __name__)

@billing_bp.route("/", methods=["GET"])
def billing_home():
    return jsonify({
        "message": "Billing module working"
    }), 200