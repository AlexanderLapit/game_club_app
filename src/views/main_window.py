from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, current_user, on_logout=None):
        super().__init__()
        self.setWindowTitle("Клуб настольных игр")
        self.resize(800, 600)

        self.on_logout = on_logout  # Сохраняем callback

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel(f"Добро пожаловать, {current_user.username} ({current_user.access_level.name})")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_order = QPushButton("Создать заказ")
        self.btn_user_mgmt = QPushButton("Управление пользователями")
        self.btn_logout = QPushButton("Выйти")

        layout.addWidget(self.label)
        layout.addWidget(self.btn_order)
        layout.addWidget(self.btn_user_mgmt)
        layout.addWidget(self.btn_logout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключаем кнопку выхода
        self.btn_logout.clicked.connect(self.handle_logout)

    def handle_logout(self):
        if self.on_logout:
            self.on_logout()