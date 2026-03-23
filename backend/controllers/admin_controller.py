from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.services.admin_service import get_dashboard_metrics
from backend.models.user import User
from backend.utils.db import get_db_session

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


# ---------------------------------------
# Admin: Appointment Stats
# GET /api/admin/appointments/stats
# ---------------------------------------
@admin_bp.route("/appointments/stats", methods=["GET"])
@jwt_required()
def appointment_stats():
    from backend.models.appointment import Appointment
    from backend.utils.db import get_db_session

    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    session = get_db_session()
    try:
        booked = (
            session.query(Appointment).filter(Appointment.status == "booked").count()
        )
        completed = (
            session.query(Appointment).filter(Appointment.status == "completed").count()
        )
        cancelled = (
            session.query(Appointment).filter(Appointment.status == "cancelled").count()
        )

        return jsonify(
            {"booked": booked, "completed": completed, "cancelled": cancelled}
        ), 200
    finally:
        session.close()


# ---------------------------------------
# Admin: Revenue
# GET /api/admin/revenue
# ---------------------------------------
@admin_bp.route("/revenue", methods=["GET"])
@jwt_required()
def revenue():
    from backend.models.invoice import Invoice
    from sqlalchemy import func
    from backend.utils.db import get_db_session

    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    session = get_db_session()
    try:
        total = (
            session.query(func.sum(Invoice.total_amount))
            .filter(Invoice.status == "paid")
            .scalar()
        )
        refunded = (
            session.query(func.sum(Invoice.total_amount))
            .filter(Invoice.status == "refunded")
            .scalar()
        )

        return jsonify(
            {"total_revenue": float(total or 0), "total_refunded": float(refunded or 0)}
        ), 200
    finally:
        session.close()


# ---------------------------------------
# Admin: Top Doctors
# GET /api/admin/top-doctors
# ---------------------------------------
@admin_bp.route("/top-doctors", methods=["GET"])
@jwt_required()
def top_doctors():
    from backend.models.appointment import Appointment
    from sqlalchemy import func
    from backend.utils.db import get_db_session

    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    session = get_db_session()
    try:
        result = (
            session.query(
                Appointment.doctor_id, func.count(Appointment.id).label("total")
            )
            .filter(Appointment.status == "completed")
            .group_by(Appointment.doctor_id)
            .order_by(func.count(Appointment.id).desc())
            .limit(5)
            .all()
        )

        return jsonify(
            [{"doctor_id": r[0], "completed_appointments": r[1]} for r in result]
        ), 200
    finally:
        session.close()


# ---------------------------------------
# Admin: Payments
# GET /api/admin/payments
# ---------------------------------------
@admin_bp.route("/payments", methods=["GET"])
@jwt_required()
def payments():
    from backend.models.payment import Payment
    from backend.utils.db import get_db_session

    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    session = get_db_session()
    try:
        payments = session.query(Payment).all()

        return jsonify(
            [
                {
                    "payment_id": p.id,
                    "invoice_id": p.invoice_id,
                    "amount": p.amount,
                    "method": p.payment_method,
                    "paid_at": p.paid_at,
                }
                for p in payments
            ]
        ), 200
    finally:
        session.close()
