from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .captcha_dialog import CaptchaDialog


class LoginForm(QWidget):
    def __init__(self, auth_controller, on_success):
        super().__init__()
        self.auth_controller = auth_controller
        self.on_success = on_success
        self.setWindowTitle("🔐 Вход в систему")
        self.resize(340, 200)
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Настройка внешнего вида формы."""
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f5eb;
                font-family: "Segoe UI", sans-serif;
            }
            QLabel {
                color: #4b3c27;
                font-size: 13px;
            }
            QPushButton {
                background-color: #d4c8a5;
                color: #4b3c27;
                border: 1px solid #c0b490;
                padding: 10px;
                border-radius: 6px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e5d8b5;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #d0c4a8;
                padding: 8px;
                border-radius: 6px;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel("Добро пожаловать")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        form_layout = QFormLayout()
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Логин:", self.login_input)
        form_layout.addRow("Пароль:", self.password_input)
        layout.addLayout(form_layout)

        self.btn_login = QPushButton("Войти")
        self.btn_cancel = QPushButton("Отмена")

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def connect_signals(self):
        """Подключение сигналов."""
        self.btn_login.clicked.connect(self.try_login)
        self.btn_cancel.clicked.connect(self.close)

    def try_login(self):
        """Обработка попытки входа."""
        login = self.login_input.text().strip()
        password = self.password_input.text()

        if not login or not password:
            QMessageBox.warning(self, "⚠️ Ошибка", "Заполните все поля")
            return

        try:
            captcha_dialog = CaptchaDialog(self.auth_controller.captcha_service)
            result = captcha_dialog.exec()

            if result != captcha_dialog.DialogCode.Accepted:
                QMessageBox.warning(self, "Капча", "Вы не прошли проверку капчи")
                return
        except Exception as e:
            import traceback
            print("[FATAL] Ошибка при открытии капчи:")
            print(traceback.format_exc())
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть капчу:\n{str(e)}")
            return

        success = self.auth_controller.login(login, password)
        if not success:
            self.password_input.clear()
            QMessageBox.warning(self, "❌ Ошибка", "Неверный логин или пароль")
            return

        try:
            from controllers.user_controller import UserController
            user_service = UserController()
            user = user_service.get_user(login)

            if not user:
                QMessageBox.critical(self, "Ошибка", "Пользователь не найден")
                return

            if not user.is_active:
                QMessageBox.critical(self, "❌ Ошибка", "Аккаунт деактивирован")
                return

            username = getattr(user, 'username', None)
            access_level = getattr(user, 'access_level', None)
            level_name = getattr(access_level, 'name', 'Неизвестно') if access_level else 'Неизвестно'

            if not username:
                QMessageBox.critical(self, "Ошибка", "Данные пользователя повреждены")
                return

            print(f"[INFO] Успешный вход: {username}, уровень: {level_name}")

            self.on_success(user)
            self.close()

        except Exception as e:
            import traceback
            print("[FATAL] Ошибка при загрузке пользователя:")
            print(traceback.format_exc())
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные пользователя:\n{str(e)}")