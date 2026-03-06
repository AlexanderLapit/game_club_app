from .auth_controller import AuthController
from .main_controller import MainController
from .order_controller import OrderController
from .user_controller import UserController
from src.utils.security import Security
from .customer_controller import CustomerController  # ← Добавлено

__all__ = [
    "AuthController",
    "MainController",
    "OrderController",
    "UserController",
    "Security",
    "CustomerController"
]