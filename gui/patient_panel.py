from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QHBoxLayout, QFrame, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from services.assignments import get_doctor_for_patient
from services.lab_orders import get_orders_by_patient
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

class PatientPanel(QWidget):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Patient Panel")
        self.user = user

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
                border-radius: 12px;
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
                padding: 6px 14px;
                border-radius: 12px;
                font-size: 15px;
                font-family: 'Raleway';
            }
            QPushButton:hover {
                background-color: #682da1;
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

        # Tab: Orders
        self.order_tab = QWidget()
        self.order_layout = QVBoxLayout()
        self.order_tab.setLayout(self.order_layout)
        self.tabs.addTab(self.order_tab, "Lab Orders")

        greeting_frame = QFrame()
        greeting_frame.setFrameShape(QFrame.StyledPanel)
        greeting_frame.setStyleSheet("""
            QFrame {
                background-color: #f5ebff;
                border-radius: 12px;
                padding: 4px;
                margin-bottom: 5px;
            }
        """)
        self.order_layout.addWidget(QLabel(f"Welcome, {self.user.first_name} {self.user.last_name}"))

        greeting_layout = QVBoxLayout()
        greeting_frame.setLayout(greeting_layout)

        doctor = get_doctor_for_patient(user.id)
        if doctor:
            greeting_layout.addWidget(QLabel(f"Your assigned doctor: {doctor.first_name} {doctor.last_name}"))
        else:
            greeting_layout.addWidget(QLabel("You have no assigned doctor yet. Please wait for assignment."))

        self.order_layout.addWidget(greeting_frame)
        self.order_layout.addWidget(QLabel("Your Lab Orders:"))

        self.order_table = QTableWidget()
        self.order_layout.addWidget(self.order_table)

        # Tab: Completed Tests
        self.completed_tab = QWidget()
        self.completed_layout = QVBoxLayout()
        self.completed_tab.setLayout(self.completed_layout)
        self.tabs.addTab(self.completed_tab, "Completed Tests")

        self.load_orders()

    def load_orders(self):
        orders = get_orders_by_patient(self.user.id)
        pending_orders = sorted(
            [o for o in orders if getattr(o, "status", "").lower() != "completed"],
            key=lambda o: o.date_created,
            reverse=True
        )

        completed_orders = sorted(
            [o for o in orders if getattr(o, "status", "").lower() == "completed"],
            key=lambda o: o.date_created,
            reverse=True
        )

        self.order_table.setRowCount(len(pending_orders))
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["Date", "Doctor", "Tests", "Priority", "Status"])

        for row, order in enumerate(pending_orders):
            self._set_item(self.order_table, row, 0, order.date_created.strftime("%Y-%m-%d %H:%M"))
            doctor_name = f"{order.doctor.first_name} {order.doctor.last_name}"
            self._set_item(self.order_table, row, 1, doctor_name)
            tests = ", ".join([item.test.name for item in order.items])
            self._set_item(self.order_table, row, 2, tests)
            self._set_item(self.order_table, row, 3, order.priority.capitalize())
            self._set_item(self.order_table, row, 4, order.status)

        header = self.order_table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(2, QHeaderView.Stretch)          
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  

        self.order_table.resizeRowsToContents()

        for order in completed_orders:
            doctor_name = f"{order.doctor.first_name} {order.doctor.last_name}"
            test_count = len(order.items)
            completed_label = QLabel(
                f"Order placed on: {order.date_created.strftime('%Y-%m-%d %H:%M')}\n"
                f"Results received on: {order.date_created.strftime('%Y-%m-%d %H:%M')}\n"
                f"Ordered by: {doctor_name}\n"
                f"Number of tests: {test_count}"
            )
            completed_label.setStyleSheet("font-weight: 300; font-size: 14px;")
            self.completed_layout.addWidget(completed_label)

            header = QPushButton("Show Results")
            header.setCheckable(True)
            header.setChecked(False)
            pdf_btn = QPushButton("Download PDF")
            pdf_btn.clicked.connect(lambda _, o=order: generate_pdf(o, f"lab_results_{o.id}.pdf"))

            frame = QFrame()
            frame.setVisible(False)
            frame.setFrameShape(QFrame.StyledPanel)
            frame_layout = QVBoxLayout()
            frame.setLayout(frame_layout)

            for item in order.items:
                line = QLabel(f"{item.test.name}: {item.result_value or '-'} {item.test.unit or ''}  "
                            f"(Ref: {item.test.ref_min or '-'}-{item.test.ref_max or '-'})  "
                            f"[{item.liw_flag or '-'}]")
                line.setStyleSheet("font-weight: light; font-size: 13px; color: #7838b5;")
                frame_layout.addWidget(line)

            frame_layout.addWidget(pdf_btn)

            def toggle(checked, f=frame):
                f.setVisible(checked)
            header.toggled.connect(toggle)

            self.completed_layout.addWidget(header)
            self.completed_layout.addWidget(frame)

            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            self.completed_layout.addWidget(separator)


    def _set_item(self, table, row, column, text):
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        item.setForeground(QColor("#51227e"))
        table.setItem(row, column, item)

def generate_pdf(order, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin = 2 * cm
    current_y = height - margin

    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, current_y, "Laboratory Results")
    current_y -= 1.2 * cm

    c.setFont("Helvetica", 10)
    c.drawString(margin, current_y, f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    current_y -= 0.8 * cm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, current_y, "Patient Information")
    current_y -= 0.6 * cm
    c.setFont("Helvetica", 10)
    c.drawString(margin, current_y, f"Name: {order.patient.first_name} {order.patient.last_name}")
    current_y -= 0.5 * cm
    c.drawString(margin, current_y, f"Doctor: {order.doctor.first_name} {order.doctor.last_name}")
    current_y -= 0.8 * cm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, current_y, "Test Results")
    current_y -= 0.6 * cm

    data = [["Test", "Result", "Unit", "Reference Range", "LIW Flag"]]
    for item in order.items:
        data.append([
            item.test.name,
            str(item.result_value) if item.result_value is not None else "-",
            item.test.unit or "-",
            f"{item.test.ref_min}-{item.test.ref_max}",
            item.liw_flag or "-"
        ])

    table = Table(data, colWidths=[6*cm, 2.5*cm, 2.5*cm, 4*cm, 2.5*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d2c0ec")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#51227e")),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5ebff")]),
    ]))

    table.wrapOn(c, width - 2 * margin, current_y)
    table_height = table._height
    table.drawOn(c, margin, current_y - table_height)

    c.showPage()
    c.save()
