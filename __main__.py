#!/usr/bin/env python3

import settings
import acquisition
import export

from gui.gui import MainWindow
from process import DataScaling

def validate_settings():
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


def main():
    validate_settings()

    serial = acquisition.FakeSerial()
    gui = MainWindow()
    transform = DataScaling()

    serial.source.connect(transform.process)
    transform.source.connect(gui.plots.new_data)

    gui.start.connect(serial.start)
    gui.stop.connect(serial.stop)

    exporters = []
    for name, params in settings.export.items():
        exporter = export.FORMATS[params['format']](name, params)
        if params['stage'] == 'acquisition':
            serial.source.connect(exporter.update)
        elif params['stage'] == 'transform':
            transform.source.connect(exporter.update)
        exporters.append(exporter)

    for e in exporters:
        gui.start.connect(e.start)
        gui.stop.connect(e.stop)

    gui.show()


if __name__ == '__main__':
    main()
