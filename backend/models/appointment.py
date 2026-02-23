from sqlalchemy import Column, Integer, Date, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    slot_id = Column(Integer, ForeignKey("availability_slots.id"), nullable=False)

    appointment_date = Column(Date, nullable=False)
    status = Column(String(50), default="scheduled")

    created_at = Column(DateTime, default=datetime.utcnow)

    # ----------------------------
    # Relationships
    # ----------------------------
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("User")
    slot = relationship("AvailabilitySlot",back_populates="appointment")