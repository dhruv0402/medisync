import json
import time
from backend.utils.redis_client import redis_client
from backend.utils.db import get_db_session
from backend.models.appointment import Appointment
from backend.services.billing_service import create_invoice_for_appointment

BILLING_QUEUE = "billing_queue"


def process_job(job_data):
    session = get_db_session()
    try:
        appointment_id = job_data.get("appointment_id")

        if not appointment_id:
            print("❌ Invalid job data:", job_data)
            return

        appointment = session.query(Appointment).get(appointment_id)

        if not appointment:
            print(f"❌ Appointment not found: {appointment_id}")
            return

        create_invoice_for_appointment(session, appointment)
        session.commit()

        print(f"✅ Invoice created for appointment {appointment_id}")

    except Exception as e:
        session.rollback()
        print(f"❌ Worker error: {str(e)}")

    finally:
        session.close()


def start_worker():
    print("🚀 Billing worker started...")

    while True:
        try:
            result = redis_client.blpop(BILLING_QUEUE, timeout=5)

            if result:
                _, job_json = result
                job_data = json.loads(job_json)

                process_job(job_data)

        except Exception as e:
            print(f"❌ Worker error: {str(e)}")
            time.sleep(1)


if __name__ == "__main__":
    start_worker()
