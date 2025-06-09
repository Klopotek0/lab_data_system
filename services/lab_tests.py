from models import LabTest
from database import Session

def get_all_lab_tests():
    session = Session()
    tests = session.query(LabTest).all()
    session.close()
    return tests
