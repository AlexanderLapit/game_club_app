from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt


class LoginForm(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.setWindowTitle("Вход")
        self.resize(300, 150)

        layout = QFormLayout()
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_login = QPushButton("Войти")
        self.btn_cancel = QPushButton("Отмена")

        layout.addRow("Логин:", self.login_input)
        layout.addRow("Пароль:", self.password_input)
        layout.addRow(self.btn_login, self.btn_cancel)

        self.setLayout(layout)

        self.btn_login.clicked.connect(self.try_login)
        self.btn_cancel.clicked.connect(self.close)

    def try_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text()
        if login and password:
            # Здесь должна быть проверка через БД
            # Для теста — имитируем успешный вход
            from models import User, AccessLevel
            user = User(username=login, access_level=AccessLevel(name="Пользователь"))
            self.on_success(user)
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Ошибка", "Заполните поля")