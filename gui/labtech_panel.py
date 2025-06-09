from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QTabWidget, QTextEdit, QComboBox, QHBoxLayout, QMessageBox, QFormLayout, QScrollArea, QHeaderView
)
from services.lab_orders import get_open_orders, update_order_status, save_test_result
from models import LabOrderItem

from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

class LabtechPanel(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Lab Technician Panel")

        self.setStyleSheet("""
            QWidget {
                background-color: #fffefe;
                border-radius: 12px;
            }
            QLabel {
                font-family: 'Raleway';
                font-size: 14px;
                color: #51227e;
            }
            QTableWidget {
                background-color: #f5ebff;
                border: 2px solid #d2c0ec;
                border-radius: 12px;
                color: #210f37;
                gridline-color: #d2c0ec;
                selection-background-color: #d2c0ec;
            }
            QHeaderView::section {
                background-color: #f5ebff;
                color: #51227e;
                padding: 4px;
                font-weight: bold;
                font-family: 'Raleway';
                border: none;
            }
            QTabBar::tab {
                background-color: #e7dcf5;
                color: #51227e;
                padding: 8px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-family: 'Raleway';
            }
            QTabBar::tab:selected {
                background-color: #d2c0ec;
                font-weight: bold;
            }
            QPushButton {
                background-color: #51227e;
                color: #fffefe;
                padding: 8px 16px;
                border-radius: 12px;
                font-size: 15px;
                font-family: 'Raleway';
            }
            QPushButton:hover {
                background-color: #682da1;
            }
            QCheckBox {
                color: #51227e;
                font-family: 'Raleway';
                padding: 2px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #51227e;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #b38ee3;
                border: 1px solid #51227e;
            }
            QComboBox, QLineEdit {
                background-color: #f2e6ff;
                color: #210f37;
                border-radius: 8px;
                padding: 6px;
                font-family: 'Raleway';
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #210f37;
                selection-background-color: #d2c0ec;
                font-family: 'Raleway';
            }
            QScrollBar:horizontal {
            border: none;
            background: #f2e6ff;
            height: 10px;
            margin: 0px 0px 0px 0px;
            border-radius: 5px;
        }

            QScrollBar::handle:horizontal {
                background: #b38ee3;
                min-width: 20px;
                border-radius: 5px;
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)

        self.tabs = QTabWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        # Tab: Open Orders
        self.orders_tab = QWidget()
        self.orders_layout = QVBoxLayout()
        self.orders_tab.setLayout(self.orders_layout)
        self.tabs.addTab(self.orders_tab, "Open Orders")

        self.orders_table = QTableWidget()
        self.orders_layout.addWidget(self.orders_table)

        # Tab: Record Results
        self.result_tab = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_tab.setLayout(self.result_layout)
        self.tabs.addTab(self.result_tab, "Record Results")

        self.result_order_select = QComboBox()
        self.result_order_select.currentIndexChanged.connect(self.load_order_items)
        self.result_layout.addWidget(QLabel("Select Order:"))
        self.result_layout.addWidget(self.result_order_select)

        # Scroll area for test results
        self.result_area = QScrollArea()
        self.result_widget = QWidget()
        self.result_form = QFormLayout()
        self.result_widget.setLayout(self.result_form)
        self.result_area.setWidgetResizable(True)
        self.result_area.setWidget(self.result_widget)
        self.result_layout.addWidget(self.result_area)

        self.btn_submit_result = QPushButton("Submit Results")
        self.btn_submit_result.clicked.connect(self.submit_results)
        self.result_layout.addWidget(self.btn_submit_result)

        self.result_inputs = {}  # order_item_id -> QTextEdit

        self.load_orders()

    def load_orders(self):
        self.orders = get_open_orders()
        self.orders_table.setRowCount(len(self.orders))
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels(["Order ID", "Date", "Doctor", "Patient", "Tests", "Status"])

        self.result_order_select.clear()

        for row, order in enumerate(self.orders):
            self.orders_table.setItem(row, 0, QTableWidgetItem(str(order.id)))
            self.orders_table.setItem(row, 1, QTableWidgetItem(order.date_created.strftime("%Y-%m-%d %H:%M")))
            self.orders_table.setItem(row, 2, QTableWidgetItem(f"{order.doctor.first_name} {order.doctor.last_name}"))
            self.orders_table.setItem(row, 3, QTableWidgetItem(f"{order.patient.first_name} {order.patient.last_name}"))

            tests = ", ".join([item.test.name for item in order.items])
            test_item = QTableWidgetItem(tests)
            test_item.setTextAlignment(0x0080)
            test_item.setToolTip(tests)
            self.orders_table.setItem(row, 4, test_item)

            status_box = QComboBox()
            status_box.addItems(["pending", "in progress", "completed"])
            status_box.setCurrentText(order.status)
            status_box.currentTextChanged.connect(lambda new_status, order_id=order.id: update_order_status(order_id, new_status))
            self.orders_table.setCellWidget(row, 5, status_box)
            self.result_order_select.addItem(f"#{order.id} - {order.patient.first_name} {order.patient.last_name}", order.id)

        header = self.orders_table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.orders_table.resizeRowsToContents()

    def load_order_items(self):
        self.result_inputs.clear()
        for i in reversed(range(self.result_form.count())):
            self.result_form.removeRow(i)

        order_id = self.result_order_select.currentData()
        order = next((o for o in self.orders if o.id == order_id), None)
        print(f"Found order with {len(order.items)} items")

        if not order:
            return
        
        for item in order.items:
            print(f"Rendering: {item.test.name}")
            label = QLabel(f"{item.test.name} ({item.test.unit}, {item.test.ref_min} - {item.test.ref_max})")
            input_field = QLineEdit()
            input_field.setFixedHeight(30)

            # Regex: dopuszcza liczby typu: 12, 12.34, 0.1, .5 – ale nie litery ani inne znaki
            regex = QRegularExpression(r'^\d*\.?\d*$')
            validator = QRegularExpressionValidator(regex)
            input_field.setValidator(validator)

            self.result_inputs[item.id] = input_field
            self.result_form.addRow(label, input_field)

    def submit_results(self):
        order_id = self.result_order_select.currentData()
        all_filled = True

        for item_id, input_widget in self.result_inputs.items():
            result_value = input_widget.text().strip()
            if not result_value or result_value == ".":
                all_filled = False
            else:
                save_test_result(item_id, result_value)

        if not all_filled:
            QMessageBox.warning(self, "Warning", "Some results were left blank.")
            return

        update_order_status(order_id, "completed")
        QMessageBox.information(self, "Saved", "Results submitted and order marked as completed.")
        self.load_orders()
        self.load_order_items()
