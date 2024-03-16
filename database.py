import sqlite3
from Patient import Patient

class DatabaseHandler:
    # Ustawienia połączenia
    def __init__(self, database_file):
        """
        Initializes the DatabaseHandler instance.

        Parameters:
        - database_file (str): The path to the SQLite database file.
        """
        self.connection = sqlite3.connect(database_file)
        self.create_tables()
        
    # Tworzenie tabel w bazie danych, jeśli nie istnieją
    def create_tables(self):
        create_patients_table = '''
            CREATE TABLE IF NOT EXISTS PATIENTS (
                PATIENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                FIRST_NAME VARCHAR(64) NOT NULL,
                LAST_NAME VARCHAR(128) NOT NULL,
                BIRTHDATE DATE NOT NULL,
                HEIGHT INTEGER NOT NULL DEFAULT 0
            )
        '''

        create_measurements_table = '''
            CREATE TABLE IF NOT EXISTS MEASUREMENTS (
                MEASUREMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                PATIENT_ID INTEGER,
                MEASUREMENT_DATE DATE NOT NULL DEFAULT CURRENT_DATE,
                WEIGHT DECIMAL(5,2) NOT NULL,
                BMI DECIMAL(4,2) NOT NULL,
                FOREIGN KEY (PATIENT_ID) REFERENCES PATIENTS(PATIENT_ID) ON DELETE CASCADE
            )
        '''
        
        cursor = self.connection.cursor()
        cursor.execute(create_patients_table)
        cursor.execute(create_measurements_table)
        self.connection.commit()

    # Wykonywanie zapytania
    def execute_query(self, query, data=None):
        """
        Executes an SQL query on the database.

        Parameters:
        - query (str): The SQL query to be executed.
        - data (tuple): Data to be inserted into the query.

        Note: If data is provided, it will be used to parameterize the query.
        """
        cursor = self.connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        self.connection.commit()
        cursor.close()

    # Dodawanie nowego pacjenta
    def add_patient(self, patient):
        """
        Adds a new patient to the database.

        Parameters:
        - first_name (str): First name of the patient.
        - last_name (str): Last name of the patient.
        - birth_date (str): Birth date of the patient (formatted as 'YYYY-MM-DD').
        - height (int, optional): Height of the patient in centimeters.
        """
        if not patient.first_name or not patient.last_name or not patient.birth_date:
            print("Uzupełnij wszystkie obowiązkowe pola.")
            return
        try:
            if patient.height is not None:
                query = "INSERT INTO PATIENTS (FIRST_NAME, LAST_NAME, BIRTHDATE, HEIGHT) VALUES (?, ?, ?, ?)"
                data = (patient.first_name, patient.last_name, patient.birth_date, patient.height)
            else:
                query = "INSERT INTO PATIENTS (FIRST_NAME, LAST_NAME, BIRTHDATE) VALUES (?, ?, ?)"
                data = (patient.first_name, patient.last_name, patient.birth_date)
            
            self.execute_query(query, data)
            print("Pacjent dodany do bazy danych.")
        except sqlite3.Error as err:
            print(f"SQLite error: {err}")
        
    # Usuwanie pacjenta TODO
    def delete_patient(self, patient_id):
        """
        Deletes a patient from the database.

        Parameters:
        - patient_id (int): The ID of the patient to be deleted.
        """
        query = "DELETE FROM PATIENTS WHERE PATIENT_ID = ?"
        data = (patient_id,)
        
        try:
            self.execute_query(query, data)
            print(f"Pacjent o ID {patient_id} został usunięty z bazdy danych.")
        except sqlite3.Error as err:
            print(f"Błąd {err}")
            
    # Modyfikacja danych pacjenta TODO
    def update_patient(self, patient_id, new_first_name=None, new_last_name=None, new_birth_date=None, new_height=None):
        """
        Updates patient data in the database.

        Parameters:
        - patient_id (int): The ID of the patient to be updated.
        - new_first_name (str, optional): New first name of the patient.
        - new_last_name (str, optional): New last name of the patient.
        - new_birth_date (str, optional): New birth date of the patient (formatted as 'YYYY-MM-DD').
        - new_height (int, optional): New height of the patient in centimeters.
        """
        if not patient_id:
            print("Podaj ID pacjenta do zaktualizowania.")
            return
        
        if new_first_name is None and new_last_name is None and new_birth_date is None and new_height is None:
            print ("Nie podano danych do aktualizacji.")
            return
        
        query = "UPDATE PATIENTS SET "
        updates_data = []
        
        if new_first_name is not None:
            updates_data.append(f"FIRST_NAME = '{new_first_name}'")
            
        if new_last_name is not None:
            updates_data.append(f"LAST_NAME = '{new_last_name}'")
            
        if new_birth_date is not None:
            updates_data.append(f"BIRTHDATE = '{new_birth_date}'")
            
        if new_height is not None:
            updates_data.append(f"HEIGHT = '{new_height}'")
            
        query += ', '.join(updates_data)
        query += f" WHERE PATIENT_ID ={patient_id}"
        
        try:
            self.execute_query(query)
            print(f"Dane pacjenta o ID {patient_id} zostały zaktualizowane")
        except sqlite3.Error as err:
            print(f"Błąd: {err}")
            
    # Pobierz wszystkich pacjentów
    def get_all_patients(self):
        """
        Retrieves a list of all patients in the database.

        Returns:
        - list: A list of tuples containing patient data.
        """
        query = "SELECT * FROM PATIENTS"
        cursor = self.connection.cursor()
        
        try:
            cursor.execute(query)
            patients = cursor.fetchall()
            print("lista pacjentow: ", patients) #DO USUNIĘCIA
            return patients
        except sqlite3.Error as err:
            print(f"Błąd: {err}")
            return None
        finally:
            cursor.close()
            
    # Pobierz jednego pacjenta
    def get_patient(self, patient_id):
        """
        Retrieves birth date and height of a specific patient.

        Parameters:
        - patient_id (int): The ID of the patient.

        Returns:
        - tuple: A tuple containing the birth date and height of the patient.
        """
        query = "SELECT BIRTHDATE, HEIGHT FROM PATIENTS WHERE PATIENT_ID = ?"
        data = (patient_id,)
        
        try:
            patient = self.execute_query_with_result(query, data)
            return patient[0] if patient else None
        except sqlite3.Error as err:
            print(f"Błąd: {err}")
            return None
            
    
    # Dodawanie nowego pomiaru
    def add_measurement(self, patient_id, weight, measurement_date=None):
        """
        Adds a new measurement for a patient to the database.

        Parameters:
        - patient_id (int): The ID of the patient.
        - weight (float): The weight measurement.
        - measurement_date (str, optional): Measurement date (formatted as 'YYYY-MM-DD').
        """
        if not patient_id or not weight:
            print("Uzupełnij wszystkie obowiązkowe pola.")
            return
        
        try:
            # Pobranie wzrostu pacjenta
            height_query = "SELECT HEIGHT FROM PATIENTS WHERE PATIENT_ID = ?"
            height_data = (patient_id,)
            height_result = self.execute_query_with_result(height_query, height_data)
            
            if height_result and height_result[0][0] > 0:
                height = height_result[0][0]
                bmi = round(weight / ((height / 100) ** 2), 2)
            else:
                print(f"Nie można obliczyć BMI, brak danych o wzroście dla pacjenta o ID {patient_id}")
                return
            
            if measurement_date is None:
                query = "INSERT INTO MEASUREMENTS (PATIENT_ID, WEIGHT, BMI) VALUES (?, ?, ?)"
                data = (patient_id, weight, bmi)
            else:
                query = "INSERT INTO MEASUREMENTS (PATIENT_ID, WEIGHT, MEASUREMENT_DATE, BMI) VALUES (?, ?, ?, ?)"
                data = (patient_id, weight, measurement_date, bmi)
            
            self.execute_query(query, data)
            print("Nowy pomiar dodany do bazy danych.")
        except sqlite3.Error as err:
            print(f"Błąd: {err}")
            
    # Metoda do wykonania zapytania z wynikiem
    def execute_query_with_result(self, query, data=None):
        """
        Executes an SQL query on the database and returns the result.

        Parameters:
        - query (str): The SQL query to be executed.
        - data (tuple): Data to be inserted into the query.

        Returns:
        - list: A list of tuples containing the query result.
        """
        cursor = self.connection.cursor()
        result = None
        
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
                
            result = cursor.fetchall()
        except sqlite3.Error as err:
            print(f"Błąd: {err}")
        
        cursor.close()
        return result

    # Usuwanie pomiaru
    def delete_measurement(self, measurement_id):
        """
        Deletes a measurement from the database.

        Parameters:
        - measurement_id (int): The ID of the measurement to be deleted.
        """
        if not measurement_id:
            print("Podaj ID pomiaru do usunięcia.")
            return
        
        try:
            query = 'DELETE FROM MEASUREMENTS WHERE MEASUREMENT_ID = ?'
            data = (measurement_id,)
            
            self.execute_query(query, data)
            print(f"Pomiar o ID {measurement_id} został usunięty z bazy danych.")
        except sqlite3.Error as err:
            print(f"Błąd: {err}")
                
    # Modyfikacja pomiaru
    def update_measurement(self, measurement_id, new_weight=None, new_measurement_date=None):
        """
        Updates measurement data in the database.

        Parameters:
        - measurement_id (int): The ID of the measurement to be updated.
        - new_weight (float, optional): New weight measurement.
        - new_measurement_date (str, optional): New measurement date (formatted as 'YYYY-MM-DD').
        """
        if not measurement_id:
            print("Podaj ID pomiaru do zaktualizowania.")
            return

        if new_weight is None and new_measurement_date is None:
            print("Nie podano danych do aktualizacji pomiaru.")
            return

        try:
            # Pobranie wzrostu pacjenta
            height_query = "SELECT HEIGHT FROM PATIENTS WHERE PATIENT_ID IN (SELECT PATIENT_ID FROM MEASUREMENTS WHERE MEASUREMENT_ID = ?)"
            height_data = (measurement_id,)
            height_result = self.execute_query_with_result(height_query, height_data)

            if height_result and height_result[0][0] > 0:
                height = height_result[0][0]
                new_bmi = round(new_weight / ((height / 100) ** 2), 2) if new_weight is not None else None
            else:
                print(f"Nie można obliczyć BMI, brak danych o wzroście dla pacjenta o ID {measurement_id}")
                return

            query = "UPDATE MEASUREMENTS SET "
            updates_data = []

            if new_weight is not None:
                updates_data.append(f"WEIGHT = {new_weight}")
                updates_data.append(f"BMI = {new_bmi}")

            if new_measurement_date is not None:
                pdates_data.append(f"MEASUREMENT_DATE = '{new_measurement_date}'")

            query += ', '.join(updates_data)
            query += f" WHERE MEASUREMENT_ID = {measurement_id}"

            self.execute_query(query)
            print(f"Pomiar o ID {measurement_id} został zaktualizowany.")
        except sqlite3.Error as err:
            print(f"Błąd: {err}")   
        
    # Pobierz pomiary pacjenta
    def get_patient_measurements(self, patient_id):
        """
        Retrieves all measurements for a specific patient.

        Parameters:
        - patient_id (int): The ID of the patient.

        Returns:
        - list: A list of tuples containing measurement data.
        """

        query = "SELECT MEASUREMENT_DATE, WEIGHT, BMI FROM MEASUREMENTS WHERE PATIENT_ID = ? ORDER BY MEASUREMENT_DATE"
        data = (patient_id,)
        
        try:
            measurements = self.execute_query_with_result(query, data)
            return measurements
        except sqlite3.Error as err:
            print(f"Błąd: {err}")
            return None
    
    # Pobierz pomiary pacjenta do wykresu
    def get_patient_measurements_chart(self, patient_id):
        """
        Retrieves measurements for a specific patient for charting purposes.

        Parameters:
        - patient_id (int): The ID of the patient.

        Returns:
        - list: A list of tuples containing measurement date and weight.
        """
        query = "SELECT MEASUREMENT_DATE, WEIGHT FROM MEASUREMENTS WHERE PATIENT_ID = ? ORDER BY MEASUREMENT_DATE"
        data = (patient_id,)
        
        try:
            measurements = self.execute_query_with_result(query, data)
            return measurements
        except sqlite3.Error as err:
            print(f"Błąd: {err}")
            return None
    
    #Pobierz statystyki
    def get_statistics(self, patient_id):
        """
        Retrieves statistics for a specific patient.

        Parameters:
        - patient_id (int): The ID of the patient.

        Returns:
        - list: A list containing max weight, min weight, avg weight, date of max weight, and date of min weight.
        """
        query = """
            SELECT 
                MAX(WEIGHT) AS max_weight, 
                MIN(WEIGHT) AS min_weight, 
                ROUND(AVG(WEIGHT), 2) as avg_weight, 
                (SELECT MAX(MEASUREMENT_DATE)
                FROM MEASUREMENTS
                WHERE PATIENT_ID = ?
                AND WEIGHT = (SELECT MAX(WEIGHT)
                            FROM MEASUREMENTS
                            WHERE PATIENT_ID = ?
                            )
                ) AS date_max_weight,
                (SELECT MIN(MEASUREMENT_DATE)
                FROM MEASUREMENTS
                WHERE PATIENT_ID = ?
                AND WEIGHT = (SELECT MIN(WEIGHT)
                            FROM MEASUREMENTS
                            WHERE PATIENT_ID = ?
                            )
                ) AS date_min_weight
            FROM MEASUREMENTS 
            WHERE PATIENT_ID = ?
        """
        data = (patient_id, patient_id, patient_id, patient_id, patient_id)
        
        try:
            statistics = self.execute_query_with_result(query, data)

            if statistics and statistics[0]:
                return statistics
            else:
                print("No statistics available for the selected patient.")
                return None
        except sqlite3.Error as err:
            print(f"Błąd: {err}")
            return None
    
    def close_connection(self):
        """Closes the database connection."""
        self.connection.close()
        
    
    
def main():
    db_handler = DatabaseHandler(database_file='dietician_app.db')
    db_handler.close_connection()

if __name__ == "__main__":
    main()
