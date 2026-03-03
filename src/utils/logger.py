import logging
from datetime import datetime

logging.basicConfig(
    filename=f'app_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    encoding='utf-8'
)

def log_action(user: str, action: str):
    logging.info(f"Пользователь: {user} | Действие: {action}")