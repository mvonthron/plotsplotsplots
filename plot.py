import threading
import time
from queue import Queue

import numpy as np
from PySide import QtGui, QtCore
import pyqtgraph as pg


class DataInput(QtCore.QThread):
    source = QtCore.Signal(object)
    def __init__(self):
        super().__init__()
        # self.source = QtCore.Signal(int)

    def run(self):
        for i in range(1000):
            val = np.random.rand()
            # print(i, "->", val)
            self.source.emit(val)
            time.sleep(0.01)

class Plotter(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.dataIn = DataInput()
        self.dataIn.source.connect(self.new_data)


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

        self.y = [0, 0.1, 0.2, 0.001, 0.3]
        self.plot = self.plot_widget.plot(y=self.y, antialias=True, pen={'color': 'F66'})

        self.plot_widget.setLabel('left', 'Value', units='V')
        self.plot_widget.setLabel('bottom', 'Time', units='s')
        # self.plot_widget.setXRange(0, 100)
        # self.plot_widget.setYRange(0, 1)

        self.dataIn.start()

    def run(self):
        self.setup()

        self.win.show()
        self.app.exec_()

    @QtCore.Slot(object)
    def new_data(self, i):
        # print(" received ->", i)
        self.y.append(i)
        self.plot.setData(y=self.y)


if __name__ == '__main__':
    p = Plotter()
    p.run()





