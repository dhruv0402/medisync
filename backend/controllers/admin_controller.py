from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.admin_service import get_dashboard_metrics
from models.user import User
from utils.db import get_db_session

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    session = get_db_session()
    try:
        user_id = get_jwt_identity()
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.role != "admin":
            return jsonify({"error": "Forbidden: Admin access required"}), 403

    finally:
        session.close()

    # Call service AFTER closing auth session (clean separation of concerns)
    try:
        metrics = get_dashboard_metrics()
        return jsonify(metrics), 200
    except Exception:
        return jsonify({"error": "Internal server error"}), 500