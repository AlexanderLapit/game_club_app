import re

def validate_phone(phone):
    pattern = r'^(\+\d{1,3}|\d)?\s*$?\d{3}$?[-\.\s]?\d{3}[-\.\s]?\d{4}$'
    return re.match(pattern, phone) is not None

def validate_inn(inn):
    pattern = r'^\d{10,12}$'
    return re.match(pattern, inn) is not None

def validate_non_empty(value):
    return bool(value and value.strip())

def validate_name(name):
    if not validate_non_empty(name):
        return False
    return bool(re.match(r'^[а-яА-ЯёЁ\s\-]+$', name.strip()))

def is_valid_name(name):
    return validate_name(name)

def is_valid_login(login):
    if not validate_non_empty(login):
        return False
    return bool(re.match(r'^\w{3,20}$', login))