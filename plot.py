import threading
import time
from queue import Queue

import numpy as np
from PySide import QtGui, QtCore
import pyqtgraph as pg

class Plotter(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.y = []
        self.y2 = []

    def setup(self):
        self.app = QtGui.QApplication([])
        self.win = QtGui.QMainWindow()
        self.win.setWindowTitle('Plot test')
        self.win.resize(600, 400)

        self.widget = QtGui.QWidget()
        self.win.setCentralWidget(self.widget)

        self.layout = QtGui.QGridLayout()
        self.widget.setLayout(self.layout)

        self.plot_widget = pg.PlotWidget(name='Plot1')
        self.layout.addWidget(self.plot_widget)

        self.plot = self.plot_widget.plot(antialias=True, pen={'color': 'F66'})

        self.plot_widget.setLabel('left', 'Value', units='V')
        self.plot_widget.setLabel('bottom', 'Time', units='s')
        self.plot_widget.setXRange(0, 1000)
        self.plot_widget.setYRange(0, 10)

        self.plot_widget2 = pg.PlotWidget(name='Plot2')
        self.layout.addWidget(self.plot_widget2)

        self.plot2 = self.plot_widget2.plot(antialias=True, pen={'color': '6F6'})

        self.plot_widget2.setLabel('left', 'Value', units='V')
        self.plot_widget2.setLabel('bottom', 'Time', units='s')
        self.plot_widget2.setXRange(0, 1000)
        self.plot_widget2.setYRange(0, 10)


    def run(self):
        self.setup()

        self.win.show()
        self.app.exec_()

    @QtCore.Slot(object)
    def new_data(self, data):
        # print(" received ->", i)
        self.y.append(data.src_values[0])
        self.plot.setData(y=self.y)

        self.y2.append(data.src_values[1])
        self.plot2.setData(y=self.y2)


if __name__ == '__main__':
    p = Plotter()
    p.run()





