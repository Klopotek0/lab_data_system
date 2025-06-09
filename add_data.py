from models import LabTest
from database import Session

# lab_tests = [
#     {"name": "Morfologia krwi obwodowej z płytkami krwi"},
#     {"name": "Morfologia krwi obwodowej z wzorem odsetkowym i płytkami krwi"},
#     {"name": "Retikulocyty"},
#     {"name": "Odczyn opadania krwinek czerwonych (OB)"},
#     {"name": "Sód"},
#     {"name": "Potas"},
#     {"name": "Wapń zjonizowany"},
#     {"name": "Żelazo"},
#     {"name": "Żelazo – całkowita zdolność wiązania (TIBC)"},
#     {"name": "Stężenie transferyny"},
#     {"name": "Stężenie hemoglobiny glikowanej (HbA1c)"},
#     {"name": "Mocznik"},
#     {"name": "Kreatynina"},
#     {"name": "Glukoza"},
#     {"name": "Test obciążenia glukozą"},
#     {"name": "Białko całkowite"},
#     {"name": "Proteinogram"},
#     {"name": "Albumina"},
#     {"name": "Białko C-reaktywne (CRP)"},
#     {"name": "Kwas moczowy"},
#     {"name": "Cholesterol całkowity"},
#     {"name": "Cholesterol-HDL"},
#     {"name": "Cholesterol-LDL"},
#     {"name": "Triglicerydy (TG)"},
#     {"name": "Bilirubina całkowita"},
#     {"name": "Bilirubina bezpośrednia"},
#     {"name": "Fosfataza alkaliczna (ALP)"},
#     {"name": "Aminotransferaza asparaginianowa (AST)"},
#     {"name": "Aminotransferaza alaninowa (ALT)"},
#     {"name": "Gammaglutamylotranspeptydaza (GGTP)"},
#     {"name": "Amylaza"},
#     {"name": "Kinaza kreatynowa (CK)"},
#     {"name": "Fosfataza kwaśna całkowita (ACP)"},
#     {"name": "Czynnik reumatoidalny (RF)"},
#     {"name": "Miano antystreptolizyn O (ASO)"},
#     {"name": "Hormon tyreotropowy (TSH)"},
#     {"name": "Antygen HBs-Ag"},
#     {"name": "VDRL"},
#     {"name": "FT3"},
#     {"name": "FT4"},
#     {"name": "PSA"},
#     {"name": "Ogólne badanie moczu"},
#     {"name": "Ilościowe oznaczanie białka w moczu"},
#     {"name": "Ilościowe oznaczanie glukozy w moczu"},
#     {"name": "Ilościowe oznaczanie wapnia w moczu"},
#     {"name": "Ilościowe oznaczanie amylazy w moczu"},
#     {"name": "Badanie ogólne kału"},
#     {"name": "Badanie kału w kierunku pasożytów"},
#     {"name": "Badanie kału na krew utajoną metodą immunochemiczną"},
#     {"name": "Wskaźnik protrombinowy (INR)"},
#     {"name": "Czas kaolinowo-kefalinowy (APTT)"},
#     {"name": "Fibrynogen"},
#     {"name": "Posiew moczu z antybiogramem"},
#     {"name": "Posiew wymazu z gardła z antybiogramem"},
#     {"name": "Posiew kału w kierunku pałeczek Salmonella i Shigella"},
# ]

lab_tests_data = [
    {"name": "Sód", "unit": "mmol/L", "ref_min": 136, "ref_max": 145},
    {"name": "Potas", "unit": "mmol/L", "ref_min": 3.5, "ref_max": 5.1},
    {"name": "Wapń zjonizowany", "unit": "mmol/L", "ref_min": 1.0, "ref_max": 1.3},
    {"name": "Glukoza", "unit": "mg/dL", "ref_min": 70, "ref_max": 99},
    {"name": "Kreatynina (kobiety)", "unit": "mg/dL", "ref_min": 0.57, "ref_max": 1.11},
    {"name": "Kreatynina (mężczyźni)", "unit": "mg/dL", "ref_min": 0.72, "ref_max": 1.25},
    {"name": "Cholesterol całkowity", "unit": "mg/dL", "ref_min": 125, "ref_max": 200},
    {"name": "Cholesterol HDL (kobiety)", "unit": "mg/dL", "ref_min": 50, "ref_max": 100},
    {"name": "Cholesterol HDL (mężczyźni)", "unit": "mg/dL", "ref_min": 40, "ref_max": 100},
    {"name": "Cholesterol LDL", "unit": "mg/dL", "ref_min": 0, "ref_max": 100},
    {"name": "Triglicerydy", "unit": "mg/dL", "ref_min": 0, "ref_max": 150},
    {"name": "TSH", "unit": "µU/mL", "ref_min": 0.4, "ref_max": 4.0},
    {"name": "FT3", "unit": "pmol/L", "ref_min": 2.25, "ref_max": 6.0},
    {"name": "FT4", "unit": "pmol/L", "ref_min": 10, "ref_max": 35},
]

def seed_lab_tests():
    session = Session()
    for test in lab_tests_data:
        if not session.query(LabTest).filter_by(name=test["name"]).first():
            session.add(LabTest(
                name=test["name"],
                unit=test["unit"],
                ref_min=test["ref_min"],
                ref_max=test["ref_max"]
            ))
    session.commit()
    session.close()

seed_lab_tests()
