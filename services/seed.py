import bcrypt
from models import User, Role
from database import Session

def ensure_premade_users():
    session = Session()
    users = [
        {"login": "admin", "password": "admin", "role": Role.admin},
        {"login": "doctor", "password": "doctor123", "role": Role.doctor},
    ]
    for data in users:
        if not session.query(User).filter_by(login=data["login"]).first():
            pw_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
            user = User(
                login=data["login"],
                pw_hash=pw_hash,
                role=data["role"],
                is_approved=True
            )
            session.add(user)
    session.commit()
    session.close()
