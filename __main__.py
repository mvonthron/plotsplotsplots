#!/usr/bin/env python3

import settings
import acquisition
import export

from gui.gui import MainWindow
from process import DataScaling

class App:
    def __init__(self):
        self.validate()

        self.serial = acquisition.FakeSerial()
        self.gui = MainWindow()
        self.transform = DataScaling()

        self.serial.source.connect(self.transform.process)
        self.transform.source.connect(self.gui.plots.new_data)

        self.gui.start.connect(self.serial.start)
        self.gui.stop.connect(self.serial.stop)

        self.exporters = []
        for name, params in settings.export.items():
            exporter = export.FORMATS[params['format']](name, params)
            if params['stage'] == 'acquisition':
                self.serial.source.connect(exporter.update)
            elif params['stage'] == 'transform':
                self.transform.source.connect(exporter.update)
            self.exporters.append(exporter)

        for e in self.exporters:
            self.gui.start.connect(e.start)
            self.gui.stop.connect(e.stop)

    def start(self):
        self.gui.show()

    def validate(self):
        assert settings.NUMBER_OF_SENSORS > 0

        if settings.transform['default'] and not hasattr(settings.transform['default'], '__call__'):
                print("default transformation must be callable or None")
                settings.transform['default'] = None

        for i in range(settings.NUMBER_OF_SENSORS):
            # reverse-update plot parameters with defaults
            s = settings.plots['default'].copy()
            if i in settings.plots:
                s.update(settings.plots[i])
            settings.plots[i] = s

            # check transforms
            if i not in settings.transform or not hasattr(settings.transform[i], '__call__'):
                settings.transform[i] = settings.transform['default']

        for name, params in settings.export.items():
            if params['format'] not in export.FORMATS:
                print("Invalid export format: {}", params['format'])


if __name__ == '__main__':
    App().start()
