# main.py
from PySide6.QtWidgets import QApplication
from database import engine
from models import Base
from services.seed import ensure_premade_users
from app_controller import AppController 

Base.metadata.create_all(engine)
ensure_premade_users()

if __name__ == "__main__":
    app = QApplication([])
    controller = AppController()
    controller.run()
    app.exec()
