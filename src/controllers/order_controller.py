from database import SessionLocal
from models import Order

class OrderController:
    def __init__(self):
        self.db_session = SessionLocal()

    def create_order(self, customer_id, items):
        total_amount = self.calculate_total(items)
        order = Order(customer_id=customer_id, total_amount=total_amount)
        self.db_session.add(order)
        self.db_session.commit()

    def calculate_total(self, items):
        total = 0.0
        for item in items:
            total += item['quantity'] * item['price']
        return total

    def get_orders(self):
        return self.db_session.query(Order).all()

    def delete_order(self, order_id):
        order = self.db_session.query(Order).filter(Order.id == order_id).first()
        if order:
            self.db_session.delete(order)
            self.db_session.commit()