from PyQt6.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils.validators import is_valid_name, is_valid_login
from controllers.security import Security  # ← исправлено
from database import SessionLocal
from models import User, AccessLevel

class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация пользователя")
        self.resize(350, 200)

        self.layout = QFormLayout()

        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_register = QPushButton("Зарегистрироваться")
        self.btn_cancel = QPushButton("Отмена")

        self.layout.addRow("Логин:", self.login_input)
        self.layout.addRow("Пароль:", self.password_input)
        self.layout.addRow("Повтор пароля:", self.confirm_password_input)
        self.layout.addRow(self.btn_register, self.btn_cancel)

        self.setLayout(self.layout)

        self.btn_register.clicked.connect(self.handle_registration)
        self.btn_cancel.clicked.connect(self.close)

    def handle_registration(self):
        login = self.login_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not is_valid_login(login):
            QMessageBox.warning(self, "Ошибка", "Логин: 3–20 символов, только буквы, цифры, _")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Ошибка", "Пароль должен быть не менее 6 символов")
            return

        db = SessionLocal()
        try:
            if db.query(User).filter(User.username == login).first():
                QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует")
                return

            # Используем Security.hash_password
            hashed = Security.hash_password(password)
            new_user = User(username=login, password=hashed, access_level_id=2)
            db.add(new_user)
            db.commit()
            QMessageBox.information(self, "Успех", "Пользователь успешно зарегистрирован")
            self.close()

        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить пользователя: {e}")
        finally:
            db.close()