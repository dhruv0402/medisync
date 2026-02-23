from sqlalchemy import func
from models.invoice import Invoice
from models.appointment import Appointment
from models.doctor import Doctor
from utils.db import get_db_session
from datetime import date


def get_dashboard_metrics():
    session = get_db_session()
    try:
        total_revenue = session.query(
            func.coalesce(func.sum(Invoice.total_amount), 0)
        ).filter(
            Invoice.status == "paid"
        ).scalar()

        today_revenue = session.query(
            func.coalesce(func.sum(Invoice.total_amount), 0)
        ).filter(
            Invoice.status == "paid",
            func.date(Invoice.paid_at) == date.today()
        ).scalar()

        pending_invoices = session.query(
            func.count(Invoice.id)
        ).filter(
            Invoice.status == "pending"
        ).scalar()

        total_appointments = session.query(
            func.count(Appointment.id)
        ).scalar()

        completed_appointments = session.query(
            func.count(Appointment.id)
        ).filter(
            Appointment.status == "completed"
        ).scalar()

        revenue_label = func.sum(Invoice.total_amount).label("revenue")

        top_doctor = session.query(
            Doctor.name,
            revenue_label
        ).join(
            Invoice, Invoice.doctor_id == Doctor.id
        ).filter(
            Invoice.status == "paid"
        ).group_by(
            Doctor.id
        ).order_by(
            revenue_label.desc()
        ).first()

        return {
            "total_revenue": float(total_revenue),
            "today_revenue": float(today_revenue),
            "pending_invoices": pending_invoices,
            "total_appointments": total_appointments,
            "completed_appointments": completed_appointments,
            "top_doctor": {
                "name": top_doctor[0],
                "revenue": float(top_doctor[1])
            } if top_doctor else None
        }

    finally:
        session.close()