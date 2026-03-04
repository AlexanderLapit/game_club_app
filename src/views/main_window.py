from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, current_user, on_logout=None):
        super().__init__()
        self.current_user = current_user
        self.on_logout = on_logout
        self.setWindowTitle(f"📋 Главное меню — {current_user.username}")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f9f5eb;
            }
            QLabel {
                color: #4b3c27;
                font-size: 14px;
            }
            QPushButton {
                background-color: #d4c8a5;
                color: #4b3c27;
                border: 1px solid #c0b490;
                padding: 15px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e5d8b5;
            }
        """)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        self.label = QLabel(f"Добро пожаловать, <b>{self.current_user.username}</b><br>"
                            f"<span style='color:#7a6c4f;'>Уровень доступа: {self.current_user.access_level.name}</span>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; margin-bottom: 30px;")
        layout.addWidget(self.label)

        button_container = QVBoxLayout()
        button_container.setSpacing(15)

        self.btn_order = QPushButton("➕ Создать заказ")
        self.btn_user_mgmt = QPushButton("👥 Управление пользователями")
        self.btn_logout = QPushButton("🚪 Выйти")

        button_container.addWidget(self.btn_order)
        button_container.addWidget(self.btn_user_mgmt)
        button_container.addWidget(self.btn_logout)

        layout.addLayout(button_container)
        layout.addStretch()

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.btn_order.clicked.connect(self.open_order_form)
        self.btn_user_mgmt.clicked.connect(self.open_user_management)
        self.btn_logout.clicked.connect(self.handle_logout)

    def open_order_form(self):
        from views.order_form import OrderForm
        self.order_form = OrderForm()
        self.order_form.show()

    def open_user_management(self):
        from views.user_management import UserManagement
        self.user_mgmt = UserManagement()
        self.user_mgmt.show()

    def handle_logout(self):
        if self.on_logout:
            self.on_logout()
        self.close()