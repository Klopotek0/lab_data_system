from models import LabOrder, LabOrderItem
import datetime
from database import Session
from sqlalchemy.orm import joinedload

def create_lab_order(doctor_id, patient_id, test_ids, notes="", priority="normal"):
    session = Session()
    order = LabOrder(
        doctor_id=doctor_id,
        patient_id=patient_id,
        notes=notes,
        priority=priority,
        date_created=datetime.datetime.utcnow()
    )
    session.add(order)
    session.commit()

    for test_id in test_ids:
        item = LabOrderItem(order_id=order.id, test_id=test_id)
        session.add(item)

    session.commit()
    session.close()
    return order

def get_orders_by_doctor(doctor_id):
    session = Session()
    orders = (
        session.query(LabOrder)
        .options(
            joinedload(LabOrder.patient),
            joinedload(LabOrder.items).joinedload(LabOrderItem.test)
        )
        .filter(LabOrder.doctor_id == doctor_id)
        .order_by(LabOrder.date_created.desc())
        .all()
    )

    result = []
    for order in orders:
        test_names = [item.test.name for item in order.items]
        result.append(
            type("OrderSummary", (object,), {
                "id": order.id,
                "patient_name": f"{order.patient.first_name} {order.patient.last_name}",
                "test_names": test_names,
                "priority": order.priority,
                "status": getattr(order, "status", "Pending"),
                "created_at": order.date_created,
            })()
        )

    session.close()
    return result

def get_orders_by_patient(patient_id):
    session = Session()
    orders = (
        session.query(LabOrder)
        .options(
            joinedload(LabOrder.doctor),
            joinedload(LabOrder.patient),
            joinedload(LabOrder.items).joinedload(LabOrderItem.test)
        )
        .filter_by(patient_id=patient_id)
        .all()
    )
    session.close()
    return orders

def get_open_orders():
    session = Session()
    orders = session.query(LabOrder)\
    .options(
        joinedload(LabOrder.items).joinedload(LabOrderItem.test),
        joinedload(LabOrder.doctor),
        joinedload(LabOrder.patient)
    )\
    .filter((LabOrder.status != "completed") | (LabOrder.status == None))\
    .all()
    session.expunge_all()
    session.close()
    return orders

def add_lab_result(order_id: int, result_text: str):
    session = Session()
    order = session.query(LabOrder).get(order_id)
    if order:
        order.result = result_text
        order.status = "completed"
        session.commit()
    session.close()

def update_order_status(order_id, status):
    session = Session()
    order = session.query(LabOrder).get(order_id)
    if order:
        order.status = status
        session.commit()
    session.close()

def save_test_result(order_item_id: int, value: str):
    session = Session()
    try:
        item = session.query(LabOrderItem).get(order_item_id)
        if item:
            item.result_value = value
            try:
                result_num = float(value)
                if result_num < item.test.ref_min:
                    item.liw_flag = "L"
                elif result_num > item.test.ref_max:
                    item.liw_flag = "H"
                else:
                    item.liw_flag = "N"
            except ValueError:
                item.liw_flag = "?"
            session.commit()
    finally:
        session.close()

def get_order_by_id(order_id):
    session = Session()
    return session.query(LabOrder).filter_by(id=order_id).first()
