
import threading
import queue
from datetime import datetime
import time

import numpy as np
from PySide import QtCore

from messages import DataPacket
import settings

class Serial(threading.Thread):
    def __init__(self):
        super().__init__()
        output = queue.Queue()

    def run(self):
        pass


class FakeSerial(QtCore.QThread):
    # signals must be part of the class definition
    # http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html
    source = QtCore.Signal(object)

    def __init__(self):
        super().__init__()
        self.start_time = time.time()*1000
        self._run = False

    def run(self):
        self._run = True

        for i in range(1000):
            if not self._run:
                break

            d = DataPacket()
            d.src_timestamp = time.time()*1000 - self.start_time
            d.src_values = list(np.random.random_sample(settings.NUMBER_OF_SENSORS))
            d.src_values[0] *= 1024
            d.src_values[1] = 2 + d.src_values[1]/10
            d.src_values[4] += np.sin(i/60)*settings.plots[4]['yrange'][1]*0.4 + 4
            d.src_values[5] += 500
            d.time_received = datetime.now()

            self.source.emit(d)

            time.sleep(0.01)

        self._run = False

    @QtCore.Slot()
    def stop(self):
        self._run = False