from services.auth import authenticate, register_user
from models import Role
from PySide6.QtWidgets import (
    QDialog,
    QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QHBoxLayout, QComboBox
)
import datetime

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
        self.role_select = QComboBox()
        self.role_select.addItem("Patient", Role.patient)
        self.role_select.addItem("Doctor", Role.doctor)
        self.role_select.addItem("Laborer", Role.labtech)

        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")

        layout = QVBoxLayout()
        layout.addWidget(self.login_input)
        layout.addWidget(self.pwd_input)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.birthdate_input)
        layout.addWidget(self.role_select)
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
        role = self.role_select.currentData()
        if not all([login, pwd, first, last, bd_text]):
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
        try:
            bd = datetime.datetime.strptime(bd_text, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid birthdate format. Use YYYY-MM-DD.")
            return

        user = register_user(login, pwd, first, last, bd, role)
        if user:
            if role == Role.patient:
                QMessageBox.information(self, "Success", "Registration complete. You can now log in.")
            else:
                QMessageBox.information(self, "Success", "Registration submitted. Await administrator approval.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "This login is already taken.")