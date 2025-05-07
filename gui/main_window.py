from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from gui.admin_panel import AdminPanel
from gui.doctor_panel import DoctorPanel
from gui.labtech_panel import LabtechPanel
from gui.patient_panel import PatientPanel
from models import Role
from gui.login_panel import LoginDialog
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"Lab App - {user.role.value}")
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
        login_dialog = LoginDialog()
        if login_dialog.exec() == QDialog.Accepted:
            new_main = MainWindow(login_dialog.user)
            new_main.show()
