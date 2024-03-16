from PyQt6.QtWidgets import QWidget, QComboBox, QLabel, QSpinBox, QPushButton, QDateEdit, QMessageBox
from PyQt6.QtCore import QDate
from database import DatabaseHandler

class EditMesaurement(QWidget):
    """
    Class representing the editing of measurements for a patient.

    Parameters:
    - combobox (QComboBox): Dropdown list for selecting patients.
    - label_height (QLabel): Display label for patient's height.
    - label_birth (QLabel): Display label for patient's birth date.
    - spinbox (QSpinBox): Input widget for entering weight.
    - date (QDateEdit): Input widget for entering measurement date.
    - saveButton (QPushButton): Button for saving the measurement.

    Attributes:
    - comboBox_pacients (QComboBox): Dropdown list for selecting patients.
    - label_height (QLabel): Display label for patient's height.
    - label_date (QLabel): Display label for patient's birth date.
    - spinBox_weight_2 (QSpinBox): Input widget for entering weight.
    - dateEdit_3 (QDateEdit): Input widget for entering measurement date.
    - pushButton_2save (QPushButton): Button for saving the measurement.
    - db_handler (DatabaseHandler): Object for handling database operations.

    Methods:
    - load_patients(): Loads patients into the QComboBox dropdown list.
    - display_chosen_patient_info(): Displays information about the selected patient.
    - save(): Saves the entered weight measurement into the database.
    - clear_fields(): Clears the input fields for weight and measurement date.
    - show_popup(s: str): Displays a popup message with the given text.

    """
    def __init__(self, combobox, label_height, label_birth, spinbox, date, saveButton):
        """
        Initializes the EditMeasurement class.

        Parameters:
        - combobox (QComboBox): Dropdown list for selecting patients.
        - label_height (QLabel): Display label for patient's height.
        - label_birth (QLabel): Display label for patient's birth date.
        - spinbox (QSpinBox): Input widget for entering weight.
        - date (QDateEdit): Input widget for entering measurement date.
        - saveButton (QPushButton): Button for saving the measurement.
        """
        super(EditMesaurement, self).__init__()

        self.comboBox_pacients = combobox
        self.label_height = label_height
        self.label_date = label_birth
        self.spinBox_weight_2 = spinbox
        self.dateEdit_3 = date
        self.pushButton_2save = saveButton
        
        # Utwórz obiekt DatabaseHandler ~ JR
        print('zaraz uwtorze obiekt z bazy ')
        self.db_handler = DatabaseHandler(database_file='dietician_app.db')
        
        # Połącz rozwijaną lise z funkcja wczytywania pacjentów
        self.load_patients()
        self.comboBox_pacients.currentIndexChanged.connect(self.display_chosen_patient_info)
        print('już utworzylem teraz czekam az zapiszesz ')
        # Połącz przycisk z funkcją save
        self.pushButton_2save.clicked.connect(self.save)

        

    # Wczytanie bazy pacjentów do rozwijanej listy QComboBox
    def load_patients(self):
        """
        Loads patients into the QComboBox dropdown list.
        """
        patients = self.db_handler.get_all_patients()
        if patients:
            self.comboBox_pacients.clear()
            self.comboBox_pacients.addItems([f"{patient[1]} {patient[2]}" for patient in patients])
        else:
            print("Brak pacjentów w bazie danych")
            self.show_popup("Brak pacjentów w bazie danych")

            
    # Wyświetlanie informacji o wybranym pacjencie 
    def display_chosen_patient_info(self):
        """
        Displays information about the selected patient.
        """
        chosen_patient_index = self.comboBox_pacients.currentIndex()
        if chosen_patient_index >= 0:
            chosen_patient_id = self.db_handler.get_all_patients()[chosen_patient_index][0]
            patient_info = self.db_handler.get_patient(chosen_patient_id)
            if patient_info:
                birth_date = patient_info[1]
                height = patient_info[0]
                self.label_date.setText(f"{birth_date}")
                self.label_height.setText(f"{height}")
            else:
                print("Nie można uzyskać informacji o pacjencie.")
                self.show_popup("Nie można uzyskać informacji o pacjencie.")
        else:
            print("Nie wybrano pacjenta")
            self.show_popup("Nie wybrano pacjenta.")
    
    #zapisanie wagi do bazy
    def save(self):
        """
        Saves the entered weight measurement into the database.
        """
        try:
            print('zaczynam zapisywać')
            chosen_patient_index = self.comboBox_pacients.currentIndex()
            if chosen_patient_index >= 0:
                all_patients = self.db_handler.get_all_patients()
                if all_patients is not None and len(all_patients) > chosen_patient_index:
                    chosen_patient_id = self.db_handler.get_all_patients()[chosen_patient_index][0]
                    value = self.spinBox_weight_2.value() #pobieram wartość ze spinbox
                    weight = float(value) #zapisanie wagi w formacie 00,00
                    measurement_date = self.dateEdit_3.date().toPyDate() 
                    # Dodaj pomiar do bazy danych
                    self.db_handler.add_measurement(chosen_patient_id, weight, measurement_date)
                    print(f'Weight ({chosen_patient_id}: {weight})')
                    self.clear_fields()
                else:
                    print("Nieprawidłowy indeks pacjenta")
            else:
                print("Nie wybrano pacjenta")

        # sprawdzenie
            print(f'Weight: {weight}')
        except Exception as e:
            print(f"Błąd podczas zapisywania pomiaru {e}")
            self.show_popup(f"Błąd podczas zapisywania pomiaru {e}")

    def clear_fields(self):
        """
        Clears the input fields for weight and measurement date.
        """
        self.spinBox_weight_2.setValue(65)
        date = QDate(2024, 1, 1)
        self.dateEdit_3.setDate(date)

    def show_popup(self, s):
        """
        Displays a popup message with the given text.

        Parameters:
        - s (str): Text to be displayed in the popup.
        """
        message = QMessageBox()
        message.setWindowTitle("Message")
        message.setText(s)
        x = message.exec() 