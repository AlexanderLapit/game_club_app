from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap
from utils.captcha import Captcha

class CaptchaDialog(QDialog):
    def __init__(self, captcha_service: Captcha):
        super().__init__()
        self.setWindowTitle("Решите капчу")
        self.resize(400, 400)
        self.captcha_service = captcha_service

        self.layout = QVBoxLayout()

        # Отображение изображения
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap(captcha_service.get_image_path()))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)

        # Кнопки
        self.btn_solve = QPushButton("Решить пазл")
        self.btn_submit = QPushButton("Проверить")
        self.btn_cancel = QPushButton("Отмена")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_solve)
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)

        self.layout.addWidget(self.image_label)
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

        # Логика
        self.btn_solve.clicked.connect(self.on_solve)
        self.btn_submit.clicked.connect(self.on_submit)
        self.btn_cancel.clicked.connect(self.reject)

    def on_solve(self):
        self.captcha_service.solve()
        QMessageBox.information(self, "Готово", "Пазл собран!")

    def on_submit(self):
        if self.captcha_service.verify():
            QMessageBox.information(self, "Успех", "Капча пройдена!")
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Сначала решите пазл!")