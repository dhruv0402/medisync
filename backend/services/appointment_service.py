from backend.utils.db import get_db_session
from backend.models.appointment import Appointment
from sqlalchemy.orm import joinedload
from datetime import datetime, timezone


def get_doctor_appointments_service(doctor_id, status=None):
    session = get_db_session()

    try:
        if not isinstance(doctor_id, int):
            raise ValueError("Invalid doctor_id")

        query = (
            session.query(Appointment)
            .options(
                joinedload(Appointment.slot),
                joinedload(Appointment.patient),
            )
            .filter(Appointment.doctor_id == doctor_id)
        )

        if status:
            allowed = {"booked", "completed", "cancelled"}
            if status not in allowed:
                raise ValueError("Invalid status filter")
            query = query.filter(Appointment.status == status)

        appointments = query.order_by(Appointment.appointment_date.desc()).all()

        result = []
        now = datetime.now(timezone.utc)

        for a in appointments:
            slot = a.slot

            # Safety check (avoid NoneType crash)
            if not slot:
                continue

            # Safe datetime handling
            try:
                slot_datetime = datetime.combine(slot.date, slot.start_time).replace(
                    tzinfo=timezone.utc
                )
            except Exception:
                slot_datetime = None

            result.append(
                {
                    "appointment_id": a.id,
                    "status": a.status,
                    "date": str(slot.date) if slot.date else None,
                    "start_time": str(slot.start_time) if slot.start_time else None,
                    "end_time": str(slot.end_time) if slot.end_time else None,
                    "patient_name": a.patient.name if a.patient else None,
                    "is_upcoming": slot_datetime >= now if slot_datetime else False,
                }
            )

        return result

    except Exception as e:
        print("DOCTOR APPOINTMENTS ERROR:", str(e))
        raise

    finally:
        session.close()
