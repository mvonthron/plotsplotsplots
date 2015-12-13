
SENSOR_NUMBER = 8

class DataPacket:
    def __init__(self):
        self.src_timestamp = None
        self.src_values = [None]*SENSOR_NUMBER
        self.time_received = None
