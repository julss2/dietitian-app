from PyQt6.QtWidgets import QApplication
from MainWindowUI import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())