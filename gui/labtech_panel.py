from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox

#TODO: Implement the Labtech class
class LabtechPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Labtech Panel")
