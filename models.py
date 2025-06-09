from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
import enum
import datetime


Base = declarative_base()

class Role(enum.Enum):
    admin = "Admin"
    labtech = "Laborer"
    doctor = "Doctor"
    patient = "Patient"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    pw_hash = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    birthdate = Column(DateTime)
    is_approved = Column(Boolean, default=False)
 
class PatientDoctorLink(Base):
    __tablename__ = "patient_doctor"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("users.id"))

    patient = relationship("User", foreign_keys=[patient_id])
    doctor = relationship("User", foreign_keys=[doctor_id])

class LabTest(Base):
    __tablename__ = "lab_tests"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    unit = Column(String, nullable=False)
    ref_min = Column(Float, nullable=False)
    ref_max = Column(Float, nullable=False)

class LabOrder(Base):
    __tablename__ = "lab_orders"
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    patient_id = Column(Integer, ForeignKey("users.id"))
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    priority = Column(String, default="normal")
    notes = Column(String)
    status = Column(String, default="pending") 

    doctor = relationship("User", foreign_keys=[doctor_id])
    patient = relationship("User", foreign_keys=[patient_id])
    items = relationship("LabOrderItem", back_populates="order")

class LabOrderItem(Base):
    __tablename__ = "lab_order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("lab_orders.id"))
    test_id = Column(Integer, ForeignKey("lab_tests.id"))
    result_value = Column(Float) 
    liw_flag = Column(String)

    order = relationship("LabOrder", back_populates="items")
    test = relationship("LabTest")

