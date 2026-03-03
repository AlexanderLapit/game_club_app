from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpinBox, QDoubleSpinBox
from PyQt6.QtCore import Qt

class OrderForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание заказа")
        self.resize(700, 400)

        self.layout = QVBoxLayout()

        self.label = QLabel("Форма создания заказа")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Товар", "Кол-во", "Цена", "ИТОГО", "Удалить"])

        self.btn_add = QPushButton("Добавить товар")
        self.btn_save = QPushButton("Сохранить заказ")
        self.btn_cancel = QPushButton("Отмена")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        self.total_label = QLabel("Общая сумма: 0.00 руб")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)
        self.layout.addLayout(btn_layout)
        self.layout.addWidget(self.total_label)

        self.setLayout(self.layout)

        self.btn_add.clicked.connect(self.add_product_row)
        self.btn_save.clicked.connect(self.save_order)
        self.btn_cancel.clicked.connect(self.close)

    def add_product_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        name = QLineEdit()
        quantity = QSpinBox()
        quantity.setRange(1, 999)
        price = QDoubleSpinBox()
        price.setRange(0.01, 999999.99)
        total = QLabel("0.00")
        remove_btn = QPushButton("×")
        remove_btn.setStyleSheet("color: red; font-weight: bold;")

        self.table.setCellWidget(row, 0, name)
        self.table.setCellWidget(row, 1, quantity)
        self.table.setCellWidget(row, 2, price)
        self.table.setCellWidget(row, 3, total)
        self.table.setCellWidget(row, 4, remove_btn)

        # Обновление итого при изменении кол-ва или цены
        quantity.valueChanged.connect(lambda: self.update_total(row))
        price.valueChanged.connect(lambda: self.update_total(row))
        remove_btn.clicked.connect(lambda: self.remove_row(row))

    def update_total(self, row):
        qty = self.table.cellWidget(row, 1).value()
        price = self.table.cellWidget(row, 2).value()
        total = qty * price
        self.table.cellWidget(row, 3).setText(f"{total:.2f}")
        self.update_grand_total()

    def update_grand_total(self):
        total = 0.0
        for row in range(self.table.rowCount()):
            total += float(self.table.cellWidget(row, 3).text())
        self.total_label.setText(f"Общая сумма: {total:.2f} руб")

    def remove_row(self, row):
        self.table.removeRow(row)
        self.update_grand_total()

    def save_order(self):
        items = []
        for row in range(self.table.rowCount()):
            name_w = self.table.cellWidget(row, 0)
            qty_w = self.table.cellWidget(row, 1)
            price_w = self.table.cellWidget(row, 2)
            items.append({
                'name': name_w.text(),
                'quantity': qty_w.value(),
                'price': price_w.value()
            })
        # Передать в OrderController
        QMessageBox.information(self, "Сохранено", f"Заказ на сумму {self.total_label.text()} создан")
        self.close()