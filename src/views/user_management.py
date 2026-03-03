from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout

class UserManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление пользователями")
        self.resize(700, 400)

        self.layout = QVBoxLayout()

        self.user_table = QTableWidget(0, 3)
        self.user_table.setHorizontalHeaderLabels(["Логин", "Уровень доступа", "Статус"])

        self.btn_add = QPushButton("Добавить пользователя")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)

        self.layout.addWidget(self.user_table)
        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)

        # Можно добавить логику работы с таблицей