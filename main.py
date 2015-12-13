import settings
import acquisition
from plot import Plotter

def validate_settings():
    assert settings.NUMBER_OF_SENSORS > 0

    for i in range(settings.NUMBER_OF_SENSORS):
        # reverse-update plot parameters with defaults
        s = settings.plots['default'].copy()
        if i in settings.plots:
            s.update(settings.plots[i])
        settings.plots[i] = s

def main():
    validate_settings()

    serial = acquisition.FakeSerial()
    plot = Plotter()

    serial.source.connect(plot.new_data)

    serial.start()
    plot.run()


if __name__ == '__main__':
    main()
