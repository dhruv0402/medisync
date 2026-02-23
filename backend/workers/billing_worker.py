import json
import redis
import time

from utils.db import get_db_session
from models.appointment import Appointment
from models.invoice import Invoice
from services.billing_service import create_invoice_for_appointment
from utils.db import engine
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

BILLING_QUEUE = "billing_queue"


def process_job(job_data):
    session = get_db_session()
    try:
        appointment_id = job_data["appointment_id"]

        # Start transactional boundary
        with session.begin():

            appointment = session.query(Appointment).filter(
                Appointment.id == appointment_id
            ).first()

            if not appointment:
                return

            # Idempotency check
            existing_invoice = session.query(Invoice).filter(
                Invoice.appointment_id == appointment_id
            ).first()

            if existing_invoice:
                return

            create_invoice_for_appointment(
                session=session,
                appointment=appointment
            )

        print(f"✅ Invoice created for appointment {appointment_id}")

    except Exception as e:
        print("❌ Billing error:", str(e))
        session.rollback()
    finally:
        session.close()


def start_worker():
    print("🚀 Billing worker started...")
    while True:
        _, job = redis_client.blpop(BILLING_QUEUE)
        job_data = json.loads(job)
        process_job(job_data)


if __name__ == "__main__":
    start_worker()