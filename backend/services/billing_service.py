from models.invoice import Invoice
from utils.db import get_db_session
from datetime import datetime

DEFAULT_CONSULTATION_FEE = 500.0
TAX_PERCENTAGE = 0.18


def create_invoice_for_appointment(appointment):
    session = get_db_session()
    try:
        consultation_fee = DEFAULT_CONSULTATION_FEE
        tax_amount = consultation_fee * TAX_PERCENTAGE
        total_amount = consultation_fee + tax_amount

        invoice = Invoice(
            appointment_id=appointment.id,
            patient_id=appointment.patient_id,
            doctor_id=appointment.doctor_id,
            consultation_fee=consultation_fee,
            tax_amount=tax_amount,
            total_amount=total_amount,
            status="pending"
        )

        session.add(invoice)
        session.commit()
        session.refresh(invoice)

        return invoice

    finally:
        session.close()


def pay_invoice(invoice_id):
    session = get_db_session()
    try:
        invoice = (
            session.query(Invoice)
            .filter(Invoice.id == invoice_id)
            .with_for_update()
            .first()
        )

        if not invoice:
            raise ValueError("Invoice not found")

        if invoice.status == "paid":
            raise ValueError("Invoice already paid")

        invoice.status = "paid"
        invoice.paid_at = datetime.utcnow()

        session.commit()

        return {
            "invoice_id": invoice.id,
            "status": invoice.status,
            "paid_at": invoice.paid_at
        }

    finally:
        session.close()