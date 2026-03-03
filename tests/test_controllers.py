import unittest
from controllers import UserController
from database import SessionLocal
from models import User, AccessLevel

class TestUserController(unittest.TestCase):
    def setUp(self):
        self.session = SessionLocal()
        self.user_ctrl = UserController()

    def tearDown(self):
        self.session.close()

    def test_create_and_get_user(self):
        level = self.session.query(AccessLevel).first()
        self.user_ctrl.create_user('testuser2', 'password123', 'Пользователь')
        user = self.user_ctrl.get_user('testuser2')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser2')

if __name__ == '__main__':
    unittest.main()