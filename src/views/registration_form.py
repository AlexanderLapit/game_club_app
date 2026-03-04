from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from utils.validators import is_valid_login
from controllers.security import Security
from database import SessionLocal
from models import User


class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📝 Регистрация")
        self.resize(360, 240)
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f5eb;
                font-family: "Segoe UI";
            }
            QLabel {
                color: #4b3c27;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #d0c4a8;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton {
                background-color: #d4c8a5;
                color: #4b3c27;
                border: none;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e5d8b5;
            }
        """)

        layout = QVBoxLayout()
        title = QLabel("Создайте новый аккаунт")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        form_layout = QFormLayout()
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("min 3 символа")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("не менее 6 символов")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("повторите пароль")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Логин:", self.login_input)
        form_layout.addRow("Пароль:", self.password_input)
        form_layout.addRow("Подтверждение:", self.confirm_password_input)
        layout.addLayout(form_layout)

        self.btn_register = QPushButton("Зарегистрироваться")
        self.btn_cancel = QPushButton("Отмена")
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.btn_register)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def connect_signals(self):
        self.btn_register.clicked.connect(self.handle_registration)
        self.btn_cancel.clicked.connect(self.close)

    def handle_registration(self):
        login = self.login_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_password_input.text()

        if not is_valid_login(login):
            QMessageBox.warning(self, "Ошибка", "Логин: 3–20 симв., буквы/цифры/_")
            return
        if len(password) < 6:
            QMessageBox.warning(self, "Ошибка", "Пароль ≥ 6 символов")
            return
        if password != confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return

        db = SessionLocal()
        try:
            if db.query(User).filter(User.username == login).first():
                QMessageBox.warning(self, "Ошибка", "Логин занят")
                return
            hashed = Security.hash_password(password)
            new_user = User(username=login, password=hashed, access_level_id=2)
            db.add(new_user)
            db.commit()
            QMessageBox.information(self, "Успех", "Регистрация успешна!")
            self.close()
        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка БД: {e}")
        finally:
            db.close()