from PySide import QtCore
import os
import settings

class TextExport(QtCore.QObject):
    def __init__(self, name, params):
        super().__init__()
        self.stage = params['stage']
        self.filename = params['filename']
        self.file = None

    def __del__(self):
        self.stop()

    def start(self):
        d = os.path.dirname(self.filename)
        if not os.path.exists(d):
            os.makedirs(d)

        self.file = open(self.filename, 'w')

    def stop(self):
        if self.file and not self.file.closed:
            self.file.flush()
            self.file.close()

    @QtCore.Slot(object)
    def update(self, data):
        if self.file is None or self.file.closed:
            return

        # @todo duplicate with switch in __main__
        if self.stage == 'acquisition':
            self.file.write('; '.join(map(str, data.src_values)))
        elif self.stage == 'transform':
            self.file.write('; '.join(map(str, data.values)))
        self.file.write('\n');


# exporters list
FORMATS = {
    'text': TextExport
}
