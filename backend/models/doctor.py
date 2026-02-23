from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    # Relationships
    department = relationship("Department", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete")
    slots = relationship("AvailabilitySlot", back_populates="doctor", cascade="all, delete")