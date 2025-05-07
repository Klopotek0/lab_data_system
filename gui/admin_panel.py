from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget
from services.auth import get_unapproved_users, approve_user
from models import Role
from services.auth import get_users_by_role
from services.auth import delete_user

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("Pending user approvals:"))
        self.pending_table = QTableWidget()
        self.layout.addWidget(self.pending_table)
        self.load_pending_users()

        # Dodaj zakładki z użytkownikami wg ról
        self.tabs = QTabWidget()
        self.layout.addWidget(QLabel("Users by role:"))
        self.layout.addWidget(self.tabs)

        self.add_user_tab(Role.doctor, "Doctors")
        self.add_user_tab(Role.labtech, "Lab Technicians")
        self.add_user_tab(Role.patient, "Patients")

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
        for i in range(self.tabs.count()):
            table = self.tabs.widget(i)
            role = [Role.doctor, Role.labtech, Role.patient][i]
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