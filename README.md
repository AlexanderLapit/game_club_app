game_club_app/
│
├── src/                            # Исходный код проекта
│   ├── models/                     # Модели данных (ORM)
│   │   ├── __init__.py
│   │   ├── user.py                 # модель пользователя
│   │   ├── customer.py             # модель клиента
│   │   ├── product.py              # модель продукта
│   │   ├── order.py                # модель заказа
│   │   ├── material.py             # модель материалов
│   │   └── access_levels.py        # модель уровней доступа (Admin/User)
│   │
│   ├── views/                      # GUI компоненты (PyQt6)
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── login_form.py
│   │   ├── registration_form.py
│   │   ├── captcha_dialog.py         # диалог капчи
│   │   ├── order_form.py
│   │   └── user_management.py        # управление пользователями (для админа)
│   │
│   ├── controllers/                # Логика взаимодействия
│   │   ├── __init__.py
│   │   ├── auth_controller.py        # авторизация, капча
│   │   ├── main_controller.py        # запуск и управление основным интерфейсом
│   │   ├── order_controller.py       # управление заказами
│   │   ├── user_controller.py        # управление пользователями (CRUD, уровни доступа)
│   │   └── security.py               # хэширование паролей, защита
│   │
│   ├── database/                   # Работа с базой данных
│   │   ├── __init__.py
│   │   ├── db.py                   # подключение к базе, сессии
│   │   └── models.py               # регистрация ORM моделей
│   │
│   ├── utils/                      # Вспомогательные функции
│   │   ├── captcha.py                # сборка и проверка пазла
│   │   ├── validators.py             # валидация данных
│   │   └── constants.py              # константы (например, уровни доступа)
│   │
│   ├── config.py                   # Конфигурации (подключение, параметры)
│   ├── main.py
│   │── admin.py
│   └── app.py                      # Инициализация и запуск приложения
│
├── tests/                          # Тесты
│   ├── test_models.py
│   ├── test_controllers.py
│
└── README.md                       # Описание проекта