from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.services.billing_service import pay_invoice
from backend.utils.db import get_db_session
from backend.models.invoice import Invoice


invoice_bp = Blueprint("invoice", __name__, url_prefix="/api/invoices")


@invoice_bp.route("", methods=["GET"])
@jwt_required()
def get_all_invoices():
    session = get_db_session()
    try:
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"error": "Only admin can view all invoices"}), 403

        invoices = session.query(Invoice).order_by(Invoice.created_at.desc()).all()

        return jsonify(
            {
                "count": len(invoices),
                "invoices": [
                    {
                        "invoice_id": inv.id,
                        "appointment_id": inv.appointment_id,
                        "total_amount": inv.total_amount,
                        "status": inv.status,
                        "created_at": inv.created_at,
                        "paid_at": inv.paid_at,
                    }
                    for inv in invoices
                ],
            }
        ), 200
    finally:
        session.close()


@invoice_bp.route("/pay/<int:invoice_id>", methods=["PUT"])
@jwt_required()
def pay_invoice_endpoint(invoice_id):
    session = get_db_session()
    try:
        user_id = int(get_jwt_identity())
        claims = get_jwt()

        invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()

        if not invoice:
            return jsonify({"error": "Invoice not found"}), 404

        if claims.get("role") != "admin" and invoice.patient_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403

        result = pay_invoice(invoice_id)
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
    finally:
        session.close()


@invoice_bp.route("/<int:invoice_id>", methods=["GET"])
@jwt_required()
def get_invoice(invoice_id):
    session = get_db_session()
    try:
        invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()

        if not invoice:
            return jsonify({"error": "Invoice not found"}), 404

        return jsonify(
            {
                "id": invoice.id,
                "appointment_id": invoice.appointment_id,
                "patient_id": invoice.patient_id,
                "doctor_id": invoice.doctor_id,
                "consultation_fee": invoice.consultation_fee,
                "tax_amount": invoice.tax_amount,
                "total_amount": invoice.total_amount,
                "status": invoice.status,
                "created_at": invoice.created_at,
                "paid_at": invoice.paid_at,
            }
        ), 200

    finally:
        session.close()


@invoice_bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_invoices():
    session = get_db_session()
    try:
        user_id = int(get_jwt_identity())
        claims = get_jwt()

        if claims.get("role") != "patient":
            return jsonify({"error": "Only patients can view invoices"}), 403

        invoices = (
            session.query(Invoice)
            .filter(Invoice.patient_id == user_id)
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
                        "created_at": inv.created_at,
                        "paid_at": inv.paid_at,
                    }
                    for inv in invoices
                ],
            }
        ), 200

    finally:
        session.close()
