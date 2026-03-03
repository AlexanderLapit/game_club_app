from PyQt6.QtWidgets import QMessageBox
from .security import Security

class AuthController:
    def __init__(self, user_service, captcha_service):
        self.user_service = user_service
        self.captcha_service = captcha_service
        self.failed_attempts = {}

    def login(self, username, password):
        if not self.captcha_service.verify():
            QMessageBox.warning(None, "Капча", "Пожалуйста, решите капчу правильно")
            return False

        user = self.user_service.get_user(username)
        if user:
            stored_password = user['password']
            if Security.verify_password(stored_password, password):
                # Успешный вход
                self.reset_attempts(username)
                return True
            else:
                self.increment_attempts(username)
                QMessageBox.warning(None, "Ошибка", "Неверный пароль")
                return False
        else:
            QMessageBox.warning(None, "Ошибка", "Пользователь не найден")
            return False

    def increment_attempts(self, username):
        self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
        if self.failed_attempts[username] >= 3:
            self.lock_user(username)

    def reset_attempts(self, username):
        self.failed_attempts.pop(username, None)

    def lock_user(self, username):
        self.user_service.lock_user(username)
        QMessageBox.warning(None, "Блокировка", f"Пользователь {username} заблокирован после 3 неудачных попыток.")