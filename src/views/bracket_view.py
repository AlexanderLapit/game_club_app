from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QGridLayout,
    QLabel, QFrame, QPushButton, QDialog, QSpinBox, QHBoxLayout, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from models.tournament import MatchResult


class BracketView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.matches = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.content_widget = QWidget()
        self.grid_layout = QGridLayout(self.content_widget)
        self.grid_layout.setSpacing(20)

        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)

        self.setLayout(layout)

    def display_bracket(self, matches, controller):
        """Отобразить турнирную сетку"""
        self.controller = controller
        self.matches = matches

        # Очистка предыдущего отображения
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        if not matches:
            label = QLabel("🏆 Турнирная сетка еще не сгенерирована\n\n"
                           "Сетка будет создана администратором перед началом турнира")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 14px; color: #666; padding: 50px;")
            label.setWordWrap(True)
            self.grid_layout.addWidget(label, 0, 0)
            return

        # Группировка матчей по раундам
        rounds = {}
        for match in matches:
            if match.round_number not in rounds:
                rounds[match.round_number] = []
            rounds[match.round_number].append(match)

        # Находим максимальное количество матчей в раунде для правильного размещения
        max_matches_in_round = max(len(round_matches) for round_matches in rounds.values())

        # Отображение по раундам
        for round_num, round_matches in sorted(rounds.items()):
            # Заголовок раунда
            round_label = QLabel(f"Раунд {round_num}")
            round_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(round_label, 0, round_num - 1)

            # Рассчитываем вертикальные отступы для центрирования матчей
            matches_in_this_round = len(round_matches)
            vertical_spacing = max(1, max_matches_in_round // (matches_in_this_round * 2))

            sorted_matches = sorted(round_matches, key=lambda m: m.match_number)

            for i, match in enumerate(sorted_matches):
                match_widget = self.create_match_widget(match)
                # Размещаем матчи с отступами для визуального центрирования
                row_position = 1 + i * (vertical_spacing * 2)
                self.grid_layout.addWidget(match_widget, row_position, round_num - 1)

    def create_match_widget(self, match):
        """Создать виджет для отображения матча"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setLineWidth(2)
        frame.setMinimumWidth(220)
        frame.setMinimumHeight(120)

        # Установка цвета в зависимости от статуса
        if match.result == MatchResult.NOT_PLAYED:
            if match.player1_id and match.player2_id:
                frame.setStyleSheet("QFrame { background-color: #2a2a2a; border: 2px solid #4a4a4a; }")
            else:
                frame.setStyleSheet("QFrame { background-color: #252525; border: 2px dashed #555; }")
        else:
            frame.setStyleSheet("QFrame { background-color: #3a3a3a; border: 2px solid #5a5a5a; }")

        layout = QVBoxLayout()
        layout.setSpacing(5)

        # Игрок 1
        player1_text = match.player1.user.username if match.player1 else "Ожидание"
        player1_label = QLabel(f"👤 {player1_text}")
        player1_label.setWordWrap(True)

        if match.result == MatchResult.PLAYER1_WIN:
            player1_label.setStyleSheet(
                "font-weight: bold; color: #4CAF50; background-color: #1a3a1a; "
                "padding: 4px; border-radius: 3px;")
            player1_label.setText(f"🏆 {player1_text}")
        elif match.result == MatchResult.PLAYER2_WIN:
            player1_label.setStyleSheet("color: #999;")
            player1_label.setText(f"👤 {player1_text}")
        elif not match.player1_id:
            player1_label.setStyleSheet("color: #888; font-style: italic;")
            player1_label.setText("⏳ Ожидание...")

        layout.addWidget(player1_label)

        # Счет или VS
        if match.result == MatchResult.NOT_PLAYED:
            if match.player1_id and match.player2_id:
                vs_label = QLabel("VS")
                vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                vs_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #FF9800;")
                layout.addWidget(vs_label)
            elif match.player1_id or match.player2_id:
                # Один игрок есть - автоматический проход
                auto_label = QLabel("BYE →")
                auto_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                auto_label.setStyleSheet("font-size: 10px; color: #FFA726; font-style: italic;")
                layout.addWidget(auto_label)
        else:
            score_label = QLabel(f"{match.player1_score or 0} - {match.player2_score or 0}")
            score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            score_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            score_label.setStyleSheet("color: white;")
            layout.addWidget(score_label)

        # Игрок 2
        player2_text = match.player2.user.username if match.player2 else "Ожидание"
        player2_label = QLabel(f"👤 {player2_text}")
        player2_label.setWordWrap(True)

        if match.result == MatchResult.PLAYER2_WIN:
            player2_label.setStyleSheet(
                "font-weight: bold; color: #4CAF50; background-color: #1a3a1a; "
                "padding: 4px; border-radius: 3px;")
            player2_label.setText(f"🏆 {player2_text}")
        elif match.result == MatchResult.PLAYER1_WIN:
            player2_label.setStyleSheet("color: #999;")
            player2_label.setText(f"👤 {player2_text}")
        elif not match.player2_id:
            player2_label.setStyleSheet("color: #888; font-style: italic;")
            player2_label.setText("⏳ Ожидание...")

        layout.addWidget(player2_label)

        # Информация о матче
        match_info = f"Р{match.round_number} М{match.match_number}"
        info_label = QLabel(match_info)
        info_label.setStyleSheet("font-size: 9px; color: #777;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        # Кнопка для ввода результата (если матч готов к игре)
        if match.result == MatchResult.NOT_PLAYED and match.player1_id and match.player2_id:
            btn_result = QPushButton("📊 Ввести результат")
            btn_result.setStyleSheet("""
                QPushButton {
                    background-color: #1565C0;
                    color: white;
                    padding: 6px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            btn_result.clicked.connect(lambda checked, m=match: self.open_result_dialog(m))
            layout.addWidget(btn_result)

        frame.setLayout(layout)
        return frame

    def open_result_dialog(self, match):
        """Открыть диалог ввода результата матча"""
        dialog = MatchResultDialog(match, self.controller, self)
        if dialog.exec():
            # Обновить отображение
            tournament_id = match.tournament_id
            matches = self.controller.get_tournament_matches(tournament_id)
            self.display_bracket(matches, self.controller)


class MatchResultDialog(QDialog):
    def __init__(self, match, controller, parent=None):
        super().__init__(parent)
        self.match = match
        self.controller = controller
        self.parent_view = parent
        self.setWindowTitle("Ввод результата матча")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Информация о матче
        player1_name = self.match.player1.user.username if self.match.player1 else "Неизвестно"
        player2_name = self.match.player2.user.username if self.match.player2 else "Неизвестно"

        info_label = QLabel(f"Матч раунда {self.match.round_number}\n"
                            f"{player1_name} vs {player2_name}")
        info_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("padding: 10px;")
        layout.addWidget(info_label)

        # Ввод счета
        score_layout = QHBoxLayout()
        score_layout.setSpacing(20)

        # Игрок 1
        player1_layout = QVBoxLayout()
        player1_name_label = QLabel(player1_name)
        player1_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        player1_name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        player1_layout.addWidget(player1_name_label)

        self.score1_input = QSpinBox()
        self.score1_input.setRange(0, 100)
        self.score1_input.setValue(0)
        self.score1_input.setStyleSheet("font-size: 18px; padding: 5px;")
        player1_layout.addWidget(self.score1_input)
        score_layout.addLayout(player1_layout)

        # Разделитель
        vs_label = QLabel("VS")
        vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vs_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        score_layout.addWidget(vs_label)

        # Игрок 2
        player2_layout = QVBoxLayout()
        player2_name_label = QLabel(player2_name)
        player2_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        player2_name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        player2_layout.addWidget(player2_name_label)

        self.score2_input = QSpinBox()
        self.score2_input.setRange(0, 100)
        self.score2_input.setValue(0)
        self.score2_input.setStyleSheet("font-size: 18px; padding: 5px;")
        player2_layout.addWidget(self.score2_input)
        score_layout.addLayout(player2_layout)

        layout.addLayout(score_layout)

        # Предупреждение
        warning_label = QLabel("⚠️ В турнире на выбывание не может быть ничьей!")
        warning_label.setStyleSheet("color: #FF9800; font-size: 11px;")
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(warning_label)

        # Кнопки
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_result)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def save_result(self):
        """Сохранить результат матча"""
        score1 = self.score1_input.value()
        score2 = self.score2_input.value()

        if score1 == score2:
            QMessageBox.warning(self, "Ошибка", "В турнире на выбывание не может быть ничьей!")
            return

        # Определяем результат на основе счета
        if score1 > score2:
            result = MatchResult.PLAYER1_WIN
            winner_name = self.match.player1.user.username if self.match.player1 else "Игрок 1"
        else:
            result = MatchResult.PLAYER2_WIN
            winner_name = self.match.player2.user.username if self.match.player2 else "Игрок 2"

        # Подтверждение
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Победитель: {winner_name}\nСчет: {score1} - {score2}\n\nПодтвердить результат?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            self.controller.update_match_result(
                self.match.id, score1, score2, result
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить результат:\n{e}")