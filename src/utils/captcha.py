import random
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel
from config import CAPTCHA_PATH

class Captcha:
    def __init__(self):
        self.puzzle_image_path = CAPTCHA_PATH
        self.is_solved = False

    def get_image_path(self):
        """Возвращает путь к изображению для отображения."""
        return self.puzzle_image_path

    def solve(self):
        """Моделирует правильное решение пазла."""
        self.is_solved = True

    def reset(self):
        """Сброс состояния капчи."""
        self.is_solved = False

    def verify(self):
        """Проверяет, решена ли капча."""
        return self.is_solved