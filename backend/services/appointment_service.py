from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from models.doctor import Doctor
from models.availability_slot import AvailabilitySlot
from models.appointment import Appointment
from models.doctor_schedule import DoctorSchedule
from utils.db import get_db_session

from datetime import date as dt_date
from datetime import datetime, timedelta
from services.billing_queue import enqueue_billing_job
from models.invoice import Invoice
import redis
import os

# -------------------------------------------------
# Redis Configuration (Distributed Locking)
# -------------------------------------------------
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

LOCK_EXPIRY_SECONDS = 10
CANCELLATION_WINDOW_HOURS = 2


# -------------------------------------------------
# Utility: Billing Trigger Stub
# -------------------------------------------------
def trigger_billing(appointment):
    """
    Stub for billing integration.
    Replace with actual payment gateway / invoice creation logic.
    """
    print(f"💰 Billing triggered for appointment {appointment.id}")


# -------------------------------------------------
# Get Doctors by Department
# -------------------------------------------------
def get_doctors_by_department(department_id):
    session = get_db_session()
    try:
        if not isinstance(department_id, int):
            raise ValueError("Invalid department_id")

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
# Slot Generation
# -------------------------------------------------
def generate_slots_for_date(session, doctor_id, date):
    day_of_week = date.weekday()

    schedule = (
        session.query(DoctorSchedule)
        .filter(
            DoctorSchedule.doctor_id == doctor_id,
            DoctorSchedule.day_of_week == day_of_week
        )
        .first()
    )

    if not schedule:
        return

    existing = session.query(AvailabilitySlot).filter(
        AvailabilitySlot.doctor_id == doctor_id,
        AvailabilitySlot.date == date
    ).first()

    if existing:
        return

    start = datetime.combine(date, schedule.start_time)
    end = datetime.combine(date, schedule.end_time)
    duration = timedelta(minutes=schedule.slot_duration)

    while start + duration <= end:
        session.add(
            AvailabilitySlot(
                doctor_id=doctor_id,
                date=date,
                start_time=start.time(),
                end_time=(start + duration).time(),
                is_booked=False
            )
        )
        start += duration


# -------------------------------------------------
# Get Available Slots
# -------------------------------------------------
def get_available_slots(doctor_id, date):
    session = get_db_session()
    try:
        if date < dt_date.today():
            raise ValueError("Cannot fetch past dates")

        doctor = session.query(Doctor).get(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")

        existing = session.query(AvailabilitySlot).filter(
            AvailabilitySlot.doctor_id == doctor_id,
            AvailabilitySlot.date == date
        ).all()

        if not existing:
            generate_slots_for_date(session, doctor_id, date)
            session.commit()

        slots = session.query(AvailabilitySlot).filter(
            AvailabilitySlot.doctor_id == doctor_id,
            AvailabilitySlot.date == date,
            AvailabilitySlot.is_booked == False
        ).order_by(AvailabilitySlot.start_time).all()

        return [
            {
                "slot_id": s.id,
                "start_time": s.start_time.strftime("%H:%M"),
                "end_time": s.end_time.strftime("%H:%M")
            }
            for s in slots
        ]
    finally:
        session.close()


# -------------------------------------------------
# Book Appointment (Redis + DB Lock Safe)
# -------------------------------------------------
def book_appointment_service(patient_id, doctor_id, slot_id, appointment_date):
    session = get_db_session()
    lock_key = f"lock:doctor:{doctor_id}:date:{appointment_date}:slot:{slot_id}"

    try:
        redis_lock = redis_client.lock(
            lock_key,
            timeout=LOCK_EXPIRY_SECONDS,
            blocking_timeout=3
        )

        if not redis_lock.acquire(blocking=True):
            raise ValueError("Slot is being booked by another user")

        with session.begin():

            if appointment_date < dt_date.today():
                raise ValueError("Cannot book past appointments")

            slot = (
                session.query(AvailabilitySlot)
                .filter(
                    AvailabilitySlot.id == slot_id,
                    AvailabilitySlot.doctor_id == doctor_id
                )
                .with_for_update()
                .first()
            )

            if not slot:
                raise ValueError("Slot not found")

            if slot.is_booked:
                raise ValueError("Slot already booked")

            # Prevent double booking of same slot (only scheduled appointments block it)
            existing_slot_booking = session.query(Appointment).filter(
                Appointment.slot_id == slot_id,
                Appointment.status == "scheduled"
            ).with_for_update().first()

            if existing_slot_booking:
                raise ValueError("Slot already booked")

            existing_active = session.query(Appointment).filter(
                Appointment.patient_id == patient_id,
                Appointment.doctor_id == doctor_id,
                Appointment.status == "scheduled"
            ).first()

            if existing_active:
                raise ValueError("You already have an active appointment with this doctor")

            new_appointment = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                slot_id=slot_id,
                appointment_date=appointment_date,
                status="scheduled"
            )

            session.add(new_appointment)
            slot.is_booked = True

        return {
            "appointment_id": new_appointment.id,
            "status": new_appointment.status
        }

    except Exception as e:
        session.rollback()

        # Gracefully handle duplicate booking race conditions
        if "IntegrityError" in str(type(e)) or "Duplicate entry" in str(e):
            raise ValueError("Slot already booked")

        raise e

    finally:
        try:
            redis_lock.release()
        except Exception:
            pass
        session.close()


