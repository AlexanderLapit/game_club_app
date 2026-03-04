from PyQt6.QtWidgets import QApplication
from controllers import MainController
from utils.captcha import Captcha
from database.db import engine, init_db


class App:
    def __init__(self):
        self.qt_app = QApplication([])
        init_db()
        self.captcha_service = Captcha()
        self.controller = MainController(captcha_service=self.captcha_service)

    def run(self):
        self.controller.run()