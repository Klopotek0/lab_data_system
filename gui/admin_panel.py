from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QComboBox
from services.auth import get_unapproved_users, approve_user, get_users_by_role, delete_user
from models import Role
from services.assignments import get_all_doctors, get_unassigned_patients, assign_patient_to_doctor, get_patient_doctor_assignments, reassign_patient


class AdminPanel(QWidget):
    def __init__(self):
        self.role_tabs = []

        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #fffefe;
                border-radius: 12px;
            }
            QLabel {
                font-family: 'Raleway';
                font-size: 14px;
                color: #51227e;
                background: transparent;
            }
            QTableWidget {
                background-color: #f5ebff;
                border: 2px solid #d2c0ec;
                border-radius: 12px;
                color: #210f37;
                gridline-color: #d2c0ec;
                selection-background-color: #d2c0ec;
            }
            QHeaderView::section {
                background-color: #f5ebff;
                color: #51227e;
                padding: 4px;
                font-weight: bold;
                font-family: 'Raleway';
                border: none;
            }
            QTabBar::tab {
                background-color: #e7dcf5;
                color: #51227e;
                padding: 8px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-family: 'Raleway';
            }
            QTabBar::tab:selected {
                background-color: #d2c0ec;
                font-weight: bold;
            }
            QPushButton {
                background-color: #51227e;
                color: #fffefe;
                padding: 8px 16px;
                border-radius: 12px;
                font-size: 13px;
                font-family: 'Raleway';
            }
            QPushButton:hover {
                background-color: #682da1;
            }
            QCheckBox {
                color: #51227e;
                font-family: 'Raleway';
                padding: 2px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #51227e;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #b38ee3;
                border: 1px solid #51227e;
            }
            QComboBox, QTextEdit {
                background-color: #f2e6ff;
                color: #210f37;
                border-radius: 8px;
                padding: 6px;
                font-family: 'Raleway';
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #210f37;
                selection-background-color: #d2c0ec;
                font-family: 'Raleway';
            }
            QScrollBar:horizontal {
                border: none;
                background: #f2e6ff;
                height: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }

            QScrollBar::handle:horizontal {
                background: #b38ee3;
                min-width: 20px;
                border-radius: 5px;
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }

        """)

        self.user_appr_label = QLabel("Pending user approvals:")
        self.user_appr_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #a488c9;")
        self.layout.addWidget(self.user_appr_label)
        self.pending_table = QTableWidget()
        self.layout.addWidget(self.pending_table)
        self.load_pending_users()

        self.tabs = QTabWidget()
        self.user_role_label = QLabel("Users by role:")
        self.user_role_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #a488c9;")
        self.layout.addWidget(self.user_role_label)
        self.layout.addWidget(self.tabs)
        self.add_assignment_tab()

        self.add_user_tab(Role.doctor, "Doctors")
        self.add_user_tab(Role.labtech, "Lab Technicians")
        self.add_user_tab(Role.patient, "Patients")
        self.add_reassignment_tab()


    def load_pending_users(self):
        users = get_unapproved_users()
        self.pending_table.setRowCount(len(users))
        self.pending_table.setColumnCount(5)
        self.pending_table.setHorizontalHeaderLabels(["Login", "First Name", "Last Name", "Role", "Action"])

        for row, user in enumerate(users):
            self.pending_table.setItem(row, 0, QTableWidgetItem(user.login))
            self.pending_table.setItem(row, 1, QTableWidgetItem(user.first_name or ""))
            self.pending_table.setItem(row, 2, QTableWidgetItem(user.last_name or ""))
            self.pending_table.setItem(row, 3, QTableWidgetItem(user.role.value))

            approve_button = QPushButton("Approve")
            approve_button.clicked.connect(lambda checked, uid=user.id: self.approve(uid))
            self.pending_table.setCellWidget(row, 4, approve_button)

        self.pending_table.resizeColumnsToContents()

    def approve(self, user_id):
        approve_user(user_id)
        QMessageBox.information(self, "Approved", f"User ID {user_id} has been approved.")
        self.load_pending_users()
        self.refresh_all_tabs()

    def add_user_tab(self, role, title):
        table = QTableWidget()
        self.populate_role_table(table, role)
        self.tabs.addTab(table, title)
        self.role_tabs.append((table, role))

    def populate_role_table(self, table, role):
        users = get_users_by_role(role)
        table.setRowCount(len(users))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Login", "First Name", "Last Name", "Birthdate", "Action"])

        for row, user in enumerate(users):
            table.setItem(row, 0, QTableWidgetItem(user.login))
            table.setItem(row, 1, QTableWidgetItem(user.first_name or ""))
            table.setItem(row, 2, QTableWidgetItem(user.last_name or ""))
            table.setItem(row, 3, QTableWidgetItem(user.birthdate.strftime("%Y-%m-%d") if user.birthdate else ""))

            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, uid=user.id, r=role: self.delete_user(uid, r))
            table.setCellWidget(row, 4, delete_btn)

        table.resizeColumnsToContents()

    def refresh_all_tabs(self):
        for table, role in self.role_tabs:
            self.populate_role_table(table, role)

    def delete_user(self, user_id, role):
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete user ID {user_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_user(user_id)
            self.refresh_all_tabs()

    def add_assignment_tab(self):
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)

        self.doctor_select = QComboBox()
        self.doctors = get_all_doctors()
        for doctor in self.doctors:
            self.doctor_select.addItem(f"{doctor.first_name} {doctor.last_name} ({doctor.login})", doctor.id)
        
        self.doctor_select.setStyleSheet("padding: 12px; border: 1px solid #f2e6ff; font-family: 'Raleway';")

        self.patient_table = QTableWidget()
        layout.addWidget(QLabel("Select doctor to assign patients:"))
        layout.addWidget(self.doctor_select)
        layout.addWidget(self.patient_table)

        self.tabs.addTab(container, "Assign Patients")
        self.load_assignable_patients()

    def load_assignable_patients(self):
        patients = get_unassigned_patients()
        self.patient_table.setRowCount(len(patients))
        self.patient_table.setColumnCount(5)
        self.patient_table.setHorizontalHeaderLabels(["Login", "First Name", "Last Name", "Birthdate", "Assign"])

        for row, patient in enumerate(patients):
            self.patient_table.setItem(row, 0, QTableWidgetItem(patient.login))
            self.patient_table.setItem(row, 1, QTableWidgetItem(patient.first_name or ""))
            self.patient_table.setItem(row, 2, QTableWidgetItem(patient.last_name or ""))
            self.patient_table.setItem(row, 3, QTableWidgetItem(patient.birthdate.strftime("%Y-%m-%d")))

            assign_btn = QPushButton("Assign")
            assign_btn.clicked.connect(lambda _, pid=patient.id: self.assign_selected(pid))
            self.patient_table.setCellWidget(row, 4, assign_btn)

    def assign_selected(self, patient_id):
        doctor_id = self.doctor_select.currentData()
        assign_patient_to_doctor(patient_id, doctor_id)
        QMessageBox.information(self, "Assigned", "Patient has been assigned.")
        self.load_assignable_patients()
        
    def add_reassignment_tab(self):
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)

        self.reassign_table = QTableWidget()
        layout.addWidget(QLabel("Patient-Doctor Assignments:"))
        layout.addWidget(self.reassign_table)

        self.tabs.addTab(container, "View & Reassign")
        self.load_patient_doctor_assignments()

    def load_patient_doctor_assignments(self):
        assignments = get_patient_doctor_assignments()
        doctors = get_all_doctors()

        self.reassign_table.setRowCount(len(assignments))
        self.reassign_table.setColumnCount(4)
        self.reassign_table.setHorizontalHeaderLabels(["Patient", "Current Doctor", "New Doctor", "Action"])

        for row, (patient, doctor) in enumerate(assignments):
            self.reassign_table.setItem(row, 0, QTableWidgetItem(f"{patient.first_name} {patient.last_name} ({patient.login})"))
            self.reassign_table.setItem(row, 1, QTableWidgetItem(f"{doctor.first_name} {doctor.last_name} ({doctor.login})"))

            new_doc_box = QComboBox()
            for d in doctors:
                new_doc_box.addItem(f"{d.first_name} {d.last_name} ({d.login})", d.id)
            self.reassign_table.setCellWidget(row, 2, new_doc_box)

            assign_btn = QPushButton("Reassign")
            assign_btn.clicked.connect(lambda _, p_id=patient.id, box=new_doc_box: self.reassign(p_id, box))
            self.reassign_table.setCellWidget(row, 3, assign_btn)

        self.reassign_table.resizeColumnsToContents()

    def reassign(self, patient_id, combo_box):
        new_doctor_id = combo_box.currentData()
        reassign_patient(patient_id, new_doctor_id)
        QMessageBox.information(self, "Reassigned", "Patient has been reassigned to a new doctor.")
        self.load_patient_doctor_assignments()