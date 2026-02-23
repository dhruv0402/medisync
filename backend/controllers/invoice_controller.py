from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.billing_service import pay_invoice
from utils.db import get_db_session
from models.invoice import Invoice


invoice_bp = Blueprint("invoice", __name__, url_prefix="/api/invoices")


@invoice_bp.route("/pay/<int:invoice_id>", methods=["PUT"])
@jwt_required()
def pay_invoice_endpoint(invoice_id):
    try:
        result = pay_invoice(invoice_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@invoice_bp.route("/<int:invoice_id>", methods=["GET"])
@jwt_required()
def get_invoice(invoice_id):
    session = get_db_session()
    try:
        invoice = session.query(Invoice).filter(
            Invoice.id == invoice_id
        ).first()

        if not invoice:
            return jsonify({"error": "Invoice not found"}), 404

        return jsonify({
            "id": invoice.id,
            "appointment_id": invoice.appointment_id,
            "patient_id": invoice.patient_id,
            "doctor_id": invoice.doctor_id,
            "consultation_fee": invoice.consultation_fee,
            "tax_amount": invoice.tax_amount,
            "total_amount": invoice.total_amount,
            "status": invoice.status,
            "created_at": invoice.created_at,
            "paid_at": invoice.paid_at
        }), 200

    finally:
        session.close()


@invoice_bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_invoices():
    from flask_jwt_extended import get_jwt_identity, get_jwt
    from models.invoice import Invoice
    from utils.db import get_db_session

    session = get_db_session()
    try:
        user_id = int(get_jwt_identity())
        claims = get_jwt()

        if claims.get("role") != "patient":
            return jsonify({"error": "Only patients can view invoices"}), 403

        invoices = session.query(Invoice).filter(
            Invoice.patient_id == user_id
        ).order_by(Invoice.created_at.desc()).all()

        return jsonify({
            "count": len(invoices),
            "invoices": [
                {
                    "invoice_id": inv.id,
                    "appointment_id": inv.appointment_id,
                    "total_amount": inv.total_amount,
                    "status": inv.status,
                    "created_at": inv.created_at,
                    "paid_at": inv.paid_at
                }
                for inv in invoices
            ]
        }), 200

    finally:
        session.close()