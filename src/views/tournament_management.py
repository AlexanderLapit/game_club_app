from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QMessageBox, QTabWidget, QLabel, QComboBox
)
from PyQt6.QtCore import Qt
from .tournament_form import TournamentForm
from .bracket_view import BracketView
from controllers.tournament_controller import TournamentController
from models.tournament import TournamentStatus
from datetime import datetime
import traceback

class TournamentManagement(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.controller = TournamentController()
        self.setWindowTitle("🏆 Управление турнирами")
        self.resize(1000, 700)
        self.setup_ui()
        self.load_tournaments()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Вкладки
        tabs = QTabWidget()

        # Вкладка со списком турниров
        self.tournaments_tab = QWidget()
        self.setup_tournaments_tab()
        tabs.addTab(self.tournaments_tab, "📋 Список турниров")

        # Вкладка для управления матчами
        self.matches_tab = QWidget()
        self.setup_matches_tab()
        tabs.addTab(self.matches_tab, "⚔️ Управление матчами")

        layout.addWidget(tabs)
        self.setLayout(layout)

    def setup_tournaments_tab(self):
        layout = QVBoxLayout()

        # Фильтр по статусу
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Статус:"))
        self.status_filter = QComboBox()
        self.status_filter.addItem("Все", None)
        self.status_filter.addItem("Регистрация", TournamentStatus.REGISTRATION)
        self.status_filter.addItem("Идут", TournamentStatus.ONGOING)
        self.status_filter.addItem("Завершены", TournamentStatus.COMPLETED)
        self.status_filter.currentIndexChanged.connect(self.load_tournaments)
        filter_layout.addWidget(self.status_filter)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Таблица турниров
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Название", "Игра", "Дата начала", "Участники",
            "Статус", "Действия", ""
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ Создать турнир")
        self.btn_add.clicked.connect(self.open_add_dialog)
        self.btn_refresh = QPushButton("🔄 Обновить")
        self.btn_refresh.clicked.connect(self.load_tournaments)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.tournaments_tab.setLayout(layout)

    def setup_matches_tab(self):
        layout = QVBoxLayout()

        # Выбор турнира для управления матчами
        select_layout = QHBoxLayout()
        select_layout.addWidget(QLabel("Выберите турнир:"))
        self.tournament_selector = QComboBox()
        self.tournament_selector.currentIndexChanged.connect(self.on_tournament_selected)
        select_layout.addWidget(self.tournament_selector)
        select_layout.addStretch()

        self.btn_generate_bracket = QPushButton("🎲 Сгенерировать сетку")
        self.btn_generate_bracket.clicked.connect(self.generate_bracket)
        self.btn_generate_bracket.setEnabled(False)
        select_layout.addWidget(self.btn_generate_bracket)

        layout.addLayout(select_layout)

        # Просмотр сетки
        self.bracket_view = BracketView()
        layout.addWidget(self.bracket_view)

        self.matches_tab.setLayout(layout)

    def load_tournaments(self):
        """Загрузить список турниров"""
        try:
            status = self.status_filter.currentData()
            tournaments = self.controller.get_all_tournaments(status)

            self.table.setRowCount(0)
            self.tournament_selector.clear()

            for t in tournaments:
                row = self.table.rowCount()
                self.table.insertRow(row)

                self.table.setItem(row, 0, QTableWidgetItem(str(t.id)))
                self.table.setItem(row, 1, QTableWidgetItem(t.name))
                self.table.setItem(row, 2, QTableWidgetItem(t.game))
                self.table.setItem(row, 3, QTableWidgetItem(t.start_date.strftime("%d.%m.%Y %H:%M")))

                participants_count = len(t.participants)
                self.table.setItem(row, 4, QTableWidgetItem(f"{participants_count}/{t.max_participants}"))

                status_text = {
                    TournamentStatus.REGISTRATION: "📝 Регистрация",
                    TournamentStatus.ONGOING: "⚔️ Идет",
                    TournamentStatus.COMPLETED: "✅ Завершен",
                    TournamentStatus.CANCELLED: "❌ Отменен"
                }.get(t.status, str(t.status))
                self.table.setItem(row, 5, QTableWidgetItem(status_text))

                # Кнопки действий
                actions_widget = QWidget()
                actions_layout = QHBoxLayout()
                actions_layout.setContentsMargins(0, 0, 0, 0)

                btn_view = QPushButton("👁️")
                btn_view.setToolTip("Просмотр")
                btn_view.clicked.connect(lambda _, tid=t.id: self.view_tournament(tid))

                btn_edit = QPushButton("✏️")
                btn_edit.setToolTip("Редактировать")
                btn_edit.clicked.connect(lambda _, tid=t.id: self.edit_tournament(tid))

                actions_layout.addWidget(btn_view)
                actions_layout.addWidget(btn_edit)
                actions_widget.setLayout(actions_layout)
                self.table.setCellWidget(row, 6, actions_widget)

                btn_delete = QPushButton("🗑️")
                btn_delete.setToolTip("Удалить")
                btn_delete.clicked.connect(lambda _, tid=t.id: self.delete_tournament(tid))
                self.table.setCellWidget(row, 7, btn_delete)

                # Добавление в селектор
                self.tournament_selector.addItem(f"{t.name} ({t.game})", t.id)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить турниры:\n{e}")

    def open_add_dialog(self):
        """Открыть диалог создания турнира"""
        dialog = TournamentForm(on_saved=self.create_tournament)
        dialog.exec()

    def create_tournament(self, data):
        """Создать новый турнир"""
        try:
            self.controller.create_tournament(
                name=data['name'],
                game=data['game'],
                start_date=data['start_date'],
                max_participants=data['max_participants'],
                created_by=self.current_user.id,
                description=data['description'],
                prize_pool=data['prize_pool']
            )
            self.load_tournaments()
            QMessageBox.information(self, "Успех", "Турнир создан успешно!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать турнир:\n{e}")

    def edit_tournament(self, tournament_id):
        """Редактировать турнир"""
        tournament = self.controller.get_tournament_by_id(tournament_id)
        if tournament:
            dialog = TournamentForm(tournament, on_saved=lambda data: self.update_tournament(tournament_id, data))
            dialog.exec()

    def update_tournament(self, tournament_id, data):
        """Обновить турнир"""
        try:
            tournament = self.controller.get_tournament_by_id(tournament_id)
            for key, value in data.items():
                setattr(tournament, key, value)
            self.controller.db_session.commit()
            self.load_tournaments()
            QMessageBox.information(self, "Успех", "Турнир обновлен!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить турнир:\n{e}")

    def delete_tournament(self, tournament_id):
        """Удалить турнир"""
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите удалить этот турнир?\nВсе данные будут потеряны!"
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.delete_tournament(tournament_id)
                self.load_tournaments()
                QMessageBox.information(self, "Успех", "Турнир удален!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить турнир:\n{e}")

    def view_tournament(self, tournament_id):
        """Просмотр турнира"""
        from .tournament_view import TournamentView
        self.view_window = TournamentView(tournament_id, self.current_user)
        self.view_window.show()

    def on_tournament_selected(self):
        """Обработчик выбора турнира в селекторе матчей"""
        tournament_id = self.tournament_selector.currentData()
        if tournament_id:
            self.btn_generate_bracket.setEnabled(True)
            self.load_bracket(tournament_id)
        else:
            self.btn_generate_bracket.setEnabled(False)

    def generate_bracket(self):
        """Сгенерировать турнирную сетку"""
        tournament_id = self.tournament_selector.currentData()
        if not tournament_id:
            return

        reply = QMessageBox.question(
            self, "Подтверждение",
            "Сгенерировать турнирную сетку?\nЭто действие нельзя отменить!"
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.generate_bracket(tournament_id)
                self.load_bracket(tournament_id)
                self.load_tournaments()
                QMessageBox.information(self, "Успех", "Турнирная сетка сгенерирована!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сгенерировать сетку:\n{e}")

    def load_bracket(self, tournament_id):
        """Загрузить и отобразить турнирную сетку"""
        try:
            matches = self.controller.get_tournament_matches(tournament_id)
            self.bracket_view.display_bracket(matches, self.controller)
        except Exception as e:
            print("Ошибка загрузки сетки:")
            print(traceback.format_exc())
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить сетку:\n{e}")
    def closeEvent(self, event):
        """Закрытие окна"""
        self.controller.close()
        super().closeEvent(event)