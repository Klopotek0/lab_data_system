from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from services.auth import get_unapproved_users, approve_user

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administrator Panel")
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(QLabel("Pending user approvals:"))
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.load_data()

    def load_data(self):
        users = get_unapproved_users()
        self.table.setRowCount(len(users))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Login", "First Name", "Last Name", "Role", "Action"])

        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(user.login))
            self.table.setItem(row, 1, QTableWidgetItem(user.first_name or ""))
            self.table.setItem(row, 2, QTableWidgetItem(user.last_name or ""))
            self.table.setItem(row, 3, QTableWidgetItem(user.role.value))

            approve_button = QPushButton("Approve")
            approve_button.clicked.connect(lambda checked, uid=user.id: self.approve(uid))
            self.table.setCellWidget(row, 4, approve_button)

        self.table.resizeColumnsToContents()

    def approve(self, user_id):
        approve_user(user_id)
        QMessageBox.information(self, "Approved", f"User ID {user_id} has been approved.")
        self.load_data()  # refresh
