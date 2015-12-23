from PySide import QtCore
import settings

class Processor(QtCore.QObject):
    source = QtCore.Signal(object)

    def __init__(self):
        super().__init__()

class ProcessorThread(QtCore.QThread):
    def __init__(self):
        super().__init__()


        
class DataScaling(Processor):
    def __init__(self):
        super().__init__()

    @QtCore.Slot(object)
    def process(self, data):
        assert settings.NUMBER_OF_SENSORS == len(data.src_values)

        for i in range(settings.NUMBER_OF_SENSORS):
            if settings.transform[i]:
                data.values.append(
                    settings.transform[i](data.src_values[i])
                )
            else:
                data.values.append(data.src_values[i])

        # re-emit data after processing
        self.source.emit(data)


