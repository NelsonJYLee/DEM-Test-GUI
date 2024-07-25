from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from gui.patient_info_page import PatientInfoPage
from gui.test_a_page import TestAPage
from patient import Patient

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DEM Test')
        self.setFixedSize(400, 300)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        self.page_one = PatientInfoPage()
        self.page_two = TestAPage()
        
        self.stacked_widget.addWidget(self.page_one)
        self.stacked_widget.addWidget(self.page_two)
        
        self.nav_layout = QHBoxLayout()  # Changed to QHBoxLayout

        self.prev_button = QPushButton('Prev')
        self.prev_button.clicked.connect(self.show_prev_page)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.show_next_page)
        
        self.nav_layout.addWidget(self.prev_button)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.next_button)
        
        self.layout.addLayout(self.nav_layout)

        self.update_nav_buttons()

        self.patient = None
        
    def show_next_page(self):
        if self.stacked_widget.currentIndex() == 0:
            self.update_patient_info()
            self.page_two.update_test_a(self.patient.name)
        current_index = self.stacked_widget.currentIndex()
        if current_index < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(current_index + 1)
        self.update_nav_buttons()
        
    def show_prev_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)
        self.update_nav_buttons()
    
    def update_nav_buttons(self):
        current_index = self.stacked_widget.currentIndex()
        self.prev_button.setEnabled(current_index > 0)
        self.next_button.setEnabled(current_index < self.stacked_widget.count() - 1)

    def update_patient_info(self):
        name, dob, age = self.page_one.get_patient_info()
        self.patient = Patient(name, dob, age)
