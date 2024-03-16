from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QDate

from Patient import Patient
from database import DatabaseHandler
#from datetime import date

class EnterPacient(QWidget):
    def __init__(self, line_edit1, line_edit2, date_edit, spin_box1, push_button):
        super(EnterPacient, self).__init__()
        """
        Initialize the EnterPacient widget.

        Parameters:
            - line_edit1: QLineEdit - First name input field
            - line_edit2: QLineEdit - Second name input field
            - date_edit: QDateEdit - Date of birth input field
            - spin_box1: QSpinBox - Height input field
            - push_button: QPushButton - Save button
        """

        # Przypisanie argumentów do klasy
        self.lineFirst_Name = line_edit1
        self.lineSecond_Name = line_edit2
        self.date_of_birth = date_edit
        self.spinBox_height = spin_box1
        self.saveButton1 = push_button
        self.labelError = None
        
        # Utwórz obiekt DatabaseHandler 
        self.db_handler = DatabaseHandler(database_file='dietician_app.db')
        
        # Połączenie metody save ze zdarzeniem klinięcia przycisku
        self.saveButton1.clicked.connect(self.save)

    # Funkcja zapisująca dane wpisane w okienka
    def save(self):
        """
        Save patient data to the database.

        Raises:
            Exception: If an error occurs during the saving process.
        """
        try:
            #spisanie wartości z pól aplikacji
            first_name = self.lineFirst_Name.text()
            last_name = self.lineSecond_Name.text()
            birth_date = self.date_of_birth.date().toPyDate()
            height = self.spinBox_height.value()

            #stworz obiekt Pacjent
            new_patient = Patient(first_name, last_name, birth_date, height)

            # Sprawdzenie czy wypełnione są obowiązkowe pola
            if first_name and last_name and birth_date:

                # Wyłącz przycisk zapisz, aby zapobiec wielokrotnym kliknięciom
                self.saveButton1.setEnabled(False)

                # Dodaj pacjenta do bazy danych 
                self.db_handler.add_patient(new_patient)
                self.show_popup("Zapisano dane do bazy")                
                print(f"Pacjent dodany do bazy danych: {first_name}, {last_name}, {birth_date}, {height}")

                # Czyszczenie pól wejściowych
                self.clear_fields()

                # Włącz ponownie przycisk zapisz
                self.saveButton1.setEnabled(True)
            else:
                print("Uzupełnij wszystkie obowiązkowe pola.")
                self.show_popup("Uzupełnij wszystkie obowiązkowe pola.")
        except Exception as e:
            print(f"Błąd podczas zapisywania pacjenta {e}")
            self.show_popup(f"Błąd podczas zapisywania pacjenta {e}")

    # Czyszczenie okienek po dodaniu pacjenta
    def clear_fields(self):
        """
        Clear input fields after adding a patient.
        """
        self.lineFirst_Name.clear()
        self.lineSecond_Name.clear()
        date = QDate(2000, 1, 1)
        self.date_of_birth.setDate(date)
        self.spinBox_height.setValue(165) 

    def show_popup(self, s):
        """
        Display a popup message.

        Parameters:
            - s: str - Message to be displayed in the popup.
        """
        message = QMessageBox()
        message.setWindowTitle("Message")
        message.setText(s)
        x = message.exec() 
        
    


        