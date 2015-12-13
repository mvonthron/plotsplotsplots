from PySide import QtGui, QtCore
import pyqtgraph as pg

import settings


class Plotter(QtCore.QObject):
    def __init__(self):
        super().__init__()

        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow('Plots plots plots!')

        self.y_data = []
        self.plot_widget = []
        self.plot = []

    def add_plot(self, win, index):
        plot_widget = win.addPlot(name='Plot {}'.format(index))

        plot = plot_widget.plot(antialias=True, pen={'color': 'F66'})

        plot_widget.setLabel('left', 'Value', units='V')
        plot_widget.setLabel('bottom', 'Time', units='s')
        plot_widget.setXRange(0, 1000)
        plot_widget.setYRange(0, 10)

        return plot_widget, plot

    def setup(self):
        for i in range(settings.NUMBER_OF_SENSORS):
            if i > 0 and i % settings.PLOTS_PER_ROw == 0:
                self.win.nextRow()

            w, p = self.add_plot(self.win, i)
            self.plot_widget.append(w)
            self.plot.append(p)
            self.y_data.append([])



    def run(self):
        self.setup()

        self.win.show()
        self.app.exec_()

    @QtCore.Slot(object)
    def new_data(self, data):
        # print(" received ->", data)
        for i in range(settings.NUMBER_OF_SENSORS):
            self.y_data[i].append(data.src_values[i])
            self.plot[i].setData(y=self.y_data[i])


if __name__ == '__main__':
    p = Plotter()
    p.run()





