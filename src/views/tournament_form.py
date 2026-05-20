from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox,
    QDateTimeEdit, QTextEdit, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import QDateTime


class TournamentForm(QDialog):
    def __init__(self, tournament=None, on_saved=None):
        super().__init__()
        self.tournament = tournament
        self.on_saved = on_saved
        self.setWindowTitle("Создать турнир" if not tournament else "Редактировать турнир")
        self.resize(500, 400)
        self.setup_ui()

        if tournament:
            self.load_tournament_data()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название турнира")
        form_layout.addRow("Название:", self.name_input)

        self.game_input = QLineEdit()
        self.game_input.setPlaceholderText("Название игры")
        form_layout.addRow("Игра:", self.game_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Описание турнира")
        self.description_input.setMaximumHeight(100)
        form_layout.addRow("Описание:", self.description_input)

        self.start_date_input = QDateTimeEdit()
        self.start_date_input.setDateTime(QDateTime.currentDateTime().addDays(7))
        self.start_date_input.setCalendarPopup(True)
        form_layout.addRow("Дата начала:", self.start_date_input)

        self.max_participants_input = QSpinBox()
        self.max_participants_input.setRange(2, 128)
        self.max_participants_input.setValue(16)
        self.max_participants_input.setSuffix(" участников")
        form_layout.addRow("Макс. участников:", self.max_participants_input)

        self.prize_pool_input = QTextEdit()
        self.prize_pool_input.setPlaceholderText("Призовой фонд (например: 1 место - 1000 руб.)")
        self.prize_pool_input.setMaximumHeight(80)
        form_layout.addRow("Призы:", self.prize_pool_input)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_tournament)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def load_tournament_data(self):
        """Загрузить данные существующего турнира"""
        self.name_input.setText(self.tournament.name)
        self.game_input.setText(self.tournament.game)
        self.description_input.setText(self.tournament.description or "")
        self.start_date_input.setDateTime(self.tournament.start_date)
        self.max_participants_input.setValue(self.tournament.max_participants)
        self.prize_pool_input.setText(self.tournament.prize_pool or "")

    def save_tournament(self):
        """Сохранить турнир"""
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название турнира")
            return

        if not self.game_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название игры")
            return

        self.tournament_data = {
            'name': self.name_input.text().strip(),
            'game': self.game_input.text().strip(),
            'description': self.description_input.toPlainText().strip(),
            'start_date': self.start_date_input.dateTime().toPyDateTime(),
            'max_participants': self.max_participants_input.value(),
            'prize_pool': self.prize_pool_input.toPlainText().strip()
        }

        if self.on_saved:
            self.on_saved(self.tournament_data)

        self.accept()