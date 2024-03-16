from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton, QLineEdit, QSpinBox, QDoubleSpinBox, QLabel, QTableWidget, QDateEdit, QComboBox, QWidget
from PyQt6 import uic
import sys
from Page0Home import Page0Home
from MenuButtons import MenuButtons
from EnterPacient1 import EnterPacient
from EditMesaurement2 import EditMesaurement
from Statistics3 import Statistics


class MainWindow(QMainWindow):
    """
    Main application window class.

    Attributes:
    - stackedWidget (QStackedWidget): Stacked widget for managing different pages.
    - page0 (Page0Home): Instance of the Page0Home class representing the home page.
    - menu (MenuButtons): Instance of the MenuButtons class for handling menu buttons.
    - page1_enter_pacient (EnterPacient): Instance of the EnterPacient class for entering patient information.
    - page2_enter_pacient (EditMesaurement): Instance of the EditMesaurement class for editing patient measurements.
    - page3_display_table (Statistics): Instance of the Statistics class for displaying statistics.

    Methods:
    - __init__(): Initializes the main window, loads the UI file, and sets up various pages and widgets.

    """
    def __init__(self):
        """
        Initializes the main window, loads the UI file, and sets up various pages and widgets.
        """
        super(MainWindow, self).__init__()
        uic.loadUi("mainWindowStacked.ui", self)                        # Wczytaj plik UI
        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")  # Odniesienie do QStackedWidget w pliku UI

        # wrzucenie strony Home na stos | plik Page0Home
        self.page0 = Page0Home(self)
        self.page0.stacked_widget = self.stackedWidget
        self.stackedWidget.addWidget(self.page0)
        self.menu = MenuButtons(self.stackedWidget,self)

        #znalezienie przycisków na page1 | plik EnterPacient1
        line_edit_name1 = self.findChild(QLineEdit, "lineFirst_Name")
        line_edit_name2 = self.findChild(QLineEdit, "lineSecond_Name")
        date_edit = self.findChild(QDateEdit, "date_of_birth")
        spin_box_height = self.findChild(QSpinBox, "spinBox_height")
        bttn_save = self.findChild(QPushButton, "pushButton_1save")
        # Utwórz obiekt klasy EnterPacient i przekaż dane od uzytkownika
        self.page1_enter_pacient = EnterPacient(line_edit_name1, line_edit_name2, date_edit, spin_box_height, bttn_save)

        #page2
        comboBox_pacients =self.findChild(QComboBox, "comboBox3")
        label_age = self.findChild(QLabel, "label_age")
        label_date = self.findChild(QLabel, "label_height")
        spinBox_weight_2 = self.findChild(QDoubleSpinBox, "spinBox_weight_2")
        dateEdit_3 = self.findChild(QDateEdit, "dateEdit_3")
        pushButton_2save = self.findChild(QPushButton, "pushButton_2save")
        # Utwórz obiekt klasy EnterPacient i przekaż dane od uzytkownika
        self.page2_enter_pacient = EditMesaurement(comboBox_pacients, label_age, label_date, spinBox_weight_2,
                                                dateEdit_3, pushButton_2save)

        #page3
        comboBox_pacients = self.findChild(QComboBox, "comboBox3_4")
        label_age3 = self.findChild(QLabel, "label_age3_4")
        label_date3 = self.findChild(QLabel, "label_height3_4")
        table = self.findChild(QTableWidget, "tableWidget_3")
        chart = self.findChild(QWidget, "widgetChart")
        weightLow = self.findChild(QLabel,"label_weightLow")
        weightHigh = self.findChild(QLabel,"label_weightHigh")
        weightMed  = self.findChild(QLabel,"label_weightMedium")
        dateLow = self.findChild(QLabel,"date_weightLow")
        dateHigh = self.findChild(QLabel,"date_weightHigh")
        self.page3_display_table = Statistics(comboBox_pacients, label_age3, label_date3, table, chart, weightLow, weightHigh, weightMed,
                                              dateLow, dateHigh)
        

