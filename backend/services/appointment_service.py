from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from models.doctor import Doctor
from models.availability_slot import AvailabilitySlot
from models.appointment import Appointment
from utils.db import get_db_session


# -------------------------------------------------
# Get Doctors by Department
# -------------------------------------------------
def get_doctors_by_department(department_id):
    session = get_db_session()
    try:
        doctors = (
            session.query(Doctor)
            .filter(Doctor.department_id == department_id)
            .all()
        )

        return [
            {
                "id": doctor.id,
                "name": doctor.name,
                "specialization": doctor.specialization
            }
            for doctor in doctors
        ]

    finally:
        session.close()


# -------------------------------------------------
# Get Available Slots
# -------------------------------------------------
def get_available_slots(doctor_id, date):
    session = get_db_session()
    try:
        slots = (
            session.query(AvailabilitySlot)
            .filter(
                AvailabilitySlot.doctor_id == doctor_id,
                AvailabilitySlot.date == date,
                AvailabilitySlot.is_booked == False
            )
            .order_by(AvailabilitySlot.start_time)
            .all()
        )

        return [
            {
                "slot_id": slot.id,
                "start_time": slot.start_time.strftime("%H:%M"),
                "end_time": slot.end_time.strftime("%H:%M")
            }
            for slot in slots
        ]

    finally:
        session.close()


# -------------------------------------------------
# Book Appointment (Improved + Safe)
# -------------------------------------------------
def book_appointment_service(patient_id, doctor_id, slot_id, appointment_date):
    session = get_db_session()

    try:
        # Validate doctor exists
        doctor = session.query(Doctor).filter(
            Doctor.id == doctor_id
        ).first()

        if not doctor:
            raise ValueError("Doctor not found")

        # Lock slot row (prevents race condition)
        slot = (
            session.query(AvailabilitySlot)
            .filter(
                AvailabilitySlot.id == slot_id,
                AvailabilitySlot.doctor_id == doctor_id
            )
            .with_for_update()  # 🔥 row-level locking
            .first()
        )

        if not slot:
            raise ValueError("Slot not found")

        if slot.is_booked:
            raise ValueError("Selected slot is already booked")

        # Ensure slot date matches appointment date
        if slot.date != appointment_date:
            raise ValueError("Slot date mismatch")

        new_appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            slot_id=slot_id,
            appointment_date=appointment_date,
            status="scheduled"
        )

        session.add(new_appointment)

        # Mark slot as booked
        slot.is_booked = True

        session.commit()
        session.refresh(new_appointment)

        return {
            "appointment_id": new_appointment.id,
            "doctor_id": doctor_id,
            "slot_id": slot_id,
            "status": new_appointment.status
        }

    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        raise e

    finally:
        session.close()


# -------------------------------------------------
# Cancel Appointment (Improved)
# -------------------------------------------------
def cancel_appointment_service(appointment_id, patient_id):
    session = get_db_session()

    try:
        appointment = (
            session.query(Appointment)
            .options(joinedload(Appointment))
            .filter(
                Appointment.id == appointment_id,
                Appointment.patient_id == patient_id
            )
            .first()
        )

        if not appointment:
            raise ValueError("Appointment not found")

        if appointment.status == "cancelled":
            raise ValueError("Appointment already cancelled")

        # Lock slot
        slot = (
            session.query(AvailabilitySlot)
            .filter(AvailabilitySlot.id == appointment.slot_id)
            .with_for_update()
            .first()
        )

        if slot:
            slot.is_booked = False

        appointment.status = "cancelled"

        session.commit()

        return {
            "message": "Appointment cancelled successfully"
        }

    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        raise e

    finally:
        session.close()