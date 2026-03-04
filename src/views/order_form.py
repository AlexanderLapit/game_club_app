from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QSpinBox, QDoubleSpinBox, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt


class OrderForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📦 Создание заказа")
        self.resize(800, 500)
        self.items = []
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f5eb;
                font-family: "Segoe UI";
            }
            QLabel {
                color: #4b3c27;
            }
            QTableWidget {
                background-color: white;
                gridline-color: #e8e0d0;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #e8e0d0;
                color: #4b3c27;
                padding: 6px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #d4c8a5;
                color: #4b3c27;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton#delete_btn {
                background-color: #e5b8b7;
                color: #5e2c24;
            }
            QPushButton#delete_btn:hover {
                background-color: #ffcccc;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: white;
                border: 1px solid #d0c4a8;
                border-radius: 6px;
                padding: 4px;
            }
        """)

        layout = QVBoxLayout()
        title = QLabel("Форма создания заказа")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Товар", "Кол-во", "Цена", "ИТОГО", ""])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.btn_add = QPushButton("+ Добавить товар")
        self.btn_save = QPushButton("✅ Сохранить заказ")
        self.btn_cancel = QPushButton("❌ Отмена")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        self.total_label = QLabel("Общая сумма: 0.00 руб")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.total_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")

        layout.addLayout(btn_layout)
        layout.addWidget(self.total_label)
        self.setLayout(layout)

    def connect_signals(self):
        self.btn_add.clicked.connect(self.add_product_row)
        self.btn_save.clicked.connect(self.save_order)
        self.btn_cancel.clicked.connect(self.close)

    def add_product_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        name = QLineEdit()
        name.setPlaceholderText("Название товара")
        quantity = QSpinBox()
        quantity.setRange(1, 9999)
        price = QDoubleSpinBox()
        price.setRange(0.01, 1_000_000.00)
        total = QLabel("0.00")
        remove_btn = QPushButton("×")
        remove_btn.setObjectName("delete_btn")
        remove_btn.setFixedSize(30, 30)

        self.table.setCellWidget(row, 0, name)
        self.table.setCellWidget(row, 1, quantity)
        self.table.setCellWidget(row, 2, price)
        self.table.setCellWidget(row, 3, total)
        self.table.setCellWidget(row, 4, remove_btn)

        quantity.valueChanged.connect(lambda: self.update_row_total(row))
        price.valueChanged.connect(lambda: self.update_row_total(row))
        remove_btn.clicked.connect(lambda: self.remove_row(row))

        self.update_row_total(row)

    def update_row_total(self, row):
        qty = self.table.cellWidget(row, 1).value()
        price = self.table.cellWidget(row, 2).value()
        total = qty * price
        self.table.cellWidget(row, 3).setText(f"{total:.2f}")
        self.update_grand_total()

    def update_grand_total(self):
        total = sum(
            float(self.table.cellWidget(row, 3).text())
            for row in range(self.table.rowCount())
        )
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
            if name_w.text().strip():
                items.append({
                    'name': name_w.text(),
                    'quantity': qty_w.value(),
                    'price': price_w.value()
                })

        if not items:
            QMessageBox.warning(self, "⚠️ Ошибка", "Добавьте хотя бы один товар")
            return

        total = sum(i['quantity'] * i['price'] for i in items)
        QMessageBox.information(
            self, "✅ Успех",
            f"Заказ на сумму {total:.2f} руб успешно создан!"
        )
        self.close()