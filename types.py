
SENSOR_NUMBER = 8

class DataPacket:
    def __init__(self):
        self.src_timestamp = None
        self.src_value = [None]*SENSOR_NUMBER
        self.received = None
