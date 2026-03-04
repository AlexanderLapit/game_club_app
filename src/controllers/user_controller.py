from database import SessionLocal
from models import User, AccessLevel


class UserController:
    def __init__(self, session=None):
        self.db_session = session or SessionLocal()

    def get_user(self, username):
        """Получить пользователя по логину"""
        return self.db_session.query(User).filter(User.username == username).first()

    def get_all_users(self):
        """Получить всех пользователей с их уровнями доступа"""
        return self.db_session.query(User).all()

    def create_user(self, username, password, access_level='Пользователь'):
        """Создать нового пользователя"""
        from utils.security import Security
        hashed_password = Security.hash_password(password)
        level = self.get_access_level(access_level)
        user = User(username=username, password=hashed_password, access_level=level)
        self.db_session.add(user)
        self.db_session.commit()
        return user

    def get_access_level(self, level_name):
        """Получить или создать уровень доступа"""
        level = self.db_session.query(AccessLevel).filter(AccessLevel.name == level_name).first()
        if not level:
            level = AccessLevel(name=level_name)
            self.db_session.add(level)
            self.db_session.commit()
        return level

    def update_user(self, user_id, data):
        """Обновить данные пользователя"""
        user = self.db_session.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            self.db_session.commit()
        return user

    def delete_user(self, user_id):
        """Удалить пользователя"""
        user = self.db_session.query(User).filter(User.id == user_id).first()
        if user:
            self.db_session.delete(user)
            self.db_session.commit()

    def close(self):
        """Закрыть сессию"""
        if self.db_session:
            self.db_session.close()

    def __del__(self):
        self.close()