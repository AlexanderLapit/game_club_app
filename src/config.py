import os

# Настройки базы данных
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/game_club"  # ← исправлен пароль

# Другие параметры
APP_TITLE = "Клуб настольных игр"
APP_VERSION = "1.0.0"

# Параметры капчи
CAPTCHA_PARTS = 4  # количество частей пазла
CAPTCHA_PATH = "images/captcha_full.png"  # путь к изображению для капчи

# Параметры уровней доступа
ACCESS_LEVELS = {
    'Администратор': 1,
    'Пользователь': 2,
}

# Максимальное число попыток входа
MAX_LOGIN_ATTEMPTS = 3