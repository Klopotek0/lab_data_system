from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox

#TODO: Implement the DoctorPanel class
class DoctorPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Doctor Panel")
