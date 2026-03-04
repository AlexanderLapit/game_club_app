from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt


class UserManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("👥 Управление пользователями")
        self.resize(800, 500)
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f5eb;
            }
            QTableWidget {
                background-color: white;
                gridline-color: #e8e0d0;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #e8e0d0;
                color: #4b3c27;
                padding: 6px;
                font-weight: bold;
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
        self.user_table = QTableWidget(0, 4)
        self.user_table.setHorizontalHeaderLabels(["ID", "Логин", "Уровень", "Статус"])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.user_table)

        self.btn_add = QPushButton("➕ Добавить")
        self.btn_edit = QPushButton("✏️ Редактировать")
        self.btn_delete = QPushButton("🗑️ Удалить")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_add.clicked.connect(self.add_user)
        self.btn_edit.clicked.connect(self.edit_user)
        self.btn_delete.clicked.connect(self.delete_user)

    def load_users(self):
        """Загружает список пользователей в таблицу"""
        try:
            from controllers.user_controller import UserController
            uc = UserController()
            users = uc.get_all_users()
            self.user_table.setRowCount(0)  # Очистить таблицу

            for user in users:
                row = self.user_table.rowCount()
                self.user_table.insertRow(row)

                self.user_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
                self.user_table.setItem(row, 1, QTableWidgetItem(user.username))
                self.user_table.setItem(row, 2, QTableWidgetItem(user.access_level.name))
                status = "Активен" if user.is_active else "Заблокирован"
                self.user_table.setItem(row, 3, QTableWidgetItem(status))

            uc.close()

        except Exception as e:
            import traceback
            print("Ошибка при загрузке пользователей:")
            print(traceback.format_exc())

            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось загрузить пользователей.\nПроверьте подключение к базе данных.\n\nДетали: {e}"
            )

    def add_user(self):
        QMessageBox.information(self, "Добавить", "Функция в разработке.")

    def edit_user(self):
        selected = self.user_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Выберите", "Сначала выберите пользователя.")
            return
        user_id = int(self.user_table.item(selected, 0).text())
        QMessageBox.information(self, "Редактировать", f"Редактируем пользователя ID={user_id}")

    def delete_user(self):
        selected = self.user_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Выберите", "Сначала выберите пользователя.")
            return
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить этого пользователя?"
        )
        if reply == QMessageBox.StandardButton.Yes:
            user_id = int(self.user_table.item(selected, 0).text())
            try:
                from controllers.user_controller import UserController
                uc = UserController()
                uc.delete_user(user_id)
                uc.close()
                self.load_users()  # Обновить таблицу
                QMessageBox.information(self, "Успех", "Пользователь удалён.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить: {e}")