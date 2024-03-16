from PyQt6.QtWidgets import QWidget, QPushButton


class MenuButtons(QWidget):
    """
    Class representing menu buttons for navigating between pages in a stacked widget.

    Parameters:
    - stacked_widget (QStackedWidget): Reference to the QStackedWidget managing different pages.
    - main_window: Reference to the main application window.

    Attributes:
    - stacked_widget (QStackedWidget): Reference to the QStackedWidget managing different pages.
    - main_window: Reference to the main application window.
    - menuButton1 (QPushButton): Button for navigating to page 1.
    - menuButton2 (QPushButton): Button for navigating to page 2.
    - menuButton3 (QPushButton): Button for navigating to page 3.

    Methods:
    - __init__(stacked_widget, main_window): Initializes the MenuButtons class with references to stacked_widget and main_window.
    - set_page(index): Sets the current page of the stacked widget based on the provided index.

    """
    def __init__(self,stacked_widget, main_window):
        """
        Initializes the MenuButtons class.

        Parameters:
        - stacked_widget (QStackedWidget): Reference to the QStackedWidget managing different pages.
        - main_window: Reference to the main application window.
        """
        super(MenuButtons, self).__init__()

        self.stacked_widget = stacked_widget
        self.main_window = main_window

        # Odniesienie do przycisku w pliku UI
        self.menuButton1 = main_window.findChild(QPushButton, "menuButton1")
        self.menuButton2 = main_window.findChild(QPushButton, "menuButton2")
        self.menuButton3 = main_window.findChild(QPushButton, "menuButton3")

        #nadaj funkcję przyciskom (go to page)
        self.menuButton1.clicked.connect(lambda: self.set_page(1))
        self.menuButton2.clicked.connect(lambda: self.set_page(2))
        self.menuButton3.clicked.connect(lambda: self.set_page(3))

    # uniwersalna funkcja przycisków: go to x page
    def set_page(self, index):
        """
        Universal function for buttons to navigate to the specified page.

        Parameters:
        - index (int): Index of the page to navigate to.
        """
        self.stacked_widget.setCurrentIndex(index)
