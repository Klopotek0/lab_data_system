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
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout
)
from sqlalchemy import (
    create_engine, Column, Integer, String,
    DateTime, Enum, ForeignKey
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

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

class LabOrder(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="oczekujące")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    patient = relationship("User")

Base.metadata.create_all(engine)

# Ensure default admin exists
def ensure_admin():
    session = Session()
    if not session.query(User).filter_by(login="admin").first():
        pw_hash = bcrypt.hashpw("admin".encode(), bcrypt.gensalt()).decode()
        admin = User(login="admin", pw_hash=pw_hash, role=Role.admin)
        session.add(admin)
        session.commit()
    session.close()

ensure_admin()

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

def register_user(login: str, password: str, role: Role = Role.patient):
    session = Session()
    if session.query(User).filter_by(login=login).first():
        session.close()
        return None  # login already exists
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(login=login, pw_hash=pw_hash, role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return user

def new_order(patient_id: int):
    session = Session()
    order = LabOrder(patient_id=patient_id)
    session.add(order)
    session.commit()
    session.refresh(order)
    session.close()
    return order

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

        self.btn_login.clicked.connect(self.handle_login)
        self.btn_register.clicked.connect(self.handle_register)

        layout = QVBoxLayout()
        layout.addWidget(self.login_input)
        layout.addWidget(self.pwd_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_login)
        button_layout.addWidget(self.btn_register)
        layout.addLayout(button_layout)

        self.setLayout(layout)
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

    def handle_register(self):
        login = self.login_input.text().strip()
        pwd = self.pwd_input.text().strip()
        if not login or not pwd:
            QMessageBox.warning(self, "Error", "Login and password required")
            return
        user = register_user(login, pwd, Role.patient)
        if user:
            QMessageBox.information(self, "Success", "Account created. You can log in now.")
        else:
            QMessageBox.warning(self, "Error", "Login already exists")

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"Lab App - {user.role.value}")
        label = QLabel(f"Witaj, {user.login} ({user.role.value})")
        self.btn_new = QPushButton("Nowe zlecenie")
        self.btn_new.clicked.connect(self.create_order)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.btn_new)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_order(self):
        pid = self.user.id if self.user.role == Role.patient else 1
        order = new_order(pid)
        QMessageBox.information(self, "Zlecenie", f"Utworzono zlecenie ID {order.id}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = LoginDialog()
    if dlg.exec() == QDialog.Accepted:
        win = MainWindow(dlg.user)
        win.show()
        sys.exit(app.exec())