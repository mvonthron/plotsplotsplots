import threading
import time
from queue import Queue

from PySide import QtGui, QtCore
import pyqtgraph as pg

class Watcher(QtCore.QThread):
    def __init__(self, parent, queue):
        super().__init__()
        self.parent = parent
        self.queue = queue

    def run(self):
        while True:
            i = self.queue.get()
            print("received", i)
            self.queue.task_done()
            self.parent.new_data(i)

class Plotter(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.watcher = Watcher(self, queue)

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

        y = [0, 0.1, 0.2, 0.001, 0.3]
        self.plot = self.plot_widget.plot(y=y, antialias=True, pen={'color': 'F66'})

        self.plot_widget.setLabel('left', 'Value', units='V')
        self.plot_widget.setLabel('bottom', 'Time', units='s')
        self.plot_widget.setXRange(0, 6)
        self.plot_widget.setYRange(0, 1)

    def run(self):
        self.setup()
        self.watcher.start()

        self.win.show()
        self.app.exec_()

    def new_data(self, i):
        print("Received new data:", i)


if __name__ == '__main__':
    queue = Queue()

    p = Plotter(queue)
    p.start()

    print('launched')
    for i in range(10, 0, -1):
        queue.put(i)
        time.sleep(0.5)




