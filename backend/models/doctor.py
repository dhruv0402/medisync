from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from backend.models.base import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # ✅ THIS WAS MISSING
    department_id = Column(Integer, ForeignKey("departments.id"))

    specialization = Column(String(100))
    consultation_fee = Column(Integer)

    user = relationship("User")
    department = relationship("Department")
    appointments = relationship("Appointment", back_populates="doctor")
    slots = relationship("AvailabilitySlot", back_populates="doctor")
