from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

class Plotter(QtCore.QObject):
    def __init__(self):
        super().__init__()

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

        y = [0, 0.1, 0.2, 0.001, 0.3]
        self.plot = self.plot_widget.plot(y=y, antialias=True, pen={'color': 'F66'})

        self.plot_widget.setLabel('left', 'Value', units='V')
        self.plot_widget.setLabel('bottom', 'Time', units='s')
        self.plot_widget.setXRange(0, 6)
        self.plot_widget.setYRange(0, 1)

    def show(self):
        self.win.show()
        self.app.exec_()


if __name__ == '__main__':
    p = Plotter()
    p.show()
