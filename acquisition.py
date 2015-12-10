
import threading
import queue
from datetime import datetime
import time
import random

from types import DataPacket

class Serial(threading.Thread):
    def __init__(self):
        super().__init__(self)
        output = queue.Queue()

    def run(self):
        pass


class FakeSerial(threading.Thread):
    def __init__(self):
        super().__init__(self)
        self.output = queue.Queue()
        self.start_time = time.time()*1000

    def run(self):
        d = DataPacket()
        d.src_timestamp = time.time()*1000 - self.start_time
        d.received = datetime.now()

        self.output.put(d)