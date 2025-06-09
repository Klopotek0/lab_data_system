from services.auth import authenticate, register_user
from models import Role
from PySide6.QtWidgets import (
    QDialog,
    QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QHBoxLayout, QComboBox, QLabel, QDateEdit
    )
import datetime
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDate
from PySide6.QtCore import Qt

class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setWindowIcon(QIcon("gui/assets/icon.png"))
        self.resize(400, 500)

        self.setStyleSheet("""
            QDialog {
                background-color: #210f37;
                color: #000080;
                font-size: 15px;
                font-family: 'Raleway';
            }
            QLineEdit, QDateEdit, QComboBox {
                background-color: #51227e;
                color: white;
                padding: 6px;
                border: 1px solid #51227e;
                border-radius: 4px;
                font-family: 'Raleway';
            }
            QComboBox QAbstractItemView {
                background-color: #51227e;
                color: white;
                selection-background-color: #403f79;
            }
            QDateEdit QCalendarWidget QWidget {
                background-color: #210f37;
                color: #a488c9;
            }
            QPushButton {
                background-color: #51227e;
                color: #fffefe;
                padding: 6px 14px;
                border-radius: 4px;
                font-family: 'Raleway';
            }
          QPushButton:hover {
                background-color: #682da1;
            }
            QLabel {
                font-family: 'Raleway';
                font-size: 15px;
                color: #a488c9;
            }
        """)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login")
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Password")
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setCalendarPopup(True) 
        self.birthdate_input.setDate(QDate.currentDate())
        self.role_select = QComboBox()
        self.role_select.addItem("Patient", Role.patient)
        self.role_select.addItem("Doctor", Role.doctor)
        self.role_select.addItem("Laborer", Role.labtech)

        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")

        layout = QVBoxLayout()
        layout.setSpacing(10)

        title_label = QLabel("CREATE ACCOUNT")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        layout.addWidget(QLabel("Login:"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.pwd_input)
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.first_name_input)
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.last_name_input)
        layout.addWidget(QLabel("Date of Birth:"))
        layout.addWidget(self.birthdate_input)
        layout.addWidget(QLabel("Role:"))
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
        birthdate = self.birthdate_input.date().toString("yyyy-MM-dd")
        role = self.role_select.currentData()
        if not all([login, pwd, first, last, birthdate]):
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
        try:
            bd = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
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