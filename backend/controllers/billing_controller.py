from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# payment handled via invoice_controller
from backend.utils.db import get_db_session
from backend.models.invoice import Invoice

billing_bp = Blueprint("billing", __name__, url_prefix="/api/billing")


# ---------------------------------------------
# Get My Invoices
# GET /api/billing/my
# ---------------------------------------------
@billing_bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_invoices():
    session = get_db_session()
    try:
        patient_id = int(get_jwt_identity())

        invoices = (
            session.query(Invoice)
            .filter(Invoice.patient_id == patient_id)
            .order_by(Invoice.created_at.desc())
            .all()
        )

        return jsonify(
            {
                "count": len(invoices),
                "invoices": [
                    {
                        "invoice_id": inv.id,
                        "appointment_id": inv.appointment_id,
                        "total_amount": inv.total_amount,
                        "status": inv.status,
                    }
                    for inv in invoices
                ],
            }
        ), 200

    finally:
        session.close()
