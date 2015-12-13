
import threading
import queue
from datetime import datetime
import time

import numpy as np
from PySide import QtCore

from messages import DataPacket, SENSOR_NUMBER

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
    sink = QtCore.Signal(object)

    def __init__(self):
        super().__init__()
        self.start_time = time.time()*1000

    def run(self):
        for i in range(1000):
            d = DataPacket()
            d.src_timestamp = time.time()*1000 - self.start_time
            d.src_values = list(np.random.random_sample(SENSOR_NUMBER))
            d.src_values[0] += 5
            d.src_values[1] += 2
            d.time_received = datetime.now()

            self.source.emit(d)

            time.sleep(0.01)