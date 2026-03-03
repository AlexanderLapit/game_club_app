from PyQt6.QtWidgets import QApplication
from controllers import MainController
from utils.captcha import Captcha
from database.db import engine, init_db  # ← импортируем engine и init_db

class App:
    def __init__(self):
        self.qt_app = QApplication([])

        # Инициализируем базу данных и создаём таблицы
        init_db()

        # Инициализация служб
        self.captcha_service = Captcha()

        # Инициализация контроллера
        self.controller = MainController(user_service=None, captcha_service=self.captcha_service)

    def run(self):
        self.controller.run()
        self.qt_app.exec()