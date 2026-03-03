import unittest
from PyQt6.QtWidgets import QApplication
from main import main

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])

    def test_app_launch(self):
        # Проверка запуска главного окна
        main()

    def tearDown(self):
        self.app.quit()

if __name__ == '__main__':
    unittest.main()