from PySide import QtGui, QtCore
import time
from math import ceil

import pyqtgraph as pg

import settings

class Plot:
    def __init__(self, i=None, s=None):
        self.index = i
        self.settings = s

        self.widget = None
        self.plot = None
        self.data = []

        if self.settings is not None:
            self._setup()

    def _setup(self):
        self.widget = pg.PlotItem(name=self.settings['title'].format(index=self.index))

        self.plot = self.widget.plot(antialias=True, pen={'color': self.settings['color']})

        if 'fill' in self.settings and self.settings['fill']:
            self.plot.setData(fillLevel=0, brush=self.settings['fill'])

        self.widget.setLabel('left', 'Force', units='N')
        self.widget.setLabel('bottom', 'Time', units='s')

        self.widget.setXRange(self.settings['xrange'][0], self.settings['xrange'][1])
        self.widget.setYRange(self.settings['yrange'][0], self.settings['yrange'][1])

    def append(self, i):
        self.data.append(i)
        self.plot.setData(y=self.data)

    def clear(self):
        self.data = []
        self.plot.clear()


class TimePlot(Plot):
    def __init__(self, i=None, s={}):
        self.src_line = None
        self.src_data = []
        self.last_src_time = None

        self.rcv_line = None
        self.rcv_data = []
        self.last_rcv_time = None

        super().__init__(i, s)

        del self.plot
        
    def _setup(self):
        self.widget = pg.PlotItem(name="Timing")
        self.widget.setXRange(settings.plots['default']['xrange'][0], settings.plots['default']['xrange'][1])
        self.widget.setYRange(0, settings.target_period*2)
        self.widget.setLabel('left', 'Period', units='s')
        self.widget.setLabel('bottom', 'Time', units='s')

        # reference
        self.widget.addLine(y=settings.target_period, pen={'color': '333'})

        self.src_line = self.widget.plot(antialias=True, pen={'color': 'F00'})
        self.rcv_line = self.widget.plot(antialias=True, pen={'color': '00F'})

        return self.widget

    def append(self, rcv, src):
        if self.rcv_line:
            if self.last_rcv_time:
                self.rcv_data.append(rcv - self.last_rcv_time)
                self.rcv_line.setData(y=self.rcv_data)
            self.last_rcv_time = rcv

        if self.src_line:
            if self.last_src_time:
                self.src_data.append(src - self.last_src_time)
                self.src_line.setData(y=self.src_data)
            self.last_src_time = src

    def clear(self):
        if self.rcv_line:
            self.rcv_data = []
            self.last_rcv_time = None
            self.rcv_line.clear()

        if self.src_line:
            self.src_data = []
            self.last_src_time = None
            self.src_line.clear()



class MasterPlot(Plot):
    def __init__(self, i=None, s={}):
        self.lines = []
        self.selection = None
        super().__init__(i, s)
        del self.plot

    def _setup(self):
        self.widget = pg.PlotItem(name="Master plot")
        for i in range(settings.NUMBER_OF_SENSORS):
            self.lines.append(self.widget.plot(antialias=True, pen={'color': settings.plots[i]['color']}))

        self.selection = pg.LinearRegionItem(settings.plots['default']['xrange'])
        self.selection.setZValue(-42)
        self.widget.addItem(self.selection)

    def clear(self):
        for line in self.lines:
            line.clear()

class Plotter(QtCore.QObject):
    fpsMessage = QtCore.Signal(str)

    def __init__(self, parent):
        super().__init__()

        self.win = parent
        self.plots = {}

        self.state = {
            # FPS calculation (for titlebar)
            'last_update': time.time(),
            'fps': 0.0,
        }

    def set_show_title(self, state):
        for i, plot in self.plots.items():
            if plot.settings.get('title', False):
                plot.widget.setTitle(plot.settings['title'].format(index=i) if state == QtCore.Qt.Checked else None)

        self.refresh_grid()

    def set_show_plot(self, state, index):
        assert index in settings.plots

        self.plots[index].settings['show'] = state == QtCore.Qt.Checked
        self.refresh_grid()

    def refresh_grid(self):
        self.win.clear()
        shown = 0

        for _, plot in self.plots.items():
            if plot.settings['show']:
                if plot.index != 'master':
                    self.win.addItem(plot.widget, row=shown/settings.PLOTS_PER_ROw, col=shown%settings.PLOTS_PER_ROw)
                    shown += 1

        if self.plots['master'].settings['show']:
            self.win.addItem(plot.widget, row=ceil(shown/settings.PLOTS_PER_ROw), col=0, colspan=settings.PLOTS_PER_ROw)

    def setXRegion(self):
        selection = self.plots['master'].selection
        for _, plot in self.plots.items():
            if plot.index != 'master' and plot.settings.get('link_master', True):
                plot.widget.setXRange(*selection.getRegion(), padding=0)

    def setup(self):
        for i in range(settings.NUMBER_OF_SENSORS):
            self.plots[i] = Plot(i, settings.plots[i])

        self.plots['time'] = TimePlot('time', settings.plots['time'])
        self.plots['master'] = MasterPlot('master', settings.plots['master'])

        if self.plots['master'].selection:
            selection = self.plots['master'].selection
            selection.sigRegionChanged.connect(self.setXRegion)

        self.refresh_grid()

    @QtCore.Slot(object)
    def new_data(self, data):
        # print(" received ->", data)
        for i in range(settings.NUMBER_OF_SENSORS):
            self.plots[i].append(data.values[i])
            self.plots['master'].lines[i].setData(y=self.plots[i].data)

        self.plots['time'].append(data.rcv_timestamp, data.src_timestamp)

        # update statusbar with FPS
        now = time.time()
        curr_fps = 1.0 / (now - self.state['last_update'])
        self.state['last_update'] = now
        self.state['fps'] = self.state['fps'] * 0.8 + curr_fps * 0.2
        self.fpsMessage.emit("%0.2f fps" % self.state['fps'])

    @QtCore.Slot()
    def clear(self):
        for i, plot in self.plots.items():
            plot.clear()


if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = pg.GraphicsWindow('Plots plots plots!')

    p = Plotter(win)
    # p.setup()

    win.show()
    app.exec_()




