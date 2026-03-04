import os
import random
from PIL import Image
from config import CAPTCHA_PATH, IMAGES_DIR

ROWS, COLS = 2, 2
TOTAL_PARTS = ROWS * COLS  # 4 части

class Captcha:
    def __init__(self):
        self.pieces = []
        self.solution_order = list(range(TOTAL_PARTS))
        self.current_order = self.solution_order[:]
        self.is_solved = False
        self.image_width = 0
        self.image_height = 0
        self.piece_width = 0
        self.piece_height = 0
        self.generate_puzzle()

    def generate_puzzle(self):
        """Разрезает изображение и перемешивает части."""
        try:
            if not os.path.exists(CAPTCHA_PATH):
                raise FileNotFoundError(f"Файл не найден: {CAPTCHA_PATH}")

            img = Image.open(CAPTCHA_PATH)
            self.image_width, self.image_height = img.size
            self.piece_width = self.image_width // COLS
            self.piece_height = self.image_height // ROWS

            parts_dir = os.path.join(IMAGES_DIR, "puzzle_parts")
            os.makedirs(parts_dir, exist_ok=True)

            for i in range(TOTAL_PARTS):
                path = os.path.join(parts_dir, f"part_{i}.png")
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            self.pieces = []
            for row in range(ROWS):
                for col in range(COLS):
                    left = col * self.piece_width
                    top = row * self.piece_height
                    right = left + self.piece_width
                    bottom = top + self.piece_height
                    piece = img.crop((left, top, right, bottom))
                    piece_path = os.path.join(parts_dir, f"part_{len(self.pieces)}.png")
                    piece.save(piece_path)
                    self.pieces.append(piece_path)

            self.current_order = list(range(TOTAL_PARTS))
            while self.current_order == self.solution_order:
                random.shuffle(self.current_order)

            self.is_solved = False

        except Exception as e:
            print(f"[Ошибка генерации] {e}")
            # Заглушка
            self.pieces = [CAPTCHA_PATH] * TOTAL_PARTS
            self.current_order = [1, 0, 3, 2]
            self.is_solved = False

    def get_piece_path(self, index):
        """Возвращает путь к части по текущему порядку."""
        if index >= len(self.current_order):
            return CAPTCHA_PATH
        piece_idx = self.current_order[index]
        return self.pieces[piece_idx] if piece_idx < len(self.pieces) else CAPTCHA_PATH

    def click_piece(self, index):
        """
        Меняет местами кликнутую часть со следующей (по кругу).
        Проверяет, совпадает ли текущий порядок с решением.
        """
        next_idx = (index + 1) % TOTAL_PARTS
        self.current_order[index], self.current_order[next_idx] = \
            self.current_order[next_idx], self.current_order[index]

        if self.current_order == self.solution_order:
            self.is_solved = True

    def verify(self):
        """Проверяет, решена ли капча."""
        return self.is_solved

    def solve(self):
        """Явно помечает капчу как решённую (на случай, если нужно принудительно)."""
        self.is_solved = True

    def reset(self):
        """Сбрасывает состояние и генерирует новую капчу."""
        self.is_solved = False
        self.generate_puzzle()