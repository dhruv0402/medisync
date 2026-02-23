from sqlalchemy import Column, Integer, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class AvailabilitySlot(Base):
    __tablename__ = "availability_slots"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    is_booked = Column(Boolean, default=False)

    # ----------------------------
    # Relationships
    # ----------------------------
    doctor = relationship("Doctor", back_populates="slots")
    appointment = relationship("Appointment", back_populates="slot", uselist=False)