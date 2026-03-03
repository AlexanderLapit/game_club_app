import unittest
from database import Base, engine
from sqlalchemy.orm import sessionmaker
from models import User, AccessLevel

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    def test_create_access_level(self):
        level = AccessLevel(name='Тестовый уровень')
        self.session.add(level)
        self.session.commit()
        self.assertIsNotNone(level.id)

    def test_create_user(self):
        level = self.session.query(AccessLevel).first()
        user = User(username='testuser', password='hashed_password', access_level=level)
        self.session.add(user)
        self.session.commit()
        self.assertIsNotNone(user.id)

if __name__ == '__main__':
    unittest.main()