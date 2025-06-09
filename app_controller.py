# app_controller.py

from PySide6.QtWidgets import QApplication, QDialog
from gui.login_panel import LoginDialog
from gui.main_window import MainWindow


class AppController:
    def __init__(self):
        self.login_dialog = None
        self.main_window = None

    def run(self):
        self.show_login()

    def show_login(self):
        self.login_dialog = LoginDialog()
        if self.login_dialog.exec() == QDialog.Accepted:
            self.show_main_window(self.login_dialog.user)

    def show_main_window(self, user):
        self.main_window = MainWindow(user)
        self.main_window.logout_requested.connect(self.show_login)
        self.main_window.show()
