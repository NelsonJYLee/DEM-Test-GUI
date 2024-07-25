from PyQt5.QtWidgets import QWidget, QLineEdit, QFormLayout, QDateEdit
from PyQt5.QtCore import QDate

class PatientInfoPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate())
        self.age_input = QLineEdit()
        
        self.layout.addRow('Name:', self.name_input)
        self.layout.addRow('Date of Birth:', self.dob_input)
        self.layout.addRow('Age:', self.age_input)
        
        self.setLayout(self.layout)

    def get_patient_info(self):
        name = self.name_input.text()
        dob = self.dob_input.date().toString('yyyy-MM-dd')
        age = self.age_input.text()
        return name, dob, age