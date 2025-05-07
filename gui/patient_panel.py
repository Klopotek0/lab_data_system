from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox

#TODO: Implement the PatientPanel class
class PatientPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Panel")
