from PyQt6.QtWidgets import QApplication
from views import MainWindow, LoginForm
from utils.logger import log_action


class MainController:
    def __init__(self, user_service=None, captcha_service=None):
        self.app = QApplication([])
        self.user_service = user_service
        self.captcha_service = captcha_service
        self.main_window = None
        self.current_user = None

    def run(self):
        self.show_login()
        self.app.exec()

    def show_login(self):
        self.login_form = LoginForm(on_success=self.on_login_success)
        self.login_form.show()

    def on_login_success(self, user):
        self.current_user = user
        log_action(user.username, "Авторизован")
        self.login_form.close()
        self.show_main_window()

    def show_main_window(self):
        self.main_window = MainWindow(current_user=self.current_user)
        self.main_window.show()

    def logout(self):
        if self.main_window:
            self.main_window.hide()
            self.main_window = None
        log_action(self.current_user.username, "Выход из системы")
        self.current_user = None
        self.show_login()