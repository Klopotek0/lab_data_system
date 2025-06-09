from models import PatientDoctorLink, User, Role
from database import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload

def get_all_doctors():
    session = Session()
    doctors = session.query(User).filter_by(role=Role.doctor, is_approved=True).all()
    session.close()
    return doctors

def get_unassigned_patients():
    session = Session()
    subquery = select(PatientDoctorLink.patient_id)
    patients = session.query(User).filter_by(role=Role.patient, is_approved=True)\
    .filter(~User.id.in_(subquery)).all()
    session.close()
    return patients

def assign_patient_to_doctor(patient_id, doctor_id):
    session = Session()
    assignment = PatientDoctorLink(patient_id=patient_id, doctor_id=doctor_id)
    session.add(assignment)
    session.commit()
    session.close()

def get_doctor_for_patient(patient_id):
    session = Session()
    link = session.query(PatientDoctorLink).filter_by(patient_id=patient_id).first()
    doctor = session.query(User).filter_by(id=link.doctor_id).first() if link else None
    session.close()
    return doctor

def get_patients_for_doctor(doctor_id):
    session = Session()
    links = session.query(PatientDoctorLink).filter_by(doctor_id=doctor_id).all()
    patient_ids = [link.patient_id for link in links]
    patients = session.query(User).filter(User.id.in_(patient_ids)).all()
    session.close()
    return patients

def get_patient_doctor_assignments():
    session = Session()
    results = (
        session.query(PatientDoctorLink)
        .options(joinedload(PatientDoctorLink.patient), joinedload(PatientDoctorLink.doctor))
        .all()
    )
    assignments = [(link.patient, link.doctor) for link in results]
    return assignments

def reassign_patient(patient_id, new_doctor_id):
    session = Session()
    assignment = session.query(PatientDoctorLink).filter_by(patient_id=patient_id).first()
    if assignment:
        assignment.doctor_id = new_doctor_id
    else:
        # jeśli nie ma – utwórz nową relację
        new_link = PatientDoctorLink(patient_id=patient_id, doctor_id=new_doctor_id)
        session.add(new_link)
    session.commit()
