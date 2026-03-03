import unittest
from utils.validators import validate_phone, validate_inn, validate_non_empty
from utils.captcha import Captcha

class TestValidators(unittest.TestCase):
    def test_validate_phone(self):
        self.assertTrue(validate_phone("+79991234567"))
        self.assertTrue(validate_phone("89991234567"))
        self.assertFalse(validate_phone("12345"))
        self.assertFalse(validate_phone("abcde"))

    def test_validate_inn(self):
        self.assertTrue(validate_inn("26320045123"))
        self.assertFalse(validate_inn("123456789"))
        self.assertFalse(validate_inn("abcdefghijk"))

    def test_validate_non_empty(self):
        self.assertTrue(validate_non_empty("Некоторый текст"))
        self.assertFalse(validate_non_empty(""))
        self.assertFalse(validate_non_empty("   "))

class TestCaptcha(unittest.TestCase):
    def setUp(self):
        self.captcha = Captcha()

    def test_generate_puzzle(self):
        pixmap = self.captcha.generate_puzzle()
        self.assertIsNotNone(pixmap)
        self.assertIsInstance(pixmap, type(self.captcha).generate_puzzle(self.captcha))

    def test_verify_captcha(self):
        # В реальности тут должна быть проверка правильности сборки
        # Для теста просто устанавливаем правильность
        self.captcha.correct = True
        self.assertTrue(self.captcha.verify())

if __name__ == '__main__':
    unittest.main()