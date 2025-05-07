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
    QWidget, QMessageBox, QHBoxLayout, QComboBox
)
from sqlalchemy import (
    create_engine, Column, Integer, String,
    DateTime, Enum, ForeignKey, Boolean
)
from sqlalchemy.orm import sessionmaker, declarative_base
from models import User, Role, Base

# ---- Database setup ----
engine = create_engine("sqlite:///lab.db", echo=False)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

# Ensure default admin and doctor

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

ensure_premade_users()

# ---- Services ----
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


# ---- GUI ----

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
