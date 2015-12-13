import settings

class DataPacket:
    def __init__(self):
        self.src_timestamp = None
        self.src_values = [None]*settings.NUMBER_OF_SENSORS
        self.time_received = None
