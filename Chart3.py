from PyQt6.QtWidgets import QVBoxLayout, QWidget
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime


class ChartWidget(QWidget):
    """
    Widget for displaying a line chart of weight measurements over time.

    Attributes:
    - figure (Figure): Matplotlib figure for the chart.
    - canvas (FigureCanvas): Matplotlib canvas for rendering the figure.

    Methods:
    - __init__(parent=None): Initializes the ChartWidget with an optional parent widget.
    - set_data(id, handler): Sets the patient ID and database handler for retrieving data.
    - statistics_chart(): Generates and displays the weight change chart based on patient measurements.

    """
    def __init__(self, parent=None):
        """
        Initializes the ChartWidget.

        Parameters:
        - parent (QWidget): Optional parent widget.
        """
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        self._pat_id = None
        self._db_hand = None

    def set_data(self, id, handler):
        """
        Sets the patient ID and database handler for retrieving data.

        Parameters:
        - id (int): Patient ID.
        - handler: Database handler object.
        """
        self._pat_id = id
        self._db_hand = handler
        self.statistics_chart()

    def statistics_chart(self):
        """
        Generates and displays the weight change chart based on patient measurements.
        """
        if self._pat_id is not None and self._db_hand is not None:
            measurements = self._db_hand.get_patient_measurements_chart(self._pat_id)
            print("Measurements:", measurements)
            print(type(measurements))
            if measurements:
                dates = [tpl[0] for tpl in measurements]
                weights = [tpl[1] for tpl in measurements]

                # for tuple in measurements:
                #     print("Dateee")
                #     dates = measurements[tuple][0]
                #     print("weighttttt")
                #     weights = measurements[tuple][1]

               # dates, weights = zip(*measurements)
                #dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in dates]
                #daty jako stingi
                #date_strings = [date.strftime("%Y-%m-%d") for date in dates]

                print("Dates: ", dates)
                print("weights: ", weights)
                print(type(dates))
                print(type(dates[0]))
                print(type(weights))
                print(type(weights[0]))



                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.plot(dates, weights, marker='o', linestyle='-', color='b')

                ax.set_title("Zmiana wagi w czasie")
                ax.set_xlabel("Data pomiaru")
                ax.set_ylabel("Waga")

                ax.xaxis_date()
                self.canvas.draw()
