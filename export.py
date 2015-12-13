from PySide import QtCore
import settings

class TextExport(QtCore.QObject):
    def __init__(self, filename):
        super().__init__()
        self.file = open(filename, 'w')

    def __del__(self):
        if not self.file.closed:
            self.file.close()

    @QtCore.Slot(object)
    def update(self, data):
        self.file.write(str(data))


# exporters list
FORMATS = {
    'text': TextExport
}
