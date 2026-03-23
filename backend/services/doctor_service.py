from sqlalchemy.exc import SQLAlchemyError
from backend.models.doctor import Doctor
from backend.models.department import Department
from backend.utils.db import get_db_session


# ---------------------------------------
# Create Doctor
# ---------------------------------------
def create_doctor_service(name, specialization, department_id):
    session = get_db_session()

    try:
        # Validate department exists
        department = (
            session.query(Department).filter(Department.id == department_id).first()
        )

        if not department:
            raise ValueError("Department not found")

        doctor = Doctor(
            user_id=name,  # TEMP: expecting caller to pass user_id instead of name
            specialization=specialization,
            department_id=department_id,
        )

        session.add(doctor)
        session.commit()
        session.refresh(doctor)

        return {
            "id": doctor.id,
            "name": doctor.user.name if doctor.user else None,
            "specialization": doctor.specialization,
            "department_id": doctor.department_id,
        }

    except SQLAlchemyError:
        session.rollback()
        raise

    finally:
        session.close()


# ---------------------------------------
# Get All Doctors
# ---------------------------------------
def get_all_doctors_service():
    session = get_db_session()

    try:
        doctors = session.query(Doctor).all()
        print("Fetched doctors:", doctors)

        return [
            {
                "id": d.id,
                "name": d.user.name if d.user else None,
                "specialization": d.specialization,
                "department_id": d.department_id,
            }
            for d in doctors
        ]

    finally:
        session.close()


# ---------------------------------------
# Get Doctors By Department
# ---------------------------------------
def get_doctors_by_department_service(department_id):
    session = get_db_session()

    try:
        doctors = (
            session.query(Doctor).filter(Doctor.department_id == department_id).all()
        )

        return [
            {
                "id": d.id,
                "name": d.user.name if d.user else None,
                "specialization": d.specialization,
            }
            for d in doctors
        ]

    finally:
        session.close()


# ---------------------------------------
# Get Doctor By ID
# ---------------------------------------
def get_doctor_by_id_service(doctor_id):
    session = get_db_session()

    try:
        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()

        if not doctor:
            raise ValueError("Doctor not found")

        return {
            "id": doctor.id,
            "name": doctor.user.name if doctor.user else None,
            "specialization": doctor.specialization,
            "department_id": doctor.department_id,
        }

    finally:
        session.close()
