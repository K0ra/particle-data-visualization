import numpy as np
import datetime
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy

from db_connection import DatabaseConnection, pg

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                               QSizePolicy.Expanding,
                               QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.connect()

    def setYearlyParameters(self, datetimeValues):
        years = mdates.YearLocator()   # every year
        months = mdates.MonthLocator()  # every month
        tickFmt = mdates.DateFormatter('%Y')

        datemin = np.datetime64(datetimeValues[0], 'Y')
        datemax = np.datetime64(datetimeValues[-1], 'Y') + np.timedelta64(1, 'Y')

        return years, months, tickFmt, datemin, datemax

    def connect(self):
        db_conn = DatabaseConnection()
        conn = db_conn.connect()

        if conn is not None:
            try:
                cur = conn.cursor()
                query = "SELECT * FROM p ORDER BY datep, timeut"
                cur.execute(query)
                print("The number of parts: ", cur.rowcount)

                i = 0
                row = 1
                datet = np.zeros(cur.rowcount, dtype=datetime.datetime)
                ch_1 = np.zeros(cur.rowcount)

                while row is not None:
                    row = cur.fetchone()
                    if row is None:
                        break

                    date, time, vec = row
                    vec = np.array(vec, dtype=np.float)
                    datet[i] = datetime.datetime.combine(date, time)
                    vec[np.isnan(vec)] = 0
                    # For the trial purposes ONLY the first channel is considered
                    ch_1[i] = vec[0]
                    i += 1

                self.axes.plot(datet.tolist(), ch_1.tolist(), 'r')

                months, days, tickFmt, datemin, datemax = self.setYearlyParameters(datet.tolist())

                # format the ticks
                self.axes.xaxis.set_major_locator(months)
                self.axes.xaxis.set_major_formatter(tickFmt)
                self.axes.xaxis.set_minor_locator(days)

                self.axes.set_xlim(datemin, datemax)

                self.axes.grid(True)

                # rotates and right aligns the x labels, and moves the bottom of the
                # axes up to make room for them
                self.fig.autofmt_xdate()
                self.draw()

                cur.close()

            except (Exception, pg.DatabaseError) as error:
                print(error)
            finally:
                conn.close()
                print('Database connection closed.')
