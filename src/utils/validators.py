import re

def validate_phone(phone):
    pattern = r'^\+?\d{10,15}$'
    return re.match(pattern, phone) is not None

def validate_inn(inn):
    pattern = r'^\d{10,12}$'
    return re.match(pattern, inn) is not None

def validate_non_empty(value):
    return bool(value and value.strip())

def validate_name(name):
    """
    Проверка ФИО: только кириллица, пробелы, дефисы.
    """
    if not validate_non_empty(name):
        return False
    return bool(re.match(r'^[а-яА-ЯёЁ\s\-]+$', name.strip()))

# --- Добавляем требуемые функции ---
def is_valid_name(name):
    """
    Совместимость с регистрационной формой.
    """
    return validate_name(name)

def is_valid_login(login):
    """
    Проверка логина: 3–20 символов, только буквы, цифры, подчёркивание.
    """
    if not validate_non_empty(login):
        return False
    return bool(re.match(r'^\w{3,20}$', login))