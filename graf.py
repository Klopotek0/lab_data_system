from graphviz import Digraph

# Create a graph
dot = Digraph(comment='Database Schema', format='png')
dot.attr(rankdir='LR')

# Nodes for tables
dot.node('User', '''User
---------------
id (PK)
login
pw_hash
role
first_name
last_name
birthdate
is_approved''')

dot.node('PatientDoctorLink', '''PatientDoctorLink
-----------------------
id (PK)
patient_id (FK)
doctor_id (FK)''')

dot.node('LabTest', '''LabTest
----------------
id (PK)
name
unit
ref_min
ref_max''')

dot.node('LabOrder', '''LabOrder
-----------------
id (PK)
doctor_id (FK)
patient_id (FK)
date_created
priority
notes
status''')

dot.node('LabOrderItem', '''LabOrderItem
---------------------
id (PK)
order_id (FK)
test_id (FK)
result_value
liw_flag''')

# Edges for relationships
dot.edge('PatientDoctorLink', 'User', label='patient_id → id')
dot.edge('PatientDoctorLink', 'User', label='doctor_id → id')
dot.edge('LabOrder', 'User', label='doctor_id → id')
dot.edge('LabOrder', 'User', label='patient_id → id')
dot.edge('LabOrderItem', 'LabOrder', label='order_id → id')
dot.edge('LabOrderItem', 'LabTest', label='test_id → id')

# Save to file
output_path = 'C:/Users/olakr/OneDrive/Pulpit/TM/lab_data_system/db_schema_graph.png'
dot.render(output_path, cleanup=True)

output_path
