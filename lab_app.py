#!/usr/bin/env python3
# lab_app.py
# Requirements: PySide6, SQLAlchemy, bcrypt
# Install: pip install PySide6 SQLAlchemy bcrypt

import sys
import datetime
import enum
import bcrypt
from PySide6.QtWidgets import (
    QApplication, QDialog, QMainWindow,
    QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QWidget, QMessageBox, QHBoxLayout
)
from sqlalchemy import (
    create_engine, Column, Integer, String,
    DateTime, Enum, ForeignKey
)
from sqlalchemy.orm import sessionmaker, declarative_base

# ---- Database setup ----
engine = create_engine("sqlite:///lab.db", echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Role(enum.Enum):
    admin = "Administrator"
    labtech = "Laborant"
    doctor = "Lekarz"
    patient = "Pacjent"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    pw_hash = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    __mapper_args__ = {"polymorphic_on": role}

class Patient(User):
    __tablename__ = "patients"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthdate = Column(DateTime, nullable=False)
    __mapper_args__ = {"polymorphic_identity": Role.patient}

class Admin(User):
    __tablename__ = "admins"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": Role.admin}

class Doctor(User):
    __tablename__ = "doctors"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": Role.doctor}

class Labtech(User):
    __tablename__ = "labtechs"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": Role.labtech}

Base.metadata.create_all(engine)

# Ensure default admin and doctor

def ensure_premade_users():
    session = Session()
    users = [
        {"login": "admin", "password": "admin", "class": Admin, "role": Role.admin},
        {"login": "doctor", "password": "doctor123", "class": Doctor, "role": Role.doctor},
    ]
    for data in users:
        if not session.query(User).filter_by(login=data["login"]).first():
            pw_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
            user = data["class"](
                login=data["login"], pw_hash=pw_hash, role=data["role"]
            )
            session.add(user)
    session.commit()
    session.close()

ensure_premade_users()

# ---- Services ----
def authenticate(login: str, password: str):
    session = Session()
    user = session.query(User).filter_by(login=login).first()
    if user and bcrypt.checkpw(password.encode(), user.pw_hash.encode()):
        session.expunge(user)
        session.close()
        return user
    session.close()
    return None

def register_patient(login, password, first_name, last_name, birthdate):
    session = Session()
    if session.query(User).filter_by(login=login).first():
        session.close()
        return None
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    patient = Patient(
        login=login, pw_hash=pw_hash,
        first_name=first_name, last_name=last_name,
        birthdate=birthdate, role=Role.patient
    )
    session.add(patient)
    session.commit()
    session.refresh(patient)
    session.close()
    return patient

# ---- GUI ----

class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Patient")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login")
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Password")
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.birthdate_input = QLineEdit()
        self.birthdate_input.setPlaceholderText("Birthdate YYYY-MM-DD")

        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")

        layout = QVBoxLayout()
        layout.addWidget(self.login_input)
        layout.addWidget(self.pwd_input)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.birthdate_input)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.btn_submit.clicked.connect(self.handle_submit)
        self.btn_cancel.clicked.connect(self.reject)

    def handle_submit(self):
        login = self.login_input.text().strip()
        pwd = self.pwd_input.text().strip()
        first = self.first_name_input.text().strip()
        last = self.last_name_input.text().strip()
        bd_text = self.birthdate_input.text().strip()
        if not all([login, pwd, first, last, bd_text]):
            QMessageBox.warning(self, "Error", "All fields are required")
            return
        try:
            bd = datetime.datetime.strptime(bd_text, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid birthdate format")
            return
        user = register_patient(login, pwd, first, last, bd)
        if user:
            QMessageBox.information(self, "Success", "Registration successful")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "User already exists")

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login")
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Password")
        self.pwd_input.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Login")
        self.btn_register = QPushButton("Register")

        layout = QVBoxLayout()
        layout.addWidget(self.login_input)
        layout.addWidget(self.pwd_input)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_register)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.btn_login.clicked.connect(self.handle_login)
        self.btn_register.clicked.connect(self.open_register)
        self.user = None

    def handle_login(self):
        login = self.login_input.text().strip()
        pwd = self.pwd_input.text().strip()
        user = authenticate(login, pwd)
        if user:
            self.user = user
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")

    def open_register(self):
        dlg = RegisterDialog()
        dlg.exec()

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"Lab App - {user.role.value}")

        label = QLabel(f"Witaj, {user.login} ({user.role.value})")
        layout = QVBoxLayout()
        layout.addWidget(label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = LoginDialog()
    if dlg.exec() == QDialog.Accepted:
        win = MainWindow(dlg.user)
        win.show()
        sys.exit(app.exec())
