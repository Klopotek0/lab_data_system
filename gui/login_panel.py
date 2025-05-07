from services.auth import authenticate
from models import Role
from .register_dialog import RegisterDialog
from gui.admin_panel import AdminPanel
from PySide6.QtWidgets import (
    QDialog,
    QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QHBoxLayout
)

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