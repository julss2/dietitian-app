from PyQt6.QtWidgets import QWidget, QPushButton

class Page0Home(QWidget):
    """
    Class representing the home page of the application.

    Parameters:
    - main_window (QWidget): The main window of the application from which button references are retrieved.

    Attributes:
    - pushButton_1 (QPushButton): Button 1 on the home page.
    - pushButton_2 (QPushButton): Button 2 on the home page.
    - pushButton_3 (QPushButton): Button 3 on the home page.

    Methods:
    - set_page(index): Switches the page in the main widget to the page with the specified index.

    """
    def __init__(self, main_window):
        """
        Initializes the home page.

        Parameters:
        - main_window (QWidget): The main window of the application from which button references are retrieved.
        """
        super(Page0Home, self).__init__()

        # Odniesienie do przycisku w pliku UI
        self.pushButton_1 = main_window.findChild(QPushButton, "pushButton_1")
        self.pushButton_2 = main_window.findChild(QPushButton, "pushButton_2")
        self.pushButton_3 = main_window.findChild(QPushButton, "pushButton_3")

        # Połącz przycisk z funkcją
        self.pushButton_1.clicked.connect(lambda: self.set_page(1))
        self.pushButton_2.clicked.connect(lambda: self.set_page(2))
        self.pushButton_3.clicked.connect(lambda: self.set_page(3))


    # Funkcja przycisków: go to x page
    def set_page(self, index):
        """
        Switches the page in the main widget to the page with the specified index.

        Parameters:
        - index (int): The index of the page to which the main widget should be switched.
        """
        self.stacked_widget.setCurrentIndex(index)



