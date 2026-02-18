from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from datetime import datetime, timedelta
from models.availability_slot import AvailabilitySlot
from models.doctor import Doctor
from utils.db import get_db_session


# -----------------------------------------
# Create Single Slot (With Overlap Protection)
# -----------------------------------------
def create_slot_service(doctor_id, date, start_time, end_time):
    session = get_db_session()

    try:
        doctor_id = int(doctor_id)

        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        start_obj = datetime.strptime(start_time, "%H:%M").time()
        end_obj = datetime.strptime(end_time, "%H:%M").time()

        if start_obj >= end_obj:
            raise ValueError("End time must be after start time")

        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise ValueError("Doctor not found")

        overlap = session.query(AvailabilitySlot).filter(
            AvailabilitySlot.doctor_id == doctor_id,
            AvailabilitySlot.date == date_obj,
            and_(
                AvailabilitySlot.start_time < end_obj,
                AvailabilitySlot.end_time > start_obj
            )
        ).first()

        if overlap:
            raise ValueError("Slot overlaps with existing slot")

        new_slot = AvailabilitySlot(
            doctor_id=doctor_id,
            date=date_obj,
            start_time=start_obj,
            end_time=end_obj,
            is_booked=False
        )

        session.add(new_slot)
        session.commit()
        session.refresh(new_slot)

        return {
            "slot_id": new_slot.id,
            "doctor_id": doctor_id,
            "date": str(date_obj),
            "start_time": str(start_obj),
            "end_time": str(end_obj),
            "is_booked": False
        }

    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


# -----------------------------------------
# Bulk Slot Creation (Auto Interval Generator)
# -----------------------------------------
def create_bulk_slots_service(
    doctor_id,
    date,
    start_time,
    end_time,
    slot_duration_minutes
):
    session = get_db_session()

    try:
        doctor_id = int(doctor_id)
        slot_duration_minutes = int(slot_duration_minutes)

        if slot_duration_minutes <= 0:
            raise ValueError("Slot duration must be greater than 0")

        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        start_datetime = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

        if start_datetime >= end_datetime:
            raise ValueError("End time must be after start time")

        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise ValueError("Doctor not found")

        current_time = start_datetime
        created_slots = []

        while current_time < end_datetime:
            next_time = current_time + timedelta(minutes=slot_duration_minutes)

            if next_time > end_datetime:
                break

            overlap = session.query(AvailabilitySlot).filter(
                AvailabilitySlot.doctor_id == doctor_id,
                AvailabilitySlot.date == date_obj,
                and_(
                    AvailabilitySlot.start_time < next_time.time(),
                    AvailabilitySlot.end_time > current_time.time()
                )
            ).first()

            if not overlap:
                slot = AvailabilitySlot(
                    doctor_id=doctor_id,
                    date=date_obj,
                    start_time=current_time.time(),
                    end_time=next_time.time(),
                    is_booked=False
                )
                session.add(slot)

                created_slots.append({
                    "start_time": str(current_time.time()),
                    "end_time": str(next_time.time())
                })

            current_time = next_time

        session.commit()

        return {
            "doctor_id": doctor_id,
            "date": str(date_obj),
            "slots_created": created_slots
        }

    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


# -----------------------------------------
# Weekly Slot Generator
# -----------------------------------------
def create_weekly_slots_service(
    doctor_id,
    weekday,
    number_of_weeks,
    start_time,
    end_time,
    slot_duration_minutes
):
    """
    weekday: 0=Monday ... 6=Sunday
    """

    session = get_db_session()

    try:
        doctor_id = int(doctor_id)
        weekday = int(weekday)
        number_of_weeks = int(number_of_weeks)
        slot_duration_minutes = int(slot_duration_minutes)

        if weekday < 0 or weekday > 6:
            raise ValueError("Weekday must be between 0 (Mon) and 6 (Sun)")

        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise ValueError("Doctor not found")

        today = datetime.today().date()
        days_ahead = (weekday - today.weekday() + 7) % 7
        first_date = today + timedelta(days=days_ahead)

        created_summary = []

        for week in range(number_of_weeks):
            current_date = first_date + timedelta(weeks=week)

            start_datetime = datetime.strptime(
                f"{current_date} {start_time}", "%Y-%m-%d %H:%M"
            )
            end_datetime = datetime.strptime(
                f"{current_date} {end_time}", "%Y-%m-%d %H:%M"
            )

            current_time = start_datetime

            while current_time < end_datetime:
                next_time = current_time + timedelta(minutes=slot_duration_minutes)

                if next_time > end_datetime:
                    break

                overlap = session.query(AvailabilitySlot).filter(
                    AvailabilitySlot.doctor_id == doctor_id,
                    AvailabilitySlot.date == current_date,
                    and_(
                        AvailabilitySlot.start_time < next_time.time(),
                        AvailabilitySlot.end_time > current_time.time()
                    )
                ).first()

                if not overlap:
                    slot = AvailabilitySlot(
                        doctor_id=doctor_id,
                        date=current_date,
                        start_time=current_time.time(),
                        end_time=next_time.time(),
                        is_booked=False
                    )
                    session.add(slot)

                current_time = next_time

            created_summary.append(str(current_date))

        session.commit()

        return {
            "doctor_id": doctor_id,
            "weekday": weekday,
            "weeks_created": number_of_weeks,
            "dates_generated": created_summary
        }

    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()