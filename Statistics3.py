from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from database import DatabaseHandler
from Chart3 import ChartWidget

class Statistics(QWidget):
    def __init__(self, comboBox_pacients, label_date, label_height, tableMeasurements, chartMeasurements, lb_wL, lb_wH, lb_wM, dt_wL, dt_wH):
        """
        Initialize the Statistics widget.

        Parameters:
            - comboBox_pacients: QComboBox - Dropdown for selecting patients
            - label_date: QLabel - Label for displaying patient's birth date
            - label_height: QLabel - Label for displaying patient's height
            - tableMeasurements: QTableWidget - Table for displaying measurements
            - chartMeasurements: ChartWidget - Custom chart widget for displaying measurements
            - lb_wL: QLabel - Label for displaying minimum weight in statistics
            - lb_wH: QLabel - Label for displaying maximum weight in statistics
            - lb_wM: QLabel - Label for displaying average weight in statistics
            - dt_wL: QLabel - Label for displaying date of minimum weight in statistics
            - dt_wH: QLabel - Label for displaying date of maximum weight in statistics
        """
        super(Statistics, self).__init__()

        self.comboBox_pacients = comboBox_pacients
        self.label_height = label_height
        self.label_date = label_date
        self.table = tableMeasurements
        self.chartMes = chartMeasurements
        self.label_weightLow = lb_wL
        self.label_weightHigh = lb_wH
        self.label_weightMedium = lb_wM
        self.date_weightLow = dt_wL
        self.date_weightHigh = dt_wH

        self.db_handler = DatabaseHandler(database_file='dietician_app.db')

        # Wczytaj pacjentów z bazy danych i uzupełnij listę rozwijaną
        self.load_patients()
        self.comboBox_pacients.currentIndexChanged.connect(self.display_chosen_patient_info)

    def load_patients(self):
        """
        Load patients from the database and populate the combo box.
        """
        patients = self.db_handler.get_all_patients()
        if patients:
            self.comboBox_pacients.clear()
            self.comboBox_pacients.addItems([f"{patient[1]} {patient[2]}" for patient in patients])
        else:
            print("Brak pacjentów w bazie danych")
            self.show_popup("Brak pacjentów w bazie danych")

    def display_chosen_patient_info(self):
        """
        Display information for the selected patient.
        """
        chosen_patient_index = self.comboBox_pacients.currentIndex()
        all_patients = self.db_handler.get_all_patients() #lista pacjentów

        if not all_patients:
            print("Brak pacjentów w bazie danych.")
            return

        if 0 <= chosen_patient_index < len(all_patients):
            chosen_patient_id = all_patients[chosen_patient_index][0]
            patient_info = self.db_handler.get_patient(chosen_patient_id)

            if patient_info:
                birth_date, height = patient_info
                self.label_date.setText(f"{birth_date}")
                self.label_height.setText(f"{height}")
                self.display_measurements(chosen_patient_id)
                self.display_statistics(chosen_patient_id)
                try:
                    # Tworzenie nowej instancji ChartWidget
                    new_chart_widget = ChartWidget()
                    # Przypisanie nowego obiektu do self.chartMes
                    self.chartMes = new_chart_widget
                    self.display_chart(chosen_patient_id)
                    print("wykres zrobiony")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Brak informacji o wybranym pacjencie.")
        else:
            print("Nieprawidłowy indeks pacjenta.")

    def display_measurements(self, patient_id):
        """
        Display measurements for the selected patient in the table.
        """
        measurements = self.db_handler.get_patient_measurements(patient_id)
        self.table.setRowCount(0)
        for measurement in measurements:
            date, weight, bmi = measurement
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(date)))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(weight)))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(bmi)))

    def display_statistics(self, patient_id):
        """
        Display statistics for the selected patient.
        """
        try:
            statistics = self.db_handler.get_statistics(patient_id)
            if statistics and len(statistics) == 1:
                (max_weight, min_weight, avg_weight, date_max_weight, date_min_weight) = statistics[0]
                avg_weight = float(avg_weight) #zapisanie wagi w formacie 00,00
                self.label_weightLow.setText(f"{min_weight}")
                self.label_weightHigh.setText(f"{max_weight}")
                self.label_weightMedium.setText(f"{avg_weight}")
                self.date_weightLow.setText(f"{date_min_weight}")
                self.date_weightHigh.setText(f"{date_max_weight}")
            else:
                print("Nie można uzyskać informacji statystycznych.")
                self.show_popup("Nie można uzyskać informacji statystycznych.")
        except Exception as e:
            print(f"Error: {e}")

    def display_chart(self, id):
        """
        Display a chart for the selected patient.
        """
        try:
            self.chartMes.set_data(id, self.db_handler)
            self.chartMes.statistics_chart()
        except Exception as e:
            print(f"Error: {e}")


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

