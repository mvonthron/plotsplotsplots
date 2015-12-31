from PySide import QtGui, QtCore
import time
from math import ceil

import pyqtgraph as pg

import settings


class Plotter(QtCore.QObject):
    fpsMessage = QtCore.Signal(str)

    def __init__(self, parent):
        super().__init__()

        self.win = parent

        self.y_data = []
        self.plot_widget = []
        self.plot = []

        self.src_line = None
        self.src_data = []
        self.rcv_line = None
        self.rcv_data = []
        self.time_plot_widget = None
        self.master_plot_widget = None
        self.master_plot_line = []

        self.fps = 0.0
        self.lastUpdate = time.time()

        self.state = {
            # Timing plot
            'last_src_time': None,
            'last_rcv_time': None,

            # FPS calculation
            'last_update': time.time(),
            'fps': 0.0,
        }

    def add_plot(self, win, index):
        params = settings.plots[index]

        plot_widget = pg.PlotItem(name=params['title'].format(index=index))

        plot = plot_widget.plot(antialias=True, pen={'color': params['color']})
        if 'fill' in params and params['fill']:
            plot.setData(fillLevel=0, brush=params['fill'])

        plot_widget.setLabel('left', 'Force', units='N')
        plot_widget.setLabel('bottom', 'Time', units='s')

        plot_widget.setXRange(params['xrange'][0], params['xrange'][1])
        plot_widget.setYRange(params['yrange'][0], params['yrange'][1])

        return plot_widget, plot

    def add_time_plot(self, win):
        plot_widget = pg.PlotItem(name="Timing")
        plot_widget.setXRange(settings.plots['default']['xrange'][0], settings.plots['default']['xrange'][1])
        plot_widget.setYRange(0, settings.target_period*2)
        plot_widget.setLabel('left', 'Period', units='s')
        plot_widget.setLabel('bottom', 'Time', units='s')

        # reference
        plot_widget.addLine(y=settings.target_period, pen={'color': '333'})

        self.src_line = plot_widget.plot(antialias=True,pen={'color': 'F00'})
        self.rcv_line = plot_widget.plot(antialias=True,pen={'color': '00F'})

        return plot_widget

    def add_master_plot(self, win):
        plot_widget = pg.PlotItem(name="Master plot")
        for i in range(settings.NUMBER_OF_SENSORS):
            self.master_plot_line.append(plot_widget.plot(antialias=True, pen={'color': settings.plots[i]['color']}))

        return plot_widget

    # @todo refactor naming + common Plot instance
    def set_show_title(self, state):
        for i in range(settings.NUMBER_OF_SENSORS):
            self.plot_widget[i].setTitle(settings.plots[i]['title'].format(index=i) if state == QtCore.Qt.Checked else None)
        self.time_plot_widget.setTitle(settings.plots['time']['title'] if state == QtCore.Qt.Checked else None)

        self.refresh_grid()

    def set_show_plot(self, state, index):
        assert index in settings.plots

        settings.plots[index]['show'] = state == QtCore.Qt.Checked
        self.refresh_grid()

    def refresh_grid(self):
        self.win.clear()
        shown = 0
        for i in range(settings.NUMBER_OF_SENSORS):
            if settings.plots[i]['show']:
                self.win.addItem(self.plot_widget[i], shown/settings.PLOTS_PER_ROw, shown%settings.PLOTS_PER_ROw)
                shown += 1

        if 'time' in settings.plots and 'show' in settings.plots['time'] and settings.plots['time']['show']:
            self.win.addItem(self.time_plot_widget, shown/settings.PLOTS_PER_ROw, shown%settings.PLOTS_PER_ROw)
            shown += 1

        if 'master' in settings.plots and 'show' in settings.plots['master'] and settings.plots['master']['show']:
            self.win.addItem(self.master_plot_widget, row=ceil(shown/settings.PLOTS_PER_ROw), col=0,
                             colspan=settings.PLOTS_PER_ROw)
            shown += 1

    def setup(self):
        for i in range(settings.NUMBER_OF_SENSORS):
            if i > 0 and i % settings.PLOTS_PER_ROw == 0:
                self.win.nextRow()

            w, p = self.add_plot(self.win, i)
            self.plot_widget.append(w)
            self.plot.append(p)
            self.y_data.append([])

        self.time_plot_widget = self.add_time_plot(self.win)
        self.master_plot_widget = self.add_master_plot(self.win)

        self.refresh_grid()

    @QtCore.Slot(object)
    def new_data(self, data):
        # print(" received ->", data)
        for i in range(settings.NUMBER_OF_SENSORS):
            self.y_data[i].append(data.values[i])
            self.plot[i].setData(y=self.y_data[i])
            self.master_plot_line[i].setData(y=self.y_data[i])

        if self.rcv_line:
            if self.state['last_rcv_time']:
                self.rcv_data.append(data.rcv_timestamp - self.state['last_rcv_time'])
                self.rcv_line.setData(y=self.rcv_data)
            self.state['last_rcv_time'] = data.rcv_timestamp

        if self.src_line:
            if self.state['last_src_time']:
                self.src_data.append(data.src_timestamp - self.state['last_src_time'])
                self.src_line.setData(y=self.src_data)
            self.state['last_src_time'] = data.src_timestamp

        now = time.time()
        curr_fps = 1.0 / (now - self.state['last_update'])
        self.state['last_update'] = now
        self.state['fps'] = self.state['fps'] * 0.8 + curr_fps * 0.2
        self.fpsMessage.emit("%0.2f fps" % self.state['fps'])

    @QtCore.Slot()
    def clear(self):
        for i in range(settings.NUMBER_OF_SENSORS):
            self.y_data[i] = []
            self.plot[i].clear()

        if self.rcv_line:
            self.rcv_data = []
            self.state['last_rcv_time'] = None
            self.rcv_line.clear()

        if self.src_line:
            self.src_data = []
            self.state['last_src_time'] = None
            self.src_line.clear()


if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = pg.GraphicsWindow('Plots plots plots!')

    p = Plotter(win)
    # p.setup()

    win.show()
    app.exec_()




