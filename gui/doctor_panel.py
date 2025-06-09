from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QCheckBox, QTextEdit, QHBoxLayout, QScrollArea, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,    QFrame
)
from services.assignments import get_patients_for_doctor
from services.lab_orders import create_lab_order
from services.lab_tests import get_all_lab_tests
from services.lab_orders import create_lab_order, get_orders_by_doctor, get_order_by_id

class DoctorPanel(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Doctor Panel")

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
            QComboBox, QTextEdit {
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
                QScrollBar:vertical {
                border: none;
                background: #f2e6ff;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #b38ee3;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        layout = QVBoxLayout(self)
        tabs = QTabWidget()

        self.new_order_tab = QWidget()
        new_order_layout = QVBoxLayout()

        self.patient_select = QComboBox()
        self.patients = get_patients_for_doctor(self.user.id)
        for p in self.patients:
            self.patient_select.addItem(f"{p.first_name} {p.last_name} ({p.login})", p.id)
        new_order_layout.addWidget(QLabel("Select patient:"))
        new_order_layout.addWidget(self.patient_select)
        self.patient_select.setStyleSheet("padding: 12px; border: 1px solid #f2e6ff;")

        self.test_checks = []
        test_layout = QVBoxLayout()
        self.tests = get_all_lab_tests()
        for test in self.tests:
            check = QCheckBox(test.name)
            check.test_id = test.id
            self.test_checks.append(check)
            test_layout.addWidget(check)

        scroll = QScrollArea()
        test_widget = QWidget()
        test_widget.setLayout(test_layout)
        scroll.setWidget(test_widget)
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(150)
        new_order_layout.addWidget(QLabel("Select tests:"))
        new_order_layout.addWidget(scroll)

        self.priority_select = QComboBox()
        self.priority_select.addItem("Normal", "normal")
        self.priority_select.addItem("Urgent", "urgent")
        new_order_layout.addWidget(QLabel("Priority:"))
        new_order_layout.addWidget(self.priority_select)
        self.priority_select.setStyleSheet("padding: 12px; border: 1px solid #f2e6ff;")
        self.notes_input = QTextEdit()
        new_order_layout.addWidget(QLabel("Additional notes:"))
        new_order_layout.addWidget(self.notes_input)

        self.btn_preview = QPushButton("Preview Order")
        self.btn_preview.clicked.connect(self.show_summary)
        new_order_layout.addWidget(self.btn_preview)

        self.new_order_tab.setLayout(new_order_layout)
        tabs.addTab(self.new_order_tab, "Create New Order")

        self.order_history_tab = QWidget()
        history_layout = QVBoxLayout()
        self.order_table = QTableWidget()
        history_layout.addWidget(QLabel("Order History:"))
        self.order_history_tab.setStyleSheet("background-color: #f5ebff;")
        history_layout.addWidget(self.order_table)
        self.order_history_tab.setLayout(history_layout)
        self.load_order_history()
        tabs.addTab(self.order_history_tab, "Order History")

        self.results_tab = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_tab.setLayout(self.results_layout)
        tabs.addTab(self.results_tab, "Patient Results")

        self.load_patient_results()

        layout.addWidget(tabs)
        self.setLayout(layout)

    def show_summary(self):
        patient = self.patient_select.currentText()
        patient_id = self.patient_select.currentData()
        selected_checks = [c for c in self.test_checks if c.isChecked()]

        if not selected_checks:
            QMessageBox.warning(self, "No tests selected", "Please select at least one test.")
            return

        selected_tests = [check.text() for check in selected_checks]
        test_ids = [check.test_id for check in selected_checks]
        notes = self.notes_input.toPlainText().strip()
        priority = self.priority_select.currentText()

        summary = f"<b>Patient:</b> {patient}<br><b>Priority:</b> {priority}<br><b>Tests:</b><ul>"
        for test in selected_tests:
            summary += f"<li>{test}</li>"
        summary += "</ul>"
        if notes:
            summary += f"<b>Notes:</b><br>{notes}"

        reply = QMessageBox.question(
            self, "Confirm Lab Order", summary,
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )

        if reply == QMessageBox.StandardButton.Ok:
            self.submit_order(patient_id, test_ids, notes, priority)

    def submit_order(self, patient_id, test_ids, notes, priority):
        create_lab_order(self.user.id, patient_id, test_ids, notes, priority)
        QMessageBox.information(self, "Order Created", "Lab order has been successfully submitted.")
        self.load_order_history() 
        for check in self.test_checks:
            check.setChecked(False)
        self.notes_input.clear()
        self.priority_select.setCurrentIndex(0)

    def load_order_history(self):
        orders = get_orders_by_doctor(self.user.id)
        self.order_table.setRowCount(len(orders))
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["Patient", "Tests", "Date", "Status", "Priority"])

        for row, order in enumerate(orders):
            self.order_table.setItem(row, 0, QTableWidgetItem(order.patient_name))
            item = QTableWidgetItem(", ".join(order.test_names))
            item.setTextAlignment(0x0080)  # Qt.AlignLeft | Qt.AlignTop
            item.setToolTip(", ".join(order.test_names))
            self.order_table.setItem(row, 1, item)
            self.order_table.setItem(row, 2, QTableWidgetItem(order.created_at.strftime("%Y-%m-%d %H:%M")))
            self.order_table.setItem(row, 3, QTableWidgetItem(order.status))
            self.order_table.setItem(row, 4, QTableWidgetItem(order.priority))

        header = self.order_table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.order_table.resizeRowsToContents()

    def load_patient_results(self):
        orders = get_orders_by_doctor(self.user.id)
        completed = [o for o in orders if o.status.lower() == "completed"]
        completed.sort(key=lambda o: o.created_at, reverse=True)

        for summary in completed:
            order = get_order_by_id(summary.id)  # 👈 pobranie pełnych danych

            label = QLabel(
                f"Patient: {order.patient.first_name} {order.patient.last_name} • "
                f"Date: {order.date_created.strftime('%Y-%m-%d %H:%M')} • "
                f"Tests: {len(order.items)}"
            )
            label.setStyleSheet("font-size: 14px; color: #51227e;")
            self.results_layout.addWidget(label)

            toggle_btn = QPushButton("Show Results")
            toggle_btn.setCheckable(True)
            toggle_btn.setChecked(False)
            result_box = QFrame()
            result_box.setVisible(False)
            result_box.setStyleSheet("background-color: #f5ebff; border-radius: 8px;")
            result_layout = QVBoxLayout(result_box)

            for item in order.items:
                result_label = QLabel(f"{item.test.name}: {item.result_value or '-'} {item.test.unit or ''} "
                                    f"(Ref: {item.test.ref_min}-{item.test.ref_max})  "
                                    f"[{item.liw_flag or '-'}]")
                result_label.setStyleSheet("font-size: 13px; color: #7838b5;")
                result_layout.addWidget(result_label)

            # pdf_btn = QPushButton("Download PDF")
            # pdf_btn.clicked.connect(lambda _, o=order: generate_pdf(o, f"lab_results_{o.id}.pdf"))
            # result_layout.addWidget(pdf_btn)

            toggle_btn.toggled.connect(lambda checked, box=result_box: box.setVisible(checked))
            self.results_layout.addWidget(toggle_btn)
            self.results_layout.addWidget(result_box)

            sep = QFrame()
            sep.setFrameShape(QFrame.HLine)
            sep.setFrameShadow(QFrame.Sunken)
            self.results_layout.addWidget(sep)

