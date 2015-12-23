import sys
from PySide.QtGui import *
from PySide.QtCore import *

from gui.mainwindow import Ui_MainWindow
from gui.plots import Plotter

import qdarkstyle
import pyqtgraph as pg

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        # self.app.setStyleSheet(qdarkstyle.load_stylesheet())
        self.app.setStyle(QGtkStyle())

        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.addPlotWidget()

    def show(self):
        super().show()
        return self.app.exec_()

    def addPlotWidget(self):
        del self.placeholder
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.horizontalLayout.addWidget(self.plotWidget)

        self.plotter = Plotter(self.plotWidget)

        self.plotter.setup()

    @property
    def plots(self):
        return self.plotter

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    app.setStyle(QGtkStyle())

    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)