from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from gui.admin_panel import AdminPanel
# from gui.doctor_panel import DoctorPanel
# from gui.labtech_panel import LabtechPanel
# from gui.patient_panel import PatientPanel

from models import Role


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"Lab App - {user.role.value}")

        if user.role == Role.admin:
            self.setCentralWidget(AdminPanel())
        # elif user.role == Role.doctor:
        #     self.setCentralWidget(DoctorPanel(user))
        # elif user.role == Role.labtech:
        #     self.setCentralWidget(LabtechPanel(user))
        # elif user.role == Role.patient:
        #     self.setCentralWidget(PatientPanel(user))
        
        # self.setCentralWidget(panel)

        label = QLabel(f"Witaj, {user.login} ({user.role.value})")
        layout = QVBoxLayout()
        layout.addWidget(label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)