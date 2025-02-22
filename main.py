import sys
import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QMessageBox, QWidget

from mpl_canvas import MyDynamicMplCanvas, np

class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")
        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                         QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)
        self.help_menu = QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)
        self.help_menu.addAction('&About', self.about)
        self.main_widget = QWidget(self)
        l = QVBoxLayout(self.main_widget)
        self.dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(self.dc)

        self.scroll = QtWidgets.QScrollBar(QtCore.Qt.Horizontal)
        l.addWidget(self.scroll)
        self.scroll.setValue(99)
        self.step = .1
        self.setupSlider()

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def setupSlider(self):
        self.lims = np.array(self.dc.axes.get_xlim())
        print("limit" + str(self.lims))
        self.scroll.setPageStep(self.step * 100)
        self.scroll.sliderReleased.connect(self.update)

        self.update()

    def update(self, evt=None):
        r = self.scroll.value() / ((1 + self.step) * 100)
        l1 = self.lims[0] + r * np.diff(self.lims)
        l2 = l1 + np.diff(self.lims) * self.step
        self.dc.axes.set_xlim(l1, l2)
        print(self.scroll.value(), l1, l2)
        self.dc.fig.canvas.draw_idle()

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",
                                """Particle Data Visualization Tool
                                    Copyright 2019 Institute of Physics and Technology

                                    This application is designed to visualize data from a scintillator detector.
                                    The data is retrieved from a PostgreSQL database and plotted using Matplotlib.

                                    Key Features:
                                    - Fetches data from a database containing timestamps and particle counts.
                                    - The vector represents the number of registered charged particles in a scintillator.
                                    - Plots the data dynamically with interactive features like zoom and scroll.

                                    This tool is built using PyQt5 for the GUI and Matplotlib for plotting.
                                    It is intended for scientific and educational purposes."""
                                )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("PyQt5 Matplot Example")
    aw.show()
    app.exec_()