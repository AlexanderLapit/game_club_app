from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QMessageBox, QLabel, QTabWidget
)
from PyQt6.QtCore import Qt
from controllers.tournament_controller import TournamentController
from models.tournament import TournamentStatus
from .bracket_view import BracketView


class TournamentView(QWidget):
    def __init__(self, tournament_id=None, current_user=None):
        super().__init__()
        self.tournament_id = tournament_id
        self.current_user = current_user
        self.controller = TournamentController()
        self.setWindowTitle("🏆 Турниры")
        self.resize(900, 700)

        # Сначала создаем основной layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Затем настраиваем UI
        self.setup_ui()

        if tournament_id:
            self.load_tournament_details(tournament_id)
        else:
            self.load_available_tournaments()

    def setup_ui(self):
        # Очищаем layout перед добавлением новых виджетов
        self.clear_layout()

        if self.tournament_id:
            # Просмотр конкретного турнира
            self.setup_tournament_details_ui()
        else:
            # Список доступных турниров
            self.setup_tournaments_list_ui()

    def clear_layout(self):
        """Очистить layout от всех виджетов"""
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def setup_tournaments_list_ui(self):
        """Настройка UI для списка турниров"""
        # Заголовок
        title_label = QLabel("Доступные турниры")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Таблица турниров
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Название", "Игра", "Дата начала", "Участники", "Статус", "Действие"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.main_layout.addWidget(self.table)

        # Кнопка обновления
        btn_layout = QHBoxLayout()
        btn_refresh = QPushButton("🔄 Обновить список")
        btn_refresh.clicked.connect(self.load_available_tournaments)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_refresh)
        btn_layout.addStretch()
        self.main_layout.addLayout(btn_layout)

    def setup_tournament_details_ui(self):
        """Настройка UI для деталей турнира"""
        # Информация о турнире
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.main_layout.addWidget(self.info_label)

        # Вкладки
        tabs = QTabWidget()

        # Вкладка с информацией
        info_tab = QWidget()
        info_layout = QVBoxLayout()

        # Таблица участников
        info_layout.addWidget(QLabel("<b>Участники турнира:</b>"))
        self.participants_table = QTableWidget(0, 3)
        self.participants_table.setHorizontalHeaderLabels(["Участник", "Дата регистрации", "Статус"])
        self.participants_table.horizontalHeader().setStretchLastSection(True)
        info_layout.addWidget(self.participants_table)

        # Кнопки регистрации
        btn_layout = QHBoxLayout()
        self.btn_register = QPushButton("📝 Зарегистрироваться на турнир")
        self.btn_register.clicked.connect(self.register_for_tournament)
        self.btn_register.setStyleSheet("padding: 8px;")

        self.btn_unregister = QPushButton("❌ Отменить регистрацию")
        self.btn_unregister.clicked.connect(self.unregister_from_tournament)
        self.btn_unregister.setStyleSheet("padding: 8px;")

        btn_layout.addWidget(self.btn_register)
        btn_layout.addWidget(self.btn_unregister)
        info_layout.addLayout(btn_layout)

        # Кнопка назад
        btn_back = QPushButton("← Назад к списку турниров")
        btn_back.clicked.connect(self.back_to_list)
        info_layout.addWidget(btn_back)

        info_tab.setLayout(info_layout)
        tabs.addTab(info_tab, "ℹ️ Информация")

        # Вкладка с сеткой
        bracket_tab = QWidget()
        bracket_layout = QVBoxLayout()
        self.bracket_view = BracketView()
        bracket_layout.addWidget(self.bracket_view)
        bracket_tab.setLayout(bracket_layout)
        tabs.addTab(bracket_tab, "⚔️ Турнирная сетка")

        self.main_layout.addWidget(tabs)

    def back_to_list(self):
        """Вернуться к списку турниров"""
        self.tournament_id = None
        self.setup_ui()
        self.load_available_tournaments()

    def load_available_tournaments(self):
        """Загрузить доступные турниры"""
        try:
            tournaments = self.controller.get_all_tournaments()
            self.table.setRowCount(0)

            for t in tournaments:
                if t.status in [TournamentStatus.REGISTRATION, TournamentStatus.ONGOING]:
                    row = self.table.rowCount()
                    self.table.insertRow(row)

                    self.table.setItem(row, 0, QTableWidgetItem(t.name))
                    self.table.setItem(row, 1, QTableWidgetItem(t.game))
                    self.table.setItem(row, 2, QTableWidgetItem(t.start_date.strftime("%d.%m.%Y %H:%M")))

                    participants_count = len(t.participants)
                    self.table.setItem(row, 3, QTableWidgetItem(f"{participants_count}/{t.max_participants}"))

                    status_text = {
                        TournamentStatus.REGISTRATION: "📝 Регистрация",
                        TournamentStatus.ONGOING: "⚔️ Идет"
                    }.get(t.status, str(t.status))
                    self.table.setItem(row, 4, QTableWidgetItem(status_text))

                    # Кнопка просмотра
                    btn_view = QPushButton("👁️ Просмотр")
                    btn_view.clicked.connect(lambda checked, tid=t.id: self.view_tournament(tid))
                    self.table.setCellWidget(row, 5, btn_view)

            # Растягиваем колонки по содержимому
            self.table.resizeColumnsToContents()

        except Exception as e:
            import traceback
            print("Ошибка загрузки турниров:")
            print(traceback.format_exc())
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить турниры:\n{e}")

    def view_tournament(self, tournament_id):
        """Открыть просмотр конкретного турнира"""
        self.tournament_id = tournament_id
        self.setup_ui()
        self.load_tournament_details(tournament_id)

    def load_tournament_details(self, tournament_id):
        """Загрузить детали турнира"""
        try:
            tournament = self.controller.get_tournament_by_id(tournament_id)
            if not tournament:
                QMessageBox.warning(self, "Ошибка", "Турнир не найден")
                self.back_to_list()
                return

            # Обновляем заголовок окна
            self.setWindowTitle(f"🏆 {tournament.name}")

            # Информация о турнире
            info_text = f"""
            <h2 style="margin: 0;">{tournament.name}</h2>
            <p><b>🎮 Игра:</b> {tournament.game}</p>
            <p><b>📝 Описание:</b> {tournament.description or 'Нет описания'}</p>
            <p><b>📅 Дата начала:</b> {tournament.start_date.strftime('%d.%m.%Y %H:%M')}</p>
            <p><b>📊 Статус:</b> {
            '📝 Регистрация' if tournament.status == TournamentStatus.REGISTRATION else
            '⚔️ Идет' if tournament.status == TournamentStatus.ONGOING else
            '✅ Завершен' if tournament.status == TournamentStatus.COMPLETED else
            '❌ Отменен'
            }</p>
            <p><b>🏆 Призовой фонд:</b><br>{tournament.prize_pool or 'Не указан'}</p>
            """
            self.info_label.setText(info_text)

            # Загрузка участников
            participants = self.controller.get_tournament_participants(tournament_id)
            self.participants_table.setRowCount(len(participants))

            for i, p in enumerate(participants):
                self.participants_table.setItem(i, 0, QTableWidgetItem(p.user.username))
                self.participants_table.setItem(i, 1, QTableWidgetItem(
                    p.registered_at.strftime("%d.%m.%Y %H:%M") if p.registered_at else "Н/Д"
                ))

                if p.eliminated:
                    status = "❌ Выбыл"
                elif p.final_position:
                    status = f"🏆 {p.final_position} место"
                else:
                    status = "✅ Активен"
                self.participants_table.setItem(i, 2, QTableWidgetItem(status))

            self.participants_table.resizeColumnsToContents()

            # Проверка регистрации текущего пользователя
            is_registered = self.controller.is_user_registered(tournament_id, self.current_user.id)
            can_register = (tournament.status == TournamentStatus.REGISTRATION and
                            len(participants) < tournament.max_participants)

            self.btn_register.setEnabled(can_register and not is_registered)
            self.btn_unregister.setEnabled(is_registered and tournament.status == TournamentStatus.REGISTRATION)

            # Загрузка сетки
            matches = self.controller.get_tournament_matches(tournament_id)
            if matches:
                self.bracket_view.display_bracket(matches, self.controller)

        except Exception as e:
            import traceback
            print("Ошибка загрузки деталей турнира:")
            print(traceback.format_exc())
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить детали турнира:\n{e}")

    def register_for_tournament(self):
        """Зарегистрироваться на турнир"""
        try:
            self.controller.register_participant(self.tournament_id, self.current_user.id)
            self.load_tournament_details(self.tournament_id)
            QMessageBox.information(self, "Успех", "✅ Вы успешно зарегистрированы на турнир!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"❌ Не удалось зарегистрироваться:\n{e}")

    def unregister_from_tournament(self):
        """Отменить регистрацию"""
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите отменить регистрацию?"
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.unregister_participant(self.tournament_id, self.current_user.id)
                self.load_tournament_details(self.tournament_id)
                QMessageBox.information(self, "Успех", "✅ Регистрация отменена")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"❌ Не удалось отменить регистрацию:\n{e}")

    def closeEvent(self, event):
        """Закрытие окна"""
        if hasattr(self, 'controller'):
            self.controller.close()
        super().closeEvent(event)