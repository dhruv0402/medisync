from sqlalchemy import Column, Integer, Date, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.models.base import Base
from sqlalchemy import Enum
from sqlalchemy import UniqueConstraint


class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (UniqueConstraint("slot_id", name="uq_slot_booking"),)
    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    slot_id = Column(Integer, ForeignKey("availability_slots.id"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    status = Column(Enum("booked", "cancelled", "completed"), default="booked")
    created_at = Column(DateTime, default=datetime.utcnow)

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("User")
    slot = relationship("AvailabilitySlot", back_populates="appointment")
