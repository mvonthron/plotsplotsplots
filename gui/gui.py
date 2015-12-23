import sys
from PySide import QtGui, QtCore

from gui.mainwindow import Ui_MainWindow
from gui.plots import Plotter

import qdarkstyle
import pyqtgraph as pg

class MainWindow(QtGui.QMainWindow):
    # signals
    start = QtCore.Signal()
    stop = QtCore.Signal()
    reset = QtCore.Signal()

    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        # self.app.setStyleSheet(qdarkstyle.load_stylesheet())
        self.app.setStyle(QtGui.QGtkStyle())
        self.plotter = None

        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.addPlotWidget()


    def addPlotWidget(self):
        del self.ui.placeholder
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.ui.horizontalLayout.addWidget(self.plotWidget)

        self.plotter = Plotter(self.plotWidget)
        self.plotter.setup()

    def setupSignalForward(self):
        pass

    def show(self):
        self.plotter.clear()
        super().show()
        return self.app.exec_()

    @property
    def plots(self):
        return self.plotter

if __name__ == '__main__':
    mainWin = MainWindow()
    sys.exit(mainWin.show())