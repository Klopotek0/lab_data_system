from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from gui.admin_panel import AdminPanel
from gui.doctor_panel import DoctorPanel
from gui.labtech_panel import LabtechPanel
from gui.patient_panel import PatientPanel
from models import Role
from gui.login_panel import LoginDialog
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon

class MainWindow(QMainWindow):

    logout_requested = Signal()

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"Lab App - {user.role.value}")
        self.setWindowIcon(QIcon("gui/assets/icon.png"))
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #210f37;
                color: #000080;
                font-size: 15px;
                font-family: 'Raleway';
            }
            QPushButton {
                background-color: #51227e;
                color: #fffefe;
                padding: 12px 20px;
                border-radius: 12px;
                font-size: 15px;
                font-family: 'Raleway';
            }
          QPushButton:hover {
                background-color: #682da1;
            }
            QLabel {
                font-family: 'Raleway';
                font-size: 14px;
                color: #f5ebff;
                font-weight: bold;
                margin-left: 10px;
            }
        """)

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.handle_logout) 

        label = QLabel(f"Hello, {user.login} ({user.role.value})")
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.handle_logout)

        top_layout = QHBoxLayout()
        top_layout.addWidget(label)
        top_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        top_layout.addWidget(logout_btn)

        if user.role == Role.admin:
            panel = AdminPanel()
        elif user.role == Role.doctor:
            panel = DoctorPanel(user)
        elif user.role == Role.labtech:
            panel = LabtechPanel(user)
        elif user.role == Role.patient:
            panel = PatientPanel(user)
        else:
            panel = QLabel("Unknown role")

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(panel)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def handle_logout(self):
        self.close()
        self.logout_requested.emit()