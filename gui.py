import sys
from PySide.QtGui import *
from PySide.QtCore import *
from gui.mainwindow import Ui_MainWindow

import qdarkstyle
import pyqtgraph as pg

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.addPlotWidget()
        # self.fillTreeView()

        self.show()

    def addPlotWidget(self):
        del self.placeholder
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.horizontalLayout.addWidget(self.plotWidget)

        self.plotWidget.addPlot(name="Test")
        self.plotWidget.addPlot(name="Test2")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    app.setStyle(QGtkStyle())

    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)