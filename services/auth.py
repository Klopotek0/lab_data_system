import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import bcrypt
from models import User, Role
from database import Session

def authenticate(login: str, password: str):
    session = Session()
    user = session.query(User).filter_by(login=login).first()
    if user and bcrypt.checkpw(password.encode(), user.pw_hash.encode()):
        if user.role != Role.patient and not user.is_approved:
            session.close()
            return None
        session.expunge(user)
        session.close()
        return user
    session.close()
    return None

def register_user(login, password, first_name, last_name, birthdate, role):
    session = Session()
    if session.query(User).filter_by(login=login).first():
        session.close()
        return None
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    approved = True if role == Role.patient else False
    user = User(
        login=login,
        pw_hash=pw_hash,
        first_name=first_name,
        last_name=last_name,
        birthdate=birthdate,
        role=role,
        is_approved=approved
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return user

def get_unapproved_users():
    session = Session()
    users = session.query(User).filter_by(is_approved=False).all()
    session.close()
    return users

def approve_user(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.is_approved = True
        session.commit()
    session.close()