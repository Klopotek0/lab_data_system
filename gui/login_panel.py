from services.auth import authenticate
from models import Role
from .register_dialog import RegisterDialog
from gui.admin_panel import AdminPanel
from PySide6.QtWidgets import (
    QDialog, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QHBoxLayout, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("gui/assets/icon.png"))
        self.resize(400, 500) 

        # Styl
        self.setStyleSheet("""
            QDialog {
                background-color: #210f37;
                color: #000080;
                font-size: 15px;
                font-family: 'Raleway';

            }
            QLineEdit {
                background-color: #51227e;
                padding: 6px;
                border: 1px solid #51227e;
                border-radius: 12px;
                font-size: 15px;
                font-family: 'Raleway';
            }
            QPushButton {
                background-color: #51227e;
                color: #fffefe;
                padding: 6px 14px;
                border-radius: 12px;
                font-size: 15px;
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
        
        title_label = QLabel("LAB TEST SYSTEM")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        #logo
        logo_label = QLabel()
        pixmap = QPixmap("gui/assets/login_logo.png")
        pixmap = pixmap.scaled(250, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter) 

        # Pola logowania
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login")
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Password")
        self.pwd_input.setEchoMode(QLineEdit.Password)

        # Przyciski
        self.btn_login = QPushButton("Login")
        self.btn_register = QPushButton("Register")

        # Układ
        layout = QVBoxLayout()
        
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        layout.addWidget(title_label)

        layout.addWidget(logo_label)    

        self.info_label = QLabel("Please log in to the system:")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #a488c9;")
        layout.addWidget(self.info_label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.pwd_input)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_register)
        layout.addWidget(self.error_label)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Akcje
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
            self.error_label.setText("Invalid login or password.")
            self.error_label.show()

    def open_register(self):
        dlg = RegisterDialog()
        dlg.exec()
