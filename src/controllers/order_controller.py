from database import SessionLocal
from models import Order, User


class OrderController:
    def __init__(self, session=None):
        self.db_session = session or SessionLocal()

    def create_order(self, customer_id, items):
        customer = self.db_session.query(User).get(customer_id)
        if not customer:
            raise ValueError("Клиент не найден")

        if not items or not isinstance(items, list):
            raise ValueError("Требуется список элементов заказа")

        total_amount = sum(item['quantity'] * item['price'] for item in items)
        order = Order(customer_id=customer_id, total_amount=total_amount)
        self.db_session.add(order)
        self.db_session.commit()
        return order

    def get_orders(self):
        return self.db_session.query(Order).all()

    def close(self):
        self.db_session.close()

    def __del__(self):
        self.close()