from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.billing_service import pay_invoice
from utils.db import get_db_session
from models.invoice import Invoice

billing_bp = Blueprint("billing", __name__)


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

        invoices = session.query(Invoice).filter(
            Invoice.patient_id == patient_id
        ).order_by(Invoice.created_at.desc()).all()

        return jsonify({
            "count": len(invoices),
            "invoices": [
                {
                    "invoice_id": inv.id,
                    "appointment_id": inv.appointment_id,
                    "total_amount": inv.total_amount,
                    "status": inv.status
                }
                for inv in invoices
            ]
        }), 200

    finally:
        session.close()


# ---------------------------------------------
# Pay Invoice
# POST /api/billing/pay/<invoice_id>
# ---------------------------------------------
@billing_bp.route("/pay/<int:invoice_id>", methods=["POST"])
@jwt_required()
def pay(invoice_id):
    try:
        result = pay_invoice(invoice_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400