import sys
from PySide import QtGui, QtCore

from gui.mainwindow import Ui_MainWindow
from gui.plots import Plotter
import settings

import qdarkstyle
import pyqtgraph as pg

class MainWindow(QtGui.QMainWindow):
    # signals
    start = QtCore.Signal()
    stop = QtCore.Signal()
    reset = QtCore.Signal()

    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.app.setApplicationName("Plots! Plots! Plots!")

        self.app.setStyleSheet(qdarkstyle.load_stylesheet())
        # self.app.setStyle(QtGui.QGtkStyle())
        self.plotter = None
        self.state = {
            'started': False,
            'fullscreen': False
        }

        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.validateUi()
        self.addPlotWidget()
        self.setupSignalForward()



    def validateUi(self):
        """
        Since mainwindow.py is generated from a UI file we run
        a few checks to validate the basic UI components are there
        """
        assert hasattr(self.ui, 'startStopButton')
        assert hasattr(self.ui, 'resetButton')

    def addPlotWidget(self):
        del self.ui.placeholder
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.ui.horizontalLayout.addWidget(self.plotWidget)

        self.plotter = Plotter(self.plotWidget)
        self.plotter.setup()

    def setupSignalForward(self):
        self.ui.startStopButton.clicked.connect(self.startStop)
        self.ui.resetButton.clicked.connect(self.plotter.clear)
        self.plotter.fpsMessage.connect(self.ui.statusbar.showMessage)

        # @todo loop over checkboxes (tried with lambda+getattr but didn't work in loop)
        self.ui.show1.stateChanged.connect(lambda state: self.plotter.setPlotShownState(state, 0))
        self.ui.show2.stateChanged.connect(lambda state: self.plotter.setPlotShownState(state, 1))
        self.ui.show3.stateChanged.connect(lambda state: self.plotter.setPlotShownState(state, 2))
        self.ui.show4.stateChanged.connect(lambda state: self.plotter.setPlotShownState(state, 3))
        self.ui.show5.stateChanged.connect(lambda state: self.plotter.setPlotShownState(state, 4))
        self.ui.show6.stateChanged.connect(lambda state: self.plotter.setPlotShownState(state, 5))
        self.ui.show7.stateChanged.connect(lambda state: self.plotter.setPlotShownState(state, 6))
        self.ui.show8.stateChanged.connect(lambda state: self.plotter.setPlotShownState(state, 7))

    @QtCore.Slot()
    def startStop(self):
        if self.state['started']:
            self.stop.emit()
            self.ui.startStopButton.setText('Start')
        else:
            self.start.emit()
            self.ui.startStopButton.setText('Stop')

        self.state['started'] = not self.state['started']

    def show(self):
        self.plotter.clear()
        super().show()
        return self.app.exec_()

    def fullscreen(self):
        if not 'fullscreen' in self.state or not self.state['fullscreen']:
            self.state['fullscreen'] = True
            self.ui.menubar.setVisible(False)
            self.ui.statusbar.setVisible(False)
            self.showFullScreen()
        else:
            self.state['fullscreen'] = False
            self.showNormal()
            self.ui.menubar.setVisible(True)
            self.ui.statusbar.setVisible(True)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F11:
            self.fullscreen()

    @property
    def plots(self):
        return self.plotter

if __name__ == '__main__':
    mainWin = MainWindow()
    sys.exit(mainWin.show())