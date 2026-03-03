from database import SessionLocal
from models import User, AccessLevel
from .security import Security

class UserController:
    def __init__(self):
        self.db_session = SessionLocal()

    def get_user(self, username):
        return self.db_session.query(User).filter(User.username == username).first()

    def create_user(self, username, password, access_level='Пользователь'):
        hashed_password = Security.hash_password(password)
        level = self.get_access_level(access_level)
        user = User(username=username, password=hashed_password, access_level=level)
        self.db_session.add(user)
        self.db_session.commit()

    def get_access_level(self, level_name):
        level = self.db_session.query(AccessLevel).filter(AccessLevel.name == level_name).first()
        if not level:
            level = AccessLevel(name=level_name)
            self.db_session.add(level)
            self.db_session.commit()
        return level

    def update_user(self, user_id, data):
        user = self.db_session.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            self.db_session.commit()

    def delete_user(self, user_id):
        user = self.db_session.query(User).filter(User.id == user_id).first()
        if user:
            self.db_session.delete(user)
            self.db_session.commit()