from PySide6.QtWidgets import QApplication, QDialog
from database import engine
from models import Base
from services.seed import ensure_premade_users
from gui.login_panel import LoginDialog
from gui.main_window import MainWindow

Base.metadata.create_all(engine)
ensure_premade_users()

app = QApplication([])
dlg = LoginDialog()
if dlg.exec() == QDialog.Accepted:
    win = MainWindow(dlg.user)
    win.show()
    app.exec()
