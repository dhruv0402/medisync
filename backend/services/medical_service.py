from backend.utils.db import get_db_session
from backend.models.medical_record import MedicalRecord


def create_medical_record(
    appointment_id, patient_id, doctor_id, diagnosis, prescription, notes
):
    session = get_db_session()

    try:
        existing = (
            session.query(MedicalRecord)
            .filter(MedicalRecord.appointment_id == appointment_id)
            .first()
        )

        if existing:
            raise ValueError("Medical record already exists")

        record = MedicalRecord(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes,
        )

        session.add(record)
        session.commit()

        return {"message": "Medical record created"}

    finally:
        session.close()


def get_patient_records(patient_id):
    session = get_db_session()

    try:
        records = (
            session.query(MedicalRecord)
            .filter(MedicalRecord.patient_id == patient_id)
            .all()
        )

        return [
            {
                "appointment_id": r.appointment_id,
                "diagnosis": r.diagnosis,
                "prescription": r.prescription,
                "notes": r.notes,
                "created_at": str(r.created_at),
            }
            for r in records
        ]

    finally:
        session.close()
