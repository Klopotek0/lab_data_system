from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.orm import declarative_base
import enum

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
 