# -------------------------------------------------
# Cancel Appointment (2-hour Rule)
# -------------------------------------------------
def cancel_appointment_service(appointment_id, patient_id):
    session = get_db_session()

    try:
        appointment = (
            session.query(Appointment)
            .options(joinedload(Appointment.slot))
            .filter(
                Appointment.id == appointment_id,
                Appointment.patient_id == patient_id
            )
            .with_for_update()
            .first()
        )

        if not appointment:
            raise ValueError("Appointment not found")

        if appointment.status != "scheduled":
            raise ValueError("Only scheduled appointments can be cancelled")

        # Check cancellation window
        slot_datetime = datetime.combine(
            appointment.appointment_date,
            appointment.slot.start_time
        )

        if slot_datetime - datetime.utcnow() < timedelta(hours=CANCELLATION_WINDOW_HOURS):
            raise ValueError("Cannot cancel within 2 hours of appointment time")

        appointment.status = "cancelled"
        appointment.slot.is_booked = False

        session.commit()

        return {"message": "Appointment cancelled"}

    finally:
        session.close()


# -------------------------------------------------
# Complete Appointment + Billing Trigger
# -------------------------------------------------
def complete_appointment_service(appointment_id):
    session = get_db_session()

    try:
        with session.begin():

            appointment = (
                session.query(Appointment)
                .options(joinedload(Appointment.slot))
                .filter(Appointment.id == appointment_id)
                .with_for_update()
                .first()
            )

            if not appointment:
                raise ValueError("Appointment not found")

            # Idempotency
            if appointment.status == "completed":
                return {
                    "appointment_id": appointment.id,
                    "status": appointment.status,
                    "message": "Already completed"
                }

            if appointment.status != "scheduled":
                raise ValueError("Only scheduled appointments can be completed")

            if appointment.appointment_date > dt_date.today():
                raise ValueError("Cannot complete future appointment")

            appointment.status = "completed"
            enqueue_billing_job(appointment.id)

        trigger_billing(appointment)

        return {
            "appointment_id": appointment.id,
            "status": appointment.status,
            "message": "Appointment completed. Billing queued."
        }

    finally:
        session.close()


# -------------------------------------------------
# Get Patient Appointments
# -------------------------------------------------
def get_patient_appointments_service(patient_id, status=None):
    session = get_db_session()

    try:
        query = session.query(Appointment).options(
            joinedload(Appointment.doctor),
            joinedload(Appointment.slot)
        ).filter(Appointment.patient_id == patient_id)

        if status:
            query = query.filter(Appointment.status == status)

        appointments = query.order_by(
            Appointment.appointment_date.desc()
        ).all()

        return [
            {
                "appointment_id": a.id,
                "doctor_name": a.doctor.name if a.doctor else None,
                "appointment_date": a.appointment_date.strftime("%Y-%m-%d"),
                "start_time": a.slot.start_time.strftime("%H:%M") if a.slot else None,
                "status": a.status
            }
            for a in appointments
        ]

    finally:
        session.close